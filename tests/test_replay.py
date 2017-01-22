import pytest
from ipwb import util

import testUtil as ipwbTest

# Successful retrieval
# Accurate retrieval
# Comprehensive retrieval of sub-resources


@pytest.mark.skip(reason='not implemented')
def test_retrieveWARCRecord_fromIPFSHash():
    pass


@pytest.mark.skip(reason='not implemented')
def test_retrieveWARCRecord_fromLocalCDXJFile():
    pass


@pytest.mark.skip(reason='not implemented')
def test_retrieveWARCRecord_fromRemoteCDXJFile_ByIPFSHash():
    pass


@pytest.mark.skip(reason='not implemented')
def test_retrieveWARCRecord_fromRemoteCDXJFile_ByHTTP():
    pass


@pytest.mark.skip(reason='not implemented')
def test_retrieveWARCRecord_fromRemoteCDXJFile_ByHTTPS():
    pass


@pytest.mark.skip(reason='not implemented')
def test_retrieveWARCRecord_fromRemoteCDXJFile_ByFTP():
    pass


@pytest.mark.skip(reason='not implemented')
def test_retrieveWARCRecord_fromRemoteCDXJFile_ByBitTorrentMagnetLink():
    pass


@pytest.mark.skip(reason='not implemented')
def test_retrieveWARCRecord_fromRemoteCDXJFile_BySMB():
    pass


@pytest.mark.skip(reason='not implemented')
def test_accuracy_retrievedContent_vsWARC():
    pass


@pytest.mark.skip(reason='not implemented')
def test_availability_subResources():
    pass


@pytest.mark.skip(reason='not implemented')
def test_inclusionInWebpage_selectResources():
    pass


@pytest.mark.skip(reason='not implemented')
def test_exclusionInWebpage_selectIrrelevantResources():
    pass


@pytest.mark.skip(reason='not implemented')
def test_fileImport_nonCDXJ():  # Fail w/ friendly message when non-cdxj
    pass


@pytest.mark.cdxjValidation
def test_cdxj_valid():
    # Missing fields
    assert not util.isValidCDXJ('test')
    # Valid SURT
    assert util.isValidCDXJ((
      r"""edu,odu,cs)/~salam 20160305192247 """
      r"""{"locator": "urn:ipfs/QmeVWGtnfuJ1QnpmtKKnyArVgEpq7v31kkt"""
      r"""Efh6c8mDiXE/QmZWKQRBNXNrVZ69LoGpMNJi5NU66gDhnGtQukWJepv7Kr", """
      r""""encryption_method": "xor", "encryption_key": "radon", """
      r""""mime_type": "text/html", "status_code": "200"}"""))
    # Bad JSON in third field
    assert not util.isValidCDXJ(r"""edu,odu,cs)/ 20160305192247 radon""")
    # Valid SURT
    assert util.isValidCDXJ(r"""edu,odu,cs)/ 20160305192247 {}""")
    # Invalid datetime
    assert not util.isValidCDXJ(r"""edu,odu,cs)/ 2016030519224 {}""")
    # Invalid SURT URI, pywb catches its own ValueError
    # assert not util.isValidCDXJ(r"""foo.bar 20160305192247 {}""")


# TODO: Have unit tests for each function in replay.py
