import pytest

__all__ = ['legacy_base_url', 'legacy_username', 'legacy_password']


@pytest.fixture(scope='session')
def legacy_base_url(request):
    """Return a base URL for legacy"""
    config = request.config
    base_url = (config.getoption('legacy_base_url') or
                config.getini('legacy_base_url'))
    if base_url is not None:
        return base_url


@pytest.fixture(scope='session')
def legacy_username(request):
    """Return a username for legacy"""
    config = request.config
    username = config.getoption('legacy_username')
    if username is not None:
        return username


@pytest.fixture(scope='session')
def legacy_password(request):
    """Return a password for legacy"""
    config = request.config
    password = config.getoption('legacy_password')
    if password is not None:
        return password
