# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os

import pytest

from pages.legacy.home import Home
from pages.legacy.dashboard import Dashboard
from pages.legacy.login_page import LoginPage


@pytest.mark.slow
@pytest.mark.nondestructive
def test_home_login(legacy_base_url, selenium):
    # GIVEN the legacy homepage
    page = Home(selenium, legacy_base_url).open()

    # WHEN we login
    username = os.environ['USERNAME']
    page = page.login(username, os.environ['PASSWORD'])

    # THEN the user is logged in (at their dashboard)
    # and the correct username is displayed
    assert type(page) is Dashboard
    assert page.username == username


@pytest.mark.slow
@pytest.mark.nondestructive
def test_home_login_logout(legacy_base_url, selenium):
    # GIVEN the legacy homepage
    page = Home(selenium, legacy_base_url).open()

    # WHEN we login, then logout
    username = os.environ['USERNAME']
    page = page.login(username, os.environ['PASSWORD'])
    page = page.logout()

    # THEN the user is logged out (at the login form page)
    assert type(page) is LoginPage


@pytest.mark.slow
@pytest.mark.nondestructive
def test_login_page_login(legacy_base_url, selenium):
    # GIVEN the legacy login form page
    page = LoginPage(selenium, legacy_base_url).open()

    # WHEN we login
    username = os.environ['USERNAME']
    page = page.login(username, os.environ['PASSWORD'])

    # THEN the user is logged in (at their dashboard)
    # and the correct username is displayed
    assert type(page) is Dashboard
    assert page.username == username


@pytest.mark.slow
@pytest.mark.nondestructive
def test_login_page_login_logout(legacy_base_url, selenium):
    # GIVEN the legacy login form page
    page = LoginPage(selenium, legacy_base_url).open()

    # WHEN we login, then logout
    username = os.environ['USERNAME']
    page = page.login(username, os.environ['PASSWORD'])
    page = page.logout()

    # THEN the user is logged out (at the login form page)
    assert type(page) is LoginPage
