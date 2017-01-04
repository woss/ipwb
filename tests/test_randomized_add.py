import pytest
import random
import os
import sys
import string

from ipwb import indexer


def func(x):
    return x


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
    """
    newWARCPath = createUniqueWARC()
    # use ipwb indexer to push
    indexer.indexFileAt(newWARCPath)  # Currently goes to stdout

    # We need to test the response, namely:
    # * Valid CDXJ
    # * Fields are unique to newly generated file (maybe need to refetch)
    # * ...
    assert func(42) == 55
