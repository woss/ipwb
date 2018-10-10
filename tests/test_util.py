import pytest

from ipwb import util


@pytest.mark.parametrize('expected,input', [
    ('', ''),
    ('foo', 'foo'),
    ('18', '18'),
    ('20181', '20181'),
    ('20181126134257.123', '20181126134257.123'),
    ('20180101000000', '2018'),
    ('20181101000000', '201811'),
    ('20181126000000', '20181126'),
    ('20181126130000', '2018112613'),
    ('20181126134200', '201811261342'),
    ('20181126134257', '20181126134257'),
])
def test_padDigits14(expected, input):
    assert expected == util.padDigits14(input)


@pytest.mark.parametrize('input', [
    '',
    'foo',
    '18',
    '20181',
    '201800',
    '20180132',
    '2018010226',
    '20180102263127',
    '20181126134257.123',
])
def test_padDigits14_inalid(input):
    with pytest.raises(ValueError):
        util.padDigits14(input, validate=True)
