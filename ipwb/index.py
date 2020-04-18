import os
import sys
from functools import lru_cache

from ipfshttpclient.exceptions import StatusError as hashNotInIPFS

from ipwb import util

IPFS_API = util.createIPFSClient()


def fetch_remote_index_file_contents(path) -> str:
    """Fetch CDXJ file from IPFS."""
    path = path.replace('ipfs://', '')
    # TODO: Take into account /ipfs/(hash), first check if this is correct fmt

    if '://' not in path:  # isAIPFSHash
        # TODO: Check if a valid IPFS hash
        print('No scheme in path, assuming IPFS hash and fetching...')
        try:
            print("Trying to ipfs.cat('{0}')".format(path))
            data_from_ipfs = IPFS_API.cat(path)

        except hashNotInIPFS:
            print(("The CDXJ at hash {0} could"
                   " not be found in IPFS").format(path))
            sys.exit()

        print('Data successfully obtained from IPFS')
        return data_from_ipfs.decode('utf-8')
    else:  # http://, ftp://, smb://, file://
        print('Path contains a scheme, fetching remote file...')
        file_contents = util.fetch_remote_file(path)
        return file_contents

    # TODO: Check if valid CDXJ here before returning


def get_index_file_contents(path=util.INDEX_FILE) -> str:
    """Fetch CDXJ file from local disk or IPFS, depending on the path."""
    if not os.path.exists(path):
        print('File {0} does not exist locally, fetching remote'.format(path))
        return fetch_remote_index_file_contents(path) or ''

    index_file_path = path.replace('ipwb.replay', 'ipwb')
    print('getting index file at {0}'.format(index_file_path))

    with open(path, 'r') as f:
        index_file_content = f.read()

    return index_file_content


@lru_cache()
def get_cached_index_file_contents(path: str) -> str:
    """Store index file content in memory after first fetch."""
    return get_index_file_contents(path)
