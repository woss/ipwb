# Number of entries in CDXJ == number of response records in WARC

import pytest
from . import testUtil as ipwbTest
import os

from ipwb import indexer


@pytest.mark.ipwbIndexerRecordCount
def test_cdxj_warc_responseRecordCount():
    newWARCPath = ipwbTest.createUniqueWARC()
    # use ipwb indexer to push
    cdxjList = indexer.indexFileAt(newWARCPath, quiet=True)
    cdxj = '\n'.join(cdxjList)
    assert ipwbTest.countCDXJEntries(cdxj) == 2


# A response record's content-length causes the payload to truncate
# WARC-Response record for html should still exist in output
@pytest.mark.ipwbIndexerBrokenWARCRecord
def test_warc_ipwbIndexerBrokenWARCRecord():
    pathOfBrokenWARC = os.path.join(os.path.dirname(__file__) +
                                    '/../samples/warcs/broken.warc')
    cdxjList = indexer.indexFileAt(pathOfBrokenWARC, quiet=True)
    cdxj = '\n'.join(cdxjList)
    assert ipwbTest.countCDXJEntries(cdxj) == 1


# WARC/1.1 allows for dates of length that are not easily converted
# to 14-digits. This test highlights the failures from a WARC
# exhibiting these dates.
@pytest.mark.ipwbIndexerVariableSizedDates
def test_warc_ipwbIndexerVariableSizedDates():
    pathOfBrokenWARC = \
        os.path.normpath(os.path.join(os.path.dirname(__file__), '..',
                         'samples', 'warcs', 'variableSizedDates.warc'))
    indexer.indexFileAt(pathOfBrokenWARC, quiet=True)

# TODO: Have unit tests for each function in indexer.py
