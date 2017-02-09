from os.path import expanduser
from os.path import basename
from os import devnull
import json
import sys
import requests
import ipfsapi
import exceptions
import subprocess
import site
# from requests.exceptions import ConnectionError
from ipfsapi.exceptions import ConnectionError


IPFSAPI_IP = '127.0.0.1'
IPFSAPI_PORT = 5001
IPWBREPLAY_IP = '127.0.0.1'
IPWBREPLAY_PORT = 5000

INDEX_FILE = 'samples/indexes/sample-encrypted.cdxj'
SAMPLE_WARC = 'samples/warcs/salam-home.warc'


def isDaemonAlive(hostAndPort="{0}:{1}".format(IPFSAPI_IP, IPFSAPI_PORT)):
    """Ensure that the IPFS daemon is running via HTTP before proceeding"""
    client = ipfsapi.Client(IPFSAPI_IP, IPFSAPI_PORT)

    try:
        # OSError if ipfs not installed
        subprocess.call(['ipfs', '--version'], stdout=open(devnull, 'wb'))

        # ConnectionError if IPFS daemon not running
        client.id()
        return True
    except ConnectionError:
        print "Daemon is not running at http://" + hostAndPort
        return False
    except OSError:
        print "IPFS is likely not installed. See https://ipfs.io/docs/install/"
        sys.exit()
    except:
        print 'Unknown error in retrieving daemon status'
        print sys.exc_info()[0]


def isValidCDXJ(stringIn):  # TODO: Check specific strict syntax
    # Also, be sure to mind the meta headers starting with @/#, etc.
    return True


def retrieveMemCount():
    with open(INDEX_FILE, 'r') as cdxFile:
        for i, l in enumerate(cdxFile):
            pass
        return i+1


def fetchRemoteFile(path):
    try:
        r = requests.get(path)
        return r.text
    except ConnectionError:
        print 'File at {0} is unavailable.'.format(path)
    except:
        print 'An unknown error occurred trying to fetch {0}'.format(path)
        print sys.exc_info()[0]
    return None


def getCDXLine(surtURI):
    with open(INDEX_FILE, 'r') as cdxFile:
        bsResp = iter_exact(cdxFile, surtURI)
        cdxLine = bsResp.next()
        return cdxLine


# IPFS Config manipulation from here on out.
def readIPFSConfig():
    try:
        with open(expanduser("~") + '/.ipfs/config', 'r') as f:
            return json.load(f)
    except IOError:
        print "IPFS config not found."
        print "Have you installed ipfs and run ipfs init?"
        sys.exit()


def writeIPFSConfig(jsonToWrite):
    with open(expanduser("~") + '/.ipfs/config', 'w') as f:
        f.write(json.dumps(jsonToWrite, indent=4, sort_keys=True))


def getIPFSAPIHostAndPort(ipfsJSON=None):
    if not ipfsJSON:
        ipfsJSON = readIPFSConfig()

    (scheme, host, protocol, port) = (
        ipfsJSON['Addresses']['API'][1:].split('/')
    )
    return host + ':' + port


def getIPFSAPIPort(ipfsJSON=None):
    if not ipfsJSON:
        ipfsJSON = readIPFSConfig()
    ipfsAPIPort = basename(ipfsJSON['Addresses']['API'])


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


def setIPWBReplayIndexPath(cdxj):
    if cdxj is None:
        cdxj = INDEX_FILE
    ipfsJSON = readIPFSConfig()
    ipfsJSON['Ipwb']['Replay']['Index'] = cdxj
    writeIPFSConfig(ipfsJSON)
    return


def getIPWBReplayIndexPath():
    ipfsJSON = readIPFSConfig()
    if 'Index' in ipfsJSON['Ipwb']['Replay']:
        return ipfsJSON['Ipwb']['Replay']['Index']
    else:
        return ''


def firstRun():
    import indexer
    # Ensure the sample WARC is in IPFS
    print 'Executing first-run procedure on provided sample data.'
    indexer.indexFileAt(site.getsitepackages()[0] + '/ipwb/' + SAMPLE_WARC,
                                                    'radon', quiet=True)
