from unittest import mock

from ipwb import check_for_update


def test_get_latest_ipwb_version():
    requests_get = mock.MagicMock()
    requests_get.return_value.json.return_value = {
        'info': {
            'version': 'foo!'
        }
    }

    with mock.patch('requests.get', requests_get):
        assert check_for_update.get_latest_ipwb_version() == 'foo!'


def test_check_pypi_for_update():
    get_latest_ipwb_version = mock.MagicMock()
    get_latest_ipwb_version.return_value = 'foo!'

    logger = mock.MagicMock()

    with mock.patch.multiple(
        check_for_update,
        get_latest_ipwb_version=get_latest_ipwb_version,
        ipwb_version='bar!',
        logger=logger,
    ):
        check_for_update.check_pypi_for_update()

    logger.warning.assert_called_once_with(
        'This version of ipwb is outdated. Please run:\n\n' +
        '   pip install --upgrade ipwb\n\n' +
        '* Latest version: %s\n' +
        '* Installed version: %s',
        'foo!',
        'bar!',
    )
