import functools
import os

import ipfshttpclient
from ipfshttpclient.exceptions import StatusError

from ipwb import util


def _fetch_index_file_from_ipfs(path: str) -> str:
    """Fetch CDXJ file from IPFS."""
    path = path.replace('ipfs://', '')
    # TODO: Take into account /ipfs/(hash), first check if this is correct fmt

    if '://' not in path:  # isAIPFSHash
        # TODO: Check if a valid IPFS hash
        print('No scheme in path, assuming IPFS hash and fetching...')
        try:
            print("Trying to ipfs.cat('{0}')".format(path))
            with ipfshttpclient.connect(util.IPFSAPI_MUTLIADDRESS) as client:
                return client.cat(path).decode('utf-8')

        except StatusError as err:
            raise Exception((
                'Cannot find CDXJ index file by hash {hash} in IPFS.'
            ).format(
                hash=path,
            )) from err

    # TODO should be refactored into another function
    else:  # http://, ftp://, smb://, file://
        print('Path contains a scheme, fetching remote file...')
        return util.fetch_remote_file(path)

    # TODO: Check if valid CDXJ here before returning


def fetch_web_archive_index(path: str = util.INDEX_FILE) -> str:
    """Fetch CDXJ file from local disk or IPFS, depending on the path."""
    if not os.path.exists(path):
        print('File {0} does not exist locally, fetching remote'.format(path))
        return _fetch_index_file_from_ipfs(path) or ''

    index_file_path = path.replace('ipwb.replay', 'ipwb')
    print('getting index file at {0}'.format(index_file_path))

    with open(path, 'r') as f:
        return f.read()


@functools.lru_cache()
def get_web_archive_index(path: str) -> str:
    """
    Store index file content in memory after first fetch.
    Helps avoid redundant network calls.
    """
    return fetch_web_archive_index(path)
