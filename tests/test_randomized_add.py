import pytest
import random
import os
import sys
import string
import json

from ipwb import indexer


def func(x):
    return x


def countCDXJFields(cdxjEntry):
    return len(cdxjEntry.split(' '))
    
    
def countCDXJEntries(cdxjData):
    return len(cdxjData.split('\n'))


def checkIPWBJSONFieldPresesence(jsonStr):
    keys = json.loads(jsonStr)
    return 'locator' in keys and 'mime_type' in keys and 'status_code' in keys

def getRandomString(n):
    return ''.join(random.SystemRandom().choice(
                   string.ascii_lowercase + string.digits) for _ in range(n))


def createUniqueWARC():
    lines = []
    warcInFilename = 'frogTest.warc'
    warcInPath = os.path.join(os.path.dirname(__file__) + '/samples/warcs/' +
                              warcInFilename)

    stringToChange = 'abcdefghijklmnopqrstuvwxz'
    randomString = getRandomString(len(stringToChange))

    with open(warcInPath, 'r') as warcFile:
        newContent = warcFile.read().replace(stringToChange, randomString)

    warcOutFilename = warcInFilename.replace('.warc', '_' +
                                             randomString + '.warc')
    warcOutPath = os.path.join(os.path.dirname(__file__) +
                               '/samples/warcs/' + warcOutFilename)
    with open(warcOutPath, 'w') as warcFile:
        warcFile.write(newContent)

    return warcOutPath


def test_push():
    """
    Read WARC, manipulate content to ensure uniqueness, push to IPFS
      WARC should result in two CDXJ entries with three space-limited fields
      each: surt URI, datetime, JSON
      JSON should contain AT LEAST locator, mime_type, and status fields
    """
    newWARCPath = createUniqueWARC()
    # use ipwb indexer to push
    cdxj = indexer.indexFileAt(newWARCPath)  # Currently goes to stdout

    # We need to test the response, namely:
    # * Valid CDXJ
    # * Fields are unique to newly generated file (maybe need to refetch)
    # * ...
    assert countCDXJEntries(cdxj) == 2
    firstEntry = cdxj.split('\n')[0]
    assert countCDXJFields(firstEntry) == 3
    firstEntryLastField = firstEntry.split(' ')[-1]
    assert checkIPWBJSONFieldPresesence(firstEntryLastField)
