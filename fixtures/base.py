import pytest

__all__ = ['selenium', 'chrome_options']


@pytest.fixture
def selenium(selenium):
    selenium.implicitly_wait(0)
    return selenium


@pytest.fixture
def chrome_options(chrome_options, pytestconfig):
    if pytestconfig.getoption('headless'):
        chrome_options.add_argument('--headless')
    return chrome_options
