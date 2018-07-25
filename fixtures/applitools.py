import pytest
from applitools.eyes import Eyes


@pytest.fixture(scope='session')
def applitools_api_key(request):
    """Return an instantiated Eyes object for applitools integration"""
    config = request.config
    applitools_api_key = config.getoption('applitools_api_key')
    if applitools_api_key is not None:
        return applitools_api_key


@pytest.fixture
def applitools(applitools_api_key):
    eyes = Eyes()
    eyes.api_key = applitools_api_key
    return eyes
