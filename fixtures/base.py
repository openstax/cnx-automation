# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

__all__ = ['selenium', 'chrome_options']


@pytest.fixture
def selenium(selenium):
    selenium.implicitly_wait(0)
    return selenium


@pytest.fixture
def chrome_options(chrome_options, pytestconfig):
    if pytestconfig.getoption('--headless'):
        chrome_options.headless = True

    # Required to run in Travis containers
    if pytestconfig.getoption('--no-sandbox'):
        chrome_options.add_argument('--no-sandbox')
    if pytestconfig.getoption('--disable-dev-shm-usage'):
        chrome_options.add_argument('--disable-dev-shm-usage')

    # This ensures the tests will still pass for someone who selected
    # a language other than English as their preferred language in Chrome
    chrome_options.add_argument('--lang=en')

    return chrome_options
