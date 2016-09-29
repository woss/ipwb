#!/usr/bin/env python
# -*- coding: utf-8 -*-

from surt import surt
import sys
import os
import ipfsApi
import json
from pywb.utils.binsearch import iter_exact
from pywb.utils.canonicalize import unsurt
from flask import Flask
from flask import Response
from requests.exceptions import ConnectionError
from os.path import expanduser
import requests

app = Flask(__name__)
app.debug = True
# @app.route("/")
# def hello():
#    return "Hello World!"
IPFSAPI_IP = '127.0.0.1'
IPFSAPI_PORT = 5001
IPWBREPLAY_IP = '127.0.0.1'
IPWBREPLAY_PORT = 5000
IPFS_API = ipfsApi.Client(IPFSAPI_IP, IPFSAPI_PORT)
INDEX_FILE = 'samples/indexes/sample-2.cdxj'


@app.route('/webui/<path:path>')
def showWebUI(path):
    path = 'ipwb/webui/' + path
    with open(path, 'r') as webuiFile:
        content = webuiFile.read()
        if 'index.html' in path:
            content = content.replace('MEMCOUNT', str(retrieveMemCount()))
            content = content.replace(
              'var uris = []', 'var uris = ' + getURIsInCDXJ())
            content = content.replace('INDEXSRC', os.path.abspath(INDEX_FILE))
        return Response(content)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def show_uri(path):
    global IPFS_API, IPFSAPI_IP, IPFSAPI_PORT, IPWBREPLAY_IP, IPWBREPLAY_PORT

    if len(path) == 0:
        return showWebUI('index.html')
        sys.exit()

    if not isDaemonAlive(IP+':'+PORT):
        errStr = ('IPFS daemon not running. '
                  'Start it using $ ipfs daemon on the command-line '
                  ' or from the <a href="/">'
                  'IPWB replay homepage</a>')
        return Response(errStr)

    # (datetime, urir) = path.split('/', 1)
    # urir = path

    # show the user profile for that user
    cdxLine = ''
    try:
        cdxLine = getCDXLine(surt(path))
    except:
        respString = ('{0} not found :(' +
                      ' <a href="http://{1}:{2}">Go home</a>').format(
                        path, IP, PORT)
        return Response(respString)

    cdxParts = cdxLine.split(" ", 2)
    # surtURI = cdxParts[0]
    # datetime = cdxParts[1]
    jObj = json.loads(cdxParts[2])

    digests = jObj['locator'].split('/')

    payload = IPFS_API.cat(digests[-1])
    header = IPFS_API.cat(digests[-2])

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


def isDaemonAlive(hostAndPort):
    """Ensure that the IPFS daemon is running via HTTP before proceeding"""
    try:
        requests.get('http://' + hostAndPort)
        return True
    except ConnectionError:
        print "Daemon is not running at http://" + hostAndPort
        return False


def getURIsInCDXJ(cdxjFile=INDEX_FILE):
    with open(cdxjFile) as indexFile:
        uris = []
        for i, l in enumerate(indexFile):
            uris.append(unsurt(l.split(' ')[0]))
            pass
        return json.dumps(uris)


def retrieveMemCount():
    with open(INDEX_FILE, 'r') as cdxFile:
        for i, l in enumerate(cdxFile):
            pass
        return i+1


def getCDXLine(surtURI):
    with open(INDEX_FILE, 'r') as cdxFile:
        bsResp = iter_exact(cdxFile, surtURI)
        cdxLine = bsResp.next()
        return cdxLine


# IPFS Config manipulation from here on out.
def readIPFSConfig():
    with open(expanduser("~") + '/.ipfs/config', 'r') as f:
        return json.load(f)


def writeIPFSConfig(jsonToWrite):
    with open(expanduser("~") + '/.ipfs/config', 'w') as f:
        f.write(json.dumps(jsonToWrite, indent=4, sort_keys=True))


def getIPFSAPIPort(ipfsJSON=None):
    if not ipfsJSON:
        ipfsJSON = readIPFSConfig()
    ipfsAPIPort = os.path.basename(ipfsJSON['Addresses']['API'])


def getIPWBReplayConfig(ipfsJSON=None):
    if not ipfsJSON:
        ipfsJSON = readIPFSConfig()
    port = None
    if ('Ipwb' in ipfsJSON and 'Replay' in ipfsJSON['Ipwb'] and
       'Port' in ipfsJSON['Ipwb']['Replay']):
        host = ipfsJSON['Ipwb']['Replay']['Host']
        port = ipfsJSON['Ipwb']['Replay']['Port']
        return (host, port)
    else:
        return None


def setIPWBReplayConfig(Host, Port, ipfsJSON=None):
    if not ipfsJSON:
        ipfsJSON = readIPFSConfig()
    ipfsJSON['Ipwb'] = {}
    ipfsJSON['Ipwb']['Replay'] = {
      u'Host': Host,
      u'Port': Port
    }
    writeIPFSConfig(ipfsJSON)


''' # Unused
def getClosestCDXLine(surtURI, datetime):
    cdxlobj = getCDXLines(surtURI)
    mingap = float("inf")
    closest = None
    for cdxl in cdxlobj:
        gap = abs(int(datetime) - int(cdxl[1]))
        if gap < mingap:
            mingap = gap
            closest = cdxl
    return closest


def getCDXLines(surtURI):
    with open('index.cdx', 'r') as cdxFile:
        cdxlobj = []
        bsResp = iter_exact(cdxFile, surtURI)
        for cdxl in bsResp:
            (suri, dttm, jobj) = cdxl.split(' ', 2)
            if suri != surtURI:
                break
            cdxlobj.append((suri, dttm, jobj))
        return cdxlobj
'''
if __name__ == "__main__":
    hostPort = getIPWBReplayConfig()
    if not hostPort:
        setIPWBReplayConfig(IPWBREPLAY_IP, IPWBREPLAY_PORT)
        hostPort = getIPWBReplayConfig()
    # print hostPort
    # sys.exit()
    app.run(host=IPWBREPLAY_IP, port=IPWBREPLAY_PORT)

# Read in URI, convert to SURT
#  surt(uriIn)
# Get SURTed URI lines in CDXJ
#  Read CDXJ
#  Do bin search to find relevant lines

# read IPFS hash from relevant lines (header, payload)

# Fetch IPFS data at hashes
