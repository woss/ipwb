import pytest
import os
import sys
import json

from ipwb import indexer

from . import testUtil as ipwbTest


def is_valid_surt(surt):
    return True  # The surt library does not yet have a way to check this


def is_valid_datetime(dt):
    return len(dt) == 14 and dt.isdigit()


def is_valid_json(jsonIn):
    try:
        j = json.loads(json.dumps(jsonIn))
    except ValueError:
        return False
    return True


def check_cdxj_fields(cdxjEntry):
    (surt, dt, json) = cdxjEntry.split(' ', 2)
    valid_surt = is_valid_surt(surt)
    valid_dt = is_valid_datetime(dt)
    valid_json = is_valid_json(json)

    return valid_surt and valid_dt and valid_json


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
    new_warc_path = ipwbTest.createUniqueWARC()
    # use ipwb indexer to push
    cdxjList = indexer.index_file_at(new_warc_path, quiet=True)
    cdxj = '\n'.join(cdxjList)

    firstEntry = cdxj.split('\n')[0]
    firstNonMetadataEntry = ''
    for line in cdxj.split('\n'):
        if line[0] != '!':
            firstNonMetadataEntry = line
            break

    assert check_cdxj_fields(firstNonMetadataEntry)
    firstEntryLastField = firstNonMetadataEntry.split(' ', 2)[2]
    assert checkIPWBJSONFieldPresesence(firstEntryLastField)
