# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
import os

import pytest

from dotenv import load_dotenv

# Import fixtures from our package so pytest can detect them
from fixtures.base import chrome_options, selenium # flake8: noqa
from fixtures.snapshot import snapshot
from fixtures.archive import archive_base_url
from fixtures.webview import american_gov_url, content_url
from fixtures.legacy import (legacy_base_url, legacy_username, legacy_password,
                             m46922_1_13_cnxml_filepath)
from tests.utils import patch_module

# Load environment variables from .env file
DOTENV_PATH = os.path.join(
  os.path.realpath(os.path.dirname(__file__)), '../.env')
load_dotenv(dotenv_path=DOTENV_PATH)

# Patch remote_connection to workaround Connection Reset by Peer bug in the Selenium driver
patch_module('patches.remote_connection',
             'selenium.webdriver.remote.remote_connection',
             '__init__')


def pytest_addoption(parser):
    group = parser.getgroup('selenium', 'selenium')
    group.addoption('--disable-dev-shm-usage',
                    action='store_true',
                    default=os.getenv('DISABLE_DEV_SHM_USAGE', False),
                    help="disable chrome's usage of /dev/shm.")
    group.addoption('--headless',
                    action='store_true',
                    default=os.getenv('HEADLESS', False),
                    help='enable headless mode for chrome.')
    group.addoption('--no-sandbox',
                    action='store_true',
                    default=os.getenv('NO_SANDBOX', False),
                    help="disable chrome's sandbox.")
    group.addoption('--print-page-source-on-failure',
                    action='store_true',
                    default=os.getenv('PRINT_PAGE_SOURCE_ON_FAILURE', False),
                    help='print page source to stdout when a test fails.')
    parser.addoption('--runslow',
                     action='store_true',
                     default=os.getenv('RUNSLOW', False),
                     help='run slow tests')
    # Adapted from:
    # https://github.com/pytest-dev/pytest-base-url/blob/master/pytest_base_url/plugin.py#L51
    parser.addini('archive_base_url', help='base url for CNX archive.')
    parser.addoption(
        '--archive_base_url',
        metavar='url',
        default=os.getenv('ARCHIVE_BASE_URL', None),
        help='base url for CNX archive.')
    parser.addini('legacy_base_url', help='base url for CNX legacy.')
    parser.addoption(
        '--legacy_base_url',
        metavar='url',
        default=os.getenv('LEGACY_BASE_URL', None),
        help='base url for CNX legacy.')
    parser.addoption(
        '--legacy_username',
        default=os.getenv('LEGACY_USERNAME'),
        help='username for CNX legacy.')
    parser.addoption(
        '--legacy_password',
        default=os.getenv('LEGACY_PASSWORD'),
        help='password for CNX legacy.')


# https://docs.pytest.org/en/latest/example/simple.html#making-test-result-information-available-in-fixtures
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # execute all other hooks to obtain the report object
    outcome = yield
    rep = outcome.get_result()

    # set a report attribute for each phase of a call, which can be "setup", "call", "teardown"
    # can be used by yield fixtures to determine if the test failed (see selenium fixture)
    setattr(item, 'rep_{when}'.format(when=rep.when), rep)
