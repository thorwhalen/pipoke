"""Tests for :mod:`pipoke.distribution`.

Network-free coverage for ``json_package_info``, whose module docstring
example is ``# doctest: +SKIP``'d (pipoke#6) because it makes a real HTTPS
request to PyPI -- which must never gate CI (a PyPI outage or a
network-restricted runner would otherwise fail an unrelated release).
"""

from unittest.mock import Mock, patch

from pipoke.distribution import json_package_info


def test_json_package_info():
    fake_payload = {
        'info': {'name': 'ps', 'author': 'someone', 'version': '1.0'},
    }
    fake_response = Mock(status_code=200, **{'json.return_value': fake_payload})
    with patch('pipoke.distribution.requests.get', return_value=fake_response) as mocked_get:
        d = json_package_info('ps')
    mocked_get.assert_called_once()
    assert isinstance(d, dict)
    assert {'name', 'author', 'version'}.issubset(d['info'])


def test_json_package_info_returns_empty_dict_on_non_ok_status():
    fake_response = Mock(status_code=404)
    with patch('pipoke.distribution.requests.get', return_value=fake_response):
        assert json_package_info('a-package-that-does-not-exist-xyz') == {}
