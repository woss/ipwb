#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import md5
import json
import pywb.warc.cdxindexer
import ipfsApi

from io import BytesIO
from pywb.warc.archiveiterator import ArchiveIterator, DefaultRecordParser
from pywb.utils.loaders import LimitReader
from pywb.warc.recordloader import ArcWarcRecordLoader
from pywb.utils.bufferedreaders import DecompressingBufferedReader
from pywb.utils.statusandheaders import StatusAndHeadersParser
from surt import surt
from requests.packages.urllib3.exceptions import NewConnectionError

IP = '127.0.0.1'
PORT = '5001'

IPFS_API = ipfsApi.Client(IP, PORT)

# TODO: Check PEP-8 for indention guidance

def main():
    checkArgs(sys.argv) # Verify that a WARC file has been passed in
    textRecordParserOptions = {'cdxj': True, 'include_all': False, 'surt_ordered': False}
    cdxLines = ''
    ipfsRetryCount = 5 # Attempts to push a WARC record to IPFS before giving up
    ipfsTempPath = '/tmp/ipfs/'

    # Create temp path if it does not already exist
    if not os.path.exists(ipfsTempPath):
      os.makedirs(ipfsTempPath)

    # Read WARC file
    loader = ArcWarcRecordLoader(verify_http = True)
    print sys.argv
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

            resHeader = pullFromIPFS(httpHeaderIPFSHash)
            resPayload = pullFromIPFS(payloadIPFSHash)

            warcContents = resHeader + "\n\n" + resPayload


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


def checkArgs(args):
    print "checking args"
    print args
    print "done checking args"
    if len(args) < 2:
        logError("Usage:\n\n{0} </path/to/file.warc[.gz]>\n".format(args[0]))
        sys.exit(0)    

class TextRecordParser(DefaultRecordParser):

    def create_payload_buffer(self, entry):
        return BytesIO()


if __name__ == '__main__':
    checkArgs(sys.argv)
    main()
