# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os

import pytest

from tests.utils import gen_from_file

DATA_DIR = os.path.join(os.path.realpath(os.path.dirname(__file__)), 'data')


def pytest_addoption(parser):
    group = parser.getgroup('selenium', 'selenium')
    group._addoption('--headless',
                     action='store_true',
                     help='enable headless mode for chrome.')
    parser.addoption('--runslow', action='store_true',
                     default=False, help='run slow tests')

def pytest_collection_modifyitems(config, items):
    if config.getoption('--runslow'):
        # --runslow given in cli: do not skip slow tests
        return
    skip_slow = pytest.mark.skip(reason='need --runslow option to run')
    for item in items:
        if 'slow' in item.keywords:
            item.add_marker(skip_slow)

@pytest.fixture
def chrome_options(chrome_options, pytestconfig):
    if pytestconfig.getoption('headless'):
        chrome_options.add_argument('--headless')
    return chrome_options


@pytest.fixture
def selenium(selenium):
    selenium.implicitly_wait(0)
    return selenium


@pytest.fixture
def content_url(base_url):
    """Creates contents URL based on the base_url

    Example: https://qa.cnx.org/contents
    """
    return '{0}/{1}'.format(base_url, 'contents')


@pytest.fixture(params=gen_from_file(os.path.join(DATA_DIR, 'american_gov_uuids.txt')))
def american_gov_url(content_url, request):
    """Creates an American Government URL based on the content_url fixture and a UUID

    Example: https://qa.cnx.org/contents/c6ee95dd-d10b-430c-8a83-20d5a28334a9
    """
    yield '{0}/{1}'.format(content_url, request.param)
