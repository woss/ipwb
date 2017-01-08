#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import sys
import os
import json
import ipfsapi
import argparse

from io import BytesIO
from pywb.warc.archiveiterator import DefaultRecordParser
from pywb.utils.canonicalize import canonicalize as surt
from requests.packages.urllib3.exceptions import NewConnectionError
from requests.exceptions import ConnectionError
import requests

from Crypto.Cipher import XOR
import base64

from __init__ import __version__ as ipwbVersion

IP = '127.0.0.1'
PORT = '5001'

IPFS_API = ipfsapi.Client(IP, PORT)


def indexFileAt(warcPath, encryptionKey=None, quiet=False):
    verifyFileExists(warcPath)

    textRecordParserOptions = {
      'cdxj': True,
      'include_all': False,
      'surt_ordered': False}
    cdxLines = ''
    ipfsRetryCount = 5  # WARC->IPFS attempts before giving up
    ipfsTempPath = '/tmp/ipfs/'

    # Create temp path for ipwb temp files if it does not already exist
    if not os.path.exists(ipfsTempPath):
        os.makedirs(ipfsTempPath)

    # Read WARC file
    # loader = ArcWarcRecordLoader(verify_http=True)
    warcFileFullPath = warcPath

    with open(warcFileFullPath, 'rb') as warc:
        iter = TextRecordParser(**textRecordParserOptions)

        for entry in iter(warc):
            # Only consider WARC resps records from reqs for web resources
            ''' TODO: Change conditional to return on non-HTTP responses
                      to reduce branch depth'''
            if entry.record.rec_type != 'response' or \
               entry.get('mime') in ('text/dns', 'text/whois'):
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

            # fileHash = md5.new(hstr).hexdigest()

            httpHeaderIPFSHash = ''
            payloadIPFSHash = ''
            retryCount = 0

            # TODO: First check that IPFS daemon is running, how do we do this?

            while retryCount < ipfsRetryCount:
                try:
                    if encryptionKey is not None:
                        # Dummy encryption, use something better in production
                        key = encryptionKey
                        if len(encryptionKey) == 0:
                            key = askUserForEncryptionKey()

                        hstr = XOR.new(key).encrypt(hstr)
                        hstr = base64.b64encode(hstr)

                        payload = XOR.new(key).encrypt(payload)
                        payload = base64.b64encode(payload)
                    httpHeaderIPFSHash = pushBytesToIPFS(bytes(hstr))
                    payloadIPFSHash = pushBytesToIPFS(bytes(payload))
                    break
                except NewConnectionError as e:
                    print('IPFS daemon is likely not running.')
                    print('Run "ipfs daemon" in another terminal session.')
                    sys.exit()
                except:
                    logError('IPFS failed on ' + entry.get('url'))
                    print(sys.exc_info())
                    retryCount += 1

            if retryCount >= ipfsRetryCount:
                logError('Skipping ' + entry.get('url'))

                continue

            uri = surt(entry.get('url'))
            timestamp = entry.get('timestamp')
            mime = entry.get('mime')

            # encrKey = ''  # TODO: Add data encryption functionality

            obj = {
                'locator': 'urn:ipfs/{0}/{1}'.format(
                  httpHeaderIPFSHash, payloadIPFSHash),
                'status_code': statusCode,
                'mime_type': mime
                }
            if encryptionKey is not None:
                obj['encryption_key'] = key
                obj['encryption_method'] = 'xor'
            objJSON = json.dumps(obj)

            cdxjLine = '{0} {1} {2}\n'.format(uri, timestamp, objJSON)
            cdxLines += cdxjLine

            if quiet:
                continue

            print(cdxjLine)
        if quiet:
            return cdxLines


def askUserForEncryptionKey():
    outputRedirected = os.fstat(0) != os.fstat(1)
    promptString = 'Enter a key for encryption: '
    if outputRedirected:  # Prevents prompt in redir output
        promptString = ''
        print(promptString, file=sys.stderr)

    key = raw_input(promptString)
    return key


def verifyDaemonIsAlive(hostAndPort):
    """Ensure that the IPFS daemon is running via HTTP before proceeding"""
    try:
        requests.get('http://' + hostAndPort)
    except ConnectionError:
        print('Daemon is not running at http://' + hostAndPort)
        sys.exit()


def verifyFileExists(warcPath):
    if os.path.isfile(warcPath):
        return
    print('File at ' + warcPath + ' does not exist!')
    sys.exit()


def logError(errIn):
    print(errIn, file=sys.stderr)


def pullFromIPFS(hash):
    global IPFS_API
    return IPFS_API.cat(hash)


def pushBytesToIPFS(bytes):
    """
    Call the IPFS API to add the byte string to IPFS.
    When IPFS returns a hash, return this to the caller
    """
    global IPFS_API

    res = IPFS_API.add_bytes(bytes)  # bytes)
    # TODO: verify that the add was successful

    # Receiving weirdness where res is sometimes a dictionary and sometimes
    #  a unicode string
    if type(res).__name__ == 'unicode':
        return res
    return res[0]['Hash']


def writeFile(filename, content):
    with open(filename, 'w') as tmpFile:
        tmpFile.write(content)


class TextRecordParser(DefaultRecordParser):

    def create_payload_buffer(self, entry):
        return BytesIO()


if __name__ == '__main__':
    checkArgs(sys.argv)
    main()
