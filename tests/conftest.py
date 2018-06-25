# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
import os

import pytest

from dotenv import load_dotenv

# Patch remote_connection to workaround Connection Reset by Peer bug in the Selenium driver
# https://github.com/SeleniumHQ/selenium/issues/5296
from patches import connection_reset_by_peer  # noqa

# Import fixtures
pytest_plugins = (
    'fixtures.base',
    'fixtures.github',
    'fixtures.snapshot',
    'fixtures.archive',
    'fixtures.webview',
    'fixtures.legacy',
    'fixtures.neb'
)

# Load environment variables from .env file
DOTENV_PATH = os.path.join(os.path.realpath(os.path.dirname(__file__)), '../.env')
load_dotenv(dotenv_path=DOTENV_PATH)


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
    parser.addini('webview_base_url', help='base url for CNX webview.')
    parser.addoption(
        '--webview_base_url',
        metavar='url',
        default=os.getenv('WEBVIEW_BASE_URL', None),
        help='base url for CNX webview.')
    parser.addoption(
        '--legacy_username',
        default=os.getenv('LEGACY_USERNAME'),
        help='username for CNX legacy.')
    parser.addoption(
        '--legacy_password',
        default=os.getenv('LEGACY_PASSWORD'),
        help='password for CNX legacy.')
    parser.addini('neb_env', help='environment name for Neb.')
    parser.addoption(
        '--neb_env',
        default=os.getenv('NEB_ENV', None),
        help='environment name for Neb.')


# https://docs.pytest.org/en/latest/example/simple.html#making-test-result-information-available-in-fixtures
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # execute all other hooks to obtain the report object
    outcome = yield
    rep = outcome.get_result()

    # set a report attribute for each phase of a call, which can be "setup", "call", "teardown"
    # can be used by yield fixtures to determine if the test failed (see selenium fixture)
    setattr(item, 'rep_{when}'.format(when=rep.when), rep)


@pytest.hookimpl(hookwrapper=True)
def pytest_terminal_summary(terminalreporter):
    yield

    for report in terminalreporter.getreports(''):
        if report.when == 'teardown':
            for (name, value) in report.user_properties:
                if name == 'terminal_summary_message':
                    print(value)
