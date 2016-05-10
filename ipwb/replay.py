#!/usr/bin/env python
# -*- coding: utf-8 -*-

from surt import surt
import sys
import ipfsApi
import json
from pywb.utils.binsearch import iter_exact
from pywb.utils.canonicalize import unsurt
from flask import Flask
from flask import Response

app = Flask(__name__)
app.debug = True
#@app.route("/")
#def hello():
#    return "Hello World!"
IP = '127.0.0.1'
PORT = '5001'
IPFS_API = ipfsApi.Client(IP, PORT)
INDEX_FILE = 'samples/indexes/sample-1.cdxj'


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def show_uri(path):
    global IPFS_API
    
    if len(path) == 0:
      with open('index.html','r') as indexFile:
        html = indexFile.read()
        html = html.replace('MEMCOUNT', str(retrieveMemCount()))
        html = html.replace('var uris = []', 'var uris = ' + getURIsInCDXJ())
        return Response(html)
        sys.exit()
    #(datetime, urir) = path.split('/', 1)
    urir = path
    
    # show the user profile for that user
    cdxLine = ''
    try:
      cdxLine = getCDXLine(surt(path))
    except:
      return Response(path+ ' not found :( <a href="http://localhost:5000">Go home</a>')
    cdxParts = cdxLine.split(" ", 2)
    surtURI = cdxParts[0]
    datetime = cdxParts[1]
    jObj = json.loads(cdxParts[2])
    
    payload = IPFS_API.cat(jObj['payload_digest'])
    header = IPFS_API.cat(jObj['header_digest'])

    #print header
    #print payload
    hLines = header.split('\n')
    hLines.pop(0)
    
    resp = Response(payload)

    for idx,hLine in enumerate(hLines):
      k,v = hLine.split(': ', 1)
      if k.lower() != "content-type":
        k = "X-Archive-Orig-" + k
      resp.headers[k] = v
      
    
    return resp

def getURIsInCDXJ(cdxjFile = INDEX_FILE):
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

    

if __name__ == "__main__":
    app.run()
    
# Read in URI, convert to SURT
  #surt(uriIn)
# Get SURTed URI lines in CDXJ
#  Read CDXJ
#  Do bin search to find relevant lines

# read IPFS hash from relevant lines (header, payload)

# Fetch IPFS data at hashes


if __name__ == '__main__':
  main()  