import pytest


def pytest_addoption(parser):
    group = parser.getgroup('selenium', 'selenium')
    group._addoption('--headless',
                     action='store_true',
                     help='enable headless mode for chrome.')


@pytest.fixture
def chrome_options(chrome_options, pytestconfig):
    if pytestconfig.getoption('headless'):
        chrome_options.add_argument('--headless')
    return chrome_options


@pytest.fixture
def selenium(selenium):
    selenium.implicitly_wait(0)
    return selenium
