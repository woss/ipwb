import pytest
import os
import sys
import json

from ipwb import indexer

import testUtil as ipwbTest


def isValidSURT(surt):
    return True  # The surt library does not yet have a way to check this


def isValidDatetime(dt):
    return len(dt) == 14 and dt.isdigit()


def isValidJSON(jsonIn):
    try:
        j = json.loads(json.dumps(jsonIn))
    except ValueError:
        return False
    return True


def checkCDXJFields(cdxjEntry):
    (surt, dt, json) = cdxjEntry.split(' ', 2)
    validSURT = isValidSURT(surt)
    validDT = isValidDatetime(dt)
    validJSON = isValidJSON(json)

    return validSURT and validDT and validJSON


def countCDXJEntries(cdxjData):
    return len(cdxjData.strip().split('\n'))


def checkIPWBJSONFieldPresesence(jsonStr):
    keys = json.loads(jsonStr)
    return 'locator' in keys and 'mime_type' in keys and 'status_code' in keys


def test_push():
    """
    Read WARC, manipulate content to ensure uniqueness, push to IPFS
      WARC should result in two CDXJ entries with three space-limited fields
      each: surt URI, datetime, JSON
      JSON should contain AT LEAST locator, mime_type, and status fields
    """
    newWARCPath = ipwbTest.createUniqueWARC()
    # use ipwb indexer to push
    cdxj = indexer.indexFileAt(newWARCPath, quiet=True)

    assert countCDXJEntries(cdxj) == 2
    firstEntry = cdxj.split('\n')[0]
    assert checkCDXJFields(firstEntry)
    firstEntryLastField = firstEntry.split(' ', 2)[2]
    assert checkIPWBJSONFieldPresesence(firstEntryLastField)
