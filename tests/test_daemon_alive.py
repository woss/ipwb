from unittest.mock import MagicMock, patch

import pytest

from ipwb.util import check_daemon_is_alive


def test_is_alive():
    ipfs_client = MagicMock()

    with patch('ipwb.util.ipfs_client', ipfs_client):
        assert check_daemon_is_alive() is True


def test_os_error():
    ipfs_client = MagicMock()
    ipfs_client.return_value.id.side_effect = OSError('foo!')

    with patch('ipwb.util.ipfs_client', ipfs_client):
        with pytest.raises(Exception, match='IPFS is likely not installed'):
            check_daemon_is_alive()


def test_unknown_error():
    ipfs_client = MagicMock()
    ipfs_client.return_value.id.side_effect = Exception('foo!')
    expected_error = 'Unknown error in retrieving IPFS daemon status.'

    with patch('ipwb.util.ipfs_client', ipfs_client):
        with pytest.raises(Exception, match=expected_error):
            check_daemon_is_alive()
