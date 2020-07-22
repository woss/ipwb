# Number of entries in CDXJ == number of response records in WARC

import pytest
from . import testUtil as ipwbTest
import os

from ipwb import indexer

from pathlib import Path


def test_cdxj_warc_responserecord_count():
    new_warc_path = ipwbTest.createUniqueWARC()
    # use ipwb indexer to push
    cdxjList = indexer.index_file_at(new_warc_path, quiet=True)
    cdxj = '\n'.join(cdxjList)
    assert ipwbTest.countCDXJEntries(cdxj) == 2


# A response record's content-length causes the payload to truncate
# WARC-Response record for html should still exist in output
def test_warc_ipwbIndexerBrokenWARCRecord():
    pathOfBrokenWARC = os.path.join(
        Path(os.path.dirname(__file__)).parent,
        'samples', 'warcs', 'broken.warc')
    cdxjList = indexer.index_file_at(pathOfBrokenWARC, quiet=True)
    cdxj = '\n'.join(cdxjList)
    assert ipwbTest.countCDXJEntries(cdxj) == 1


# TODO: Have unit tests for each function in indexer.py
