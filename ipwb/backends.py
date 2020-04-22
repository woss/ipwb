import os
from urllib.parse import urlparse

import ipfshttpclient
import requests

from ipwb import util


def fetch_ipfs_index(path: str) -> str:
    """Fetch CDXJ file content from IPFS by hash."""
    with ipfshttpclient.connect(util.IPFSAPI_MUTLIADDRESS) as client:
        return client.cat(path).decode('utf-8')


def fetch_web_index(path: str) -> str:
    """Fetch CDXJ file content from a URL."""
    return requests.get(path).text


def fetch_remote_index(path: str) -> str:
    """Fetch CDXJ file content from a remote location."""

    if path.startswith('Qm'):
        return fetch_ipfs_index(path)

    scheme = urlparse(path).scheme

    if scheme == 'ipfs':
        return fetch_ipfs_index(path.replace('ipfs://', ''))

    elif scheme:
        return fetch_web_index(path)


def fetch_local_index(path: str) -> str:
    """Fetch CDXJ index contents from a file on local disk."""
    with open(path, 'r') as f:
        return f.read()


def get_web_archive_index(path: str) -> str:
    """
    Based on path, choose appropriate backend and fetch the file contents.
    """

    # TODO right now, every backend is just a function which returns contents
    #   of a CDXJ file as string. In the future, however, backends will be
    #   probably represented as classes with much more sophisticated methods
    #   of manipulating the archive index records.
    # TODO also, it will be possible to choose a backend and configure it;
    #   whereas right now we choose a backend automatically based on the given
    #   path itself.

    if os.path.exists(path):
        return fetch_local_index(path)

    else:
        return fetch_remote_index(path)
