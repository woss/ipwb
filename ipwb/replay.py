#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import ipfsapi
import json
import subprocess
import pkg_resources
from pywb.utils.binsearch import iter_exact
from pywb.utils.canonicalize import unsurt
from pywb.utils.canonicalize import canonicalize as surt
from flask import Flask
from flask import Response
from requests.exceptions import ConnectionError

import requests

import util as ipwbConfig
from util import IPFSAPI_IP, IPFSAPI_PORT, IPWBREPLAY_IP, IPWBREPLAY_PORT
from util import INDEX_FILE
from requests import ReadTimeout

from Crypto.Cipher import XOR
import base64

app = Flask(__name__)
app.debug = False

IPFS_API = ipfsapi.Client(IPFSAPI_IP, IPFSAPI_PORT)


@app.route('/webui/<path:path>')
def showWebUI(path):
    webuiPath = '/'.join(('webui', path)).replace('ipwb.replay', 'ipwb')
    content = pkg_resources.resource_string(__name__, webuiPath)
    if 'index.html' in path:
        iFile = pkg_resources.resource_filename(__name__, INDEX_FILE)
        content = content.replace(
            'MEMCOUNT', str(retrieveMemCount(iFile)))
        content = content.replace(
            'var uris = []',
            'var uris = {0}'.format(getURIsInCDXJ(iFile)))
        content = content.replace('INDEXSRC', iFile)
    return Response(content)


@app.route('/daemon/<cmd>')
def commandDaemon(cmd):
    if cmd == 'status':
        return generateDaemonStatusButton()
    elif cmd == 'start':
        subprocess.Popen(['ipfs', 'daemon'])
        # retString = 'Failed to start IPFS daemon'
        # if 'Daemon is ready' in check_output():
        #  retString = 'IPFS daemon started'
        return Response('IPFS daemon starting...')

    elif cmd == 'stop':
        subprocess.call(['killall', 'ipfs'])
        return Response('IPFS daemon stopping...')
    else:
        print 'ERROR, bad command sent to daemon API!'
        print cmd
        return Response('bad command!')


@app.errorhandler(Exception)
def all_exception_handler(error):
    print error
    return 'Error', 500


# This route needs better restructuring but is currently only used to get the
# webUI location for the ipwb webUI, more setting might need to be fetched in
# the future.
@app.route('/config/<requestedSetting>')
def getRequestedSetting(requestedSetting):
    return Response(ipwbConfig.getIPFSAPIHostAndPort() + '/webui')


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def show_uri(path):
    global IPFS_API

    if len(path) == 0:
        return showWebUI('index.html')
        sys.exit()

    daemonAddress = '{0}:{1}'.format(IPFSAPI_IP, IPFSAPI_PORT)
    if not ipwbConfig.isDaemonAlive(daemonAddress):
        errStr = ('IPFS daemon not running. '
                  'Start it using $ ipfs daemon on the command-line '
                  ' or from the <a href="/">'
                  'IPWB replay homepage</a>.')
        return Response(errStr)

    # show the user profile for that user
    cdxLine = ''
    try:
        cdxLine = getCDXLine(surt(path))
    except:
        print sys.exc_info()[0]
        respString = ('{0} not found :(' +
                      ' <a href="http://{1}:{2}">Go home</a>').format(
            path, IPWBREPLAY_IP, IPWBREPLAY_PORT)
        return Response(respString)

    cdxParts = cdxLine.split(" ", 2)
    # surtURI = cdxParts[0]
    # datetime = cdxParts[1]
    jObj = json.loads(cdxParts[2])

    digests = jObj['locator'].split('/')

    try:
        payload = IPFS_API.cat(digests[-1], timeout=1)
        header = IPFS_API.cat(digests[-2])
    except ipfsapi.exceptions.TimeoutError:
        print "{0} not found at {1}".format(cdxParts[0], digests[-1])
        respString = ('{0} not found in IPFS :(' +
                      ' <a href="http://{1}:{2}">Go home</a>').format(
            path, IPWBREPLAY_IP, IPWBREPLAY_PORT)
        return Response(respString)
    except:
        print sys.exc_info()[0]
        print "general error"
        sys.exit()

    if 'encryption_method' in jObj:
        pKey = XOR.new(jObj['encryption_key'])
        payload = pKey.decrypt(base64.b64decode(payload))
        hKey = XOR.new(jObj['encryption_key'])
        header = hKey.decrypt(base64.b64decode(header))

    # print header
    # print payload
    hLines = header.split('\n')
    hLines.pop(0)

    resp = Response(payload)

    for idx, hLine in enumerate(hLines):
        k, v = hLine.split(': ', 1)
        if k.lower() != "content-type":
            k = "X-Archive-Orig-" + k
        resp.headers[k] = v

    return resp


