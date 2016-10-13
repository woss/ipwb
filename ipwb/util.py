from os.path import expanduser
import json
import requests
from requests.exceptions import ConnectionError

IPFSAPI_IP = '127.0.0.1'
IPFSAPI_PORT = 5001
IPWBREPLAY_IP = '127.0.0.1'
IPWBREPLAY_PORT = 5000

INDEX_FILE = 'samples/indexes/sample-2.cdxj'


def isDaemonAlive(hostAndPort="{0}:{1}".format(IPFSAPI_IP, IPFSAPI_PORT)):
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
