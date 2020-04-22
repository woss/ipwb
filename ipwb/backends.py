import os

import ipfshttpclient
from ipfshttpclient.exceptions import StatusError

from ipwb import util


def fetch_remote_index(path: str) -> str:
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


def fetch_local_index(path: str) -> str:
    """Fetch CDXJ index contents from a file on local disk."""
    # TODO what does this mean?
    index_file_path = path.replace('ipwb.replay', 'ipwb')

    print('getting index file at {0}'.format(index_file_path))

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