def generateDaemonStatusButton():
    text = 'Not Running'
    buttonText = 'Start'
    if ipwbConfig.isDaemonAlive():
        text = 'Running'
        buttonText = 'Stop'

    statusPageHTML = '<html id="status{0}" class="status">'.format(buttonText)
    statusPageHTML += ('<head><base href="/webui/" /><link rel="stylesheet" '
                       'type="text/css" href="webui.css" />'
                       '<script src="webui.js"></script>'
                       '</head><body>')
    buttonHTML = '{0}<button>{1}</button>'.format(text, buttonText)
    footer = '<script>assignStatusButtonHandlers()</script></body></html>'
    return Response('{0}{1}{2}'.format(statusPageHTML, buttonHTML, footer))


def getIndexFileContents(cdxjFile=INDEX_FILE):
    if not os.path.exists(cdxjFile):
        return ""
    indexFilePath = '/{0}'.format(cdxjFile).replace('ipwb.replay', 'ipwb')

    indexFileContent = ''
    with open(cdxjFile, 'r') as f:
        indexFileContent = f.read()

    return indexFileContent


def getIndexFileFullPath(cdxjFile=INDEX_FILE):
    indexFilePath = '/{0}'.format(cdxjFile).replace('ipwb.replay', 'ipwb')

    indexFileName = pkg_resources.resource_filename(__name__, indexFilePath)
    return indexFileName


def getURIsInCDXJ(cdxjFile=INDEX_FILE):
    indexFileContents = getIndexFileContents(cdxjFile)

    if not indexFileContents:
        return 0

    lines = indexFileContents.strip().split('\n')

    uris = []
    for i, l in enumerate(lines):
        uris.append(unsurt(l.split(' ')[0]))
        pass
    return json.dumps(uris)


def retrieveMemCount(cdxjFile=INDEX_FILE):
    print "Retrieving URI-Ms from {0}".format(cdxjFile)
    indexFileContents = getIndexFileContents(cdxjFile)

    if not indexFileContents:
        return 0

    lines = indexFileContents.strip().split('\n')
    if not lines:
        print "Index file not found"
        return 0
    for i, l in enumerate(lines):
        pass
    return i + 1


def getCDXLine(surtURI, cdxjFile=INDEX_FILE):
    fullFilePath = getIndexFileFullPath(cdxjFile)
    with open(fullFilePath, 'r') as cdxFile:
        print "looking for {0} in {1}".format(surtURI, fullFilePath)
        bsResp = iter_exact(cdxFile, surtURI)
        cdxLine = bsResp.next()

        return cdxLine


def main():
    hostPort = ipwbConfig.getIPWBReplayConfig()
    if not hostPort:
        ipwbConfig.setIPWBReplayConfig(IPWBREPLAY_IP, IPWBREPLAY_PORT)
        hostPort = ipwbConfig.getIPWBReplayConfig()

    ipwbConfig.firstRun()

    app.run(host=IPWBREPLAY_IP, port=IPWBREPLAY_PORT)


if __name__ == "__main__":
    main()

# Read in URI, convert to SURT
#  surt(uriIn)
# Get SURTed URI lines in CDXJ
#  Read CDXJ
#  Do bin search to find relevant lines

# read IPFS hash from relevant lines (header, payload)

# Fetch IPFS data at hashes
