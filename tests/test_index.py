from unittest import mock

import pytest
from ipfshttpclient.exceptions import StatusError

from ipwb.index import fetch_web_archive_index
from pathlib import Path


SAMPLE_INDEX = str(
    Path(__file__).parent.parent / 'samples/indexes/salam-home.cdxj'
)


def test_local():
    assert fetch_web_archive_index(SAMPLE_INDEX).startswith(
        '!context ["http://tools.ietf.org/html/rfc7089"]'
    )


def test_https():
    assert fetch_web_archive_index(
        'https://raw.githubusercontent.com/oduwsdl/ipwb/master/samples/' +
        'indexes/salam-home.cdxj'
    ).startswith('!context ["http://tools.ietf.org/html/rfc7089"]')


def test_ipfs_success():
    with open(SAMPLE_INDEX, 'r') as f:
        expected_content = f.read()

    connect_to_ipfs = mock.MagicMock()
    connect_to_ipfs.return_value.cat.return_value = expected_content

    with mock.patch('ipfshttpclient.connect', connect_to_ipfs):
        assert fetch_web_archive_index(
            'QmReQCtRpmEhdWZVLhoE3e8bqreD8G3avGpVfcLD7r4K6W'
        ).startswith('!context ["http://tools.ietf.org/html/rfc7089"]')


def test_ipfs_failure():
    with pytest.raises(Exception):
        with mock.patch(
            'ipfshttpclient.client.Client.cat',
            side_effect=StatusError(original='')
        ):
            fetch_web_archive_index(
                'QmReQCtRpmEhdWZVLhoE3e8bqreD8G3avGpVfcLD7r4K6W',
            )
