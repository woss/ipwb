import logging
import re

import requests

from ipwb import __version__ as ipwb_version

logger = logging.getLogger(__name__)


def get_latest_ipwb_version() -> str:
    """Fetch latest IPWB version from PyPI."""
    response = requests.get('https://pypi.python.org/pypi/ipwb/json').json()
    return response['info']['version']


def check_pypi_for_update():
    """Check if IPWB is outdated and print out a message if it is."""
    latest = get_latest_ipwb_version()
    current = re.sub(r'\.0+', '.', ipwb_version)

    if current != latest and current is not None:
        logger.warning(
            'This version of ipwb is outdated. ' +
            'Please run:\n\n' +
            '   pip install --upgrade ipwb\n\n'
            '* Latest version: %s\n' +
            '* Installed version: %s',
            latest, current
        )
