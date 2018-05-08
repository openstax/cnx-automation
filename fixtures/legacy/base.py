import pytest

__all__ = [ 'legacy_base_url' ]


@pytest.fixture(scope='session')
def legacy_base_url(request):
    """Return a base URL for legacy"""
    config = request.config
    base_url = config.getoption('legacy_base_url') or \
               config.getini('legacy_base_url')
    if base_url is not None:
        return base_url
