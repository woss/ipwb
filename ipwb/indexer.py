#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import md5
import json
import pywb.warc.cdxindexer
import ipfsApi
import argparse

from io import BytesIO
from pywb.warc.archiveiterator import ArchiveIterator, DefaultRecordParser
from pywb.utils.loaders import LimitReader
from pywb.warc.recordloader import ArcWarcRecordLoader
from pywb.utils.bufferedreaders import DecompressingBufferedReader
from pywb.utils.statusandheaders import StatusAndHeadersParser
from surt import surt
from requests.packages.urllib3.exceptions import NewConnectionError
from requests.exceptions import ConnectionError
import requests

IP = '127.0.0.1'
PORT = '5001'

IPFS_API = ipfsApi.Client(IP, PORT)

# TODO: Check PEP-8 for indention guidance

def main():
    args = checkArgs(sys.argv)  # Verify that a WARC file has been passed in
    verifyDaemonIsAlive(args.daemon_address)
    verifyFileExists(args.warcPath)
    #verifyFileExists(

    textRecordParserOptions = {
      'cdxj': True,
      'include_all': False,
      'surt_ordered': False}
    cdxLines = ''
    ipfsRetryCount = 5  # Attempts to push a WARC record to IPFS before giving up
    ipfsTempPath = '/tmp/ipfs/'

    # Create temp path if it does not already exist
    if not os.path.exists(ipfsTempPath):
      os.makedirs(ipfsTempPath)

    # Read WARC file
    loader = ArcWarcRecordLoader(verify_http = True)
    warcFileFullPath = sys.argv[1]

    with open(warcFileFullPath, 'rb') as warc:
        iter = TextRecordParser(**textRecordParserOptions)

        for entry in iter(warc):
            # Only consider WARC response records from requests for web resources
            # TODO: Change conditional to return on non-HTTP responses to reduce branch depth
            if entry.record.rec_type != 'response' or entry.get('mime') in ('text/dns', 'text/whois'):
              continue

            hdrs = entry.record.status_headers
            hstr = hdrs.protocol + ' ' + hdrs.statusline
            for h in hdrs.headers:
                hstr += "\n" + ': '.join(h)

            statusCode = hdrs.statusline.split()[0]

            if not entry.buffer:
                return

            entry.buffer.seek(0)
            payload = entry.buffer.read()

            fileHash = md5.new(hstr).hexdigest()

            hdrfn = ipfsTempPath + 'header_' + fileHash
            pldfn = ipfsTempPath + 'payload_' + fileHash

            writeFile(hdrfn, hstr)
            writeFile(pldfn, payload)

            httpHeaderIPFSHash = ''
            payloadIPFSHash = ''
            retryCount = 0

            # TODO: First check that IPFS daemon is running, how do we do this?

            while retryCount < ipfsRetryCount:
                try:
                    httpHeaderIPFSHash = pushToIPFS(hdrfn)
                    payloadIPFSHash = pushToIPFS(pldfn)
                    break
                except NewConnectionError:
                    print 'IPFS daemon is likely not running.\nRun "ipfs daemon" in another terminal session.'
                    sys.exit()
                except:
                    logError('IPFS failed on ' + entry.get('url'))
                    #print sys.exc_info()[0]
                    retryCount += 1

            if retryCount >= ipfsRetryCount:
                logError('Skipping ' + entry.get('url'))

                continue

            uri = surt(entry.get('url'))
            timestamp = entry.get('timestamp')
            mime = entry.get('mime')

            encrKey = ''  # TODO

            obj = {
                'header_digest': httpHeaderIPFSHash,
                'payload_digest': payloadIPFSHash,
                'status_code': statusCode,
                'mime_type': mime,
                'encryption_key': encrKey,
                }
            objJSON = json.dumps(obj)

            cdxjLine = '{0} {1} {2}'.format(uri, timestamp, objJSON)
            cdxLines += cdxjLine
            print cdxjLine


            #print httpHeaderIPFSHash
            resHeader = pullFromIPFS(httpHeaderIPFSHash)
            #print resHeader
            resPayload = pullFromIPFS(payloadIPFSHash)

            warcContents = resHeader + "\n\n" + resPayload


def verifyDaemonIsAlive(hostAndPort):
    try:
      resp = requests.get('http://' + hostAndPort)
      return True
    except ConnectionError:
      print "Daemon is not running"
      sys.exit()

def verifyFileExists(warcPath):
    if os.path.isfile(warcPath):
      return
    print "File at " + warcPath + "does not exist!"
    sys.exit()

def logError(errIn):
    print >> sys.stderr, errIn


def pullFromIPFS(hash):
    global IPFS_API
    return IPFS_API.cat(hash)


def pushToIPFS(path):
    global IPFS_API
    res = IPFS_API.add(path)
    # TODO: verify that the add was successful
    return res['Hash']


def writeFile(filename, content):
    with open(filename, 'w') as tmpFile:
        tmpFile.write(content)


def checkArgs(argsIn):
    parser = argparse.ArgumentParser(description='InterPlanetary Wayback (ipwb) Indexer')
    parser.add_argument('-d', '--daemon', help='Location of ipfs daemon (default 127.0.0.1:5001)', default=IP+':'+PORT, dest='daemon_address')
    parser.add_argument('-o', '--outfile', help='Path of newly created CDXJ. Shows progress by default unless suppressed with -q')
    parser.add_argument('-p', '--progress', help='Show progress of processing WARC file.', action='store_true')
    parser.add_argument('-q', '--quiet', help='Quiet mode. Show nothing on stdout. Use -o to also write to a file.', action='store_true')
    parser.add_argument('warcPath', help="Path to a WARC[.gz] file")
    results = parser.parse_args()
    return results
    # TODO: create a logToFile() function if flag is set

class TextRecordParser(DefaultRecordParser):

    def create_payload_buffer(self, entry):
        return BytesIO()


if __name__ == '__main__':
    checkArgs(sys.argv)
    main()
