import pytest

import testUtil as ipwbTest
from ipwb import replay
from time import sleep
import urllib2

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


@pytest.mark.skip(reason='not implemented')
def test_helpWithoutDaemon():  # See #244
    pass


@pytest.mark.ipfsDaemonStart
def test_unit_commandDaemon():
    replay.commandDaemon('start')
    sleep(10)
    try:
        urllib2.urlopen('http://localhost:5001')
    except urllib2.HTTPError, e:
        assert e.code == 404
    except Exception as e:
        assert False


@pytest.mark.parametrize("expected,input", [
    (True, 'http://example.com'),
    (True, 'https://example.com'),
    (True, 'HTTP://EXAMPLE.COM'),
    (True, 'HTTPS://EXAMPLE.COM'),
    (True, 'http://example.com/'),
    (True, 'http://example.com/foo.bar'),
    (True, 'https://www.example.com/foo?a=b&c=d'),
    (False, ''),
    (False, 'foo'),
    (False, 'foo/bar.baz'),
    (False, 'foo?a=b&c=d'),
    (False, '/'),
    (False, '/foo'),
    (False, '/foo/bar.baz'),
    (False, '/foo?a=b&c=d'),
    (False, './'),
    (False, './foo'),
    (False, './foo/bar.baz'),
    (False, './foo?a=b&c=d'),
    (False, '../'),
    (False, '../foo'),
    (False, '../foo/bar.baz'),
    (False, '../foo?a=b&c=d'),
    (False, '../../'),
    (False, '../../foo'),
    (False, '../../foo/bar.baz'),
    (False, '../../foo?a=b&c=d'),
    (False, 'ftp://example.com'),
    (False, 'httpd://example.com'),
    (False, 'http//example.com'),
    (False, 'http:/example.com'),
    (False, 'http:example.com'),
    (False, 'http.example.com'),
    (False, 'http-bin.com'),
])
def test_isUri(expected, input):
    assert expected == bool(replay.isUri(input))


# TODO: Have unit tests for each function in replay.py
