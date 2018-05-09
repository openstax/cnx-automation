# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from tests import markers

from pages.legacy.home import Home
from pages.legacy.dashboard import Dashboard
from pages.legacy.login_page import LoginPage


@markers.legacy
@markers.slow
@markers.nondestructive
def test_home_login(legacy_base_url, legacy_username,
                    legacy_password, selenium):
    # GIVEN the legacy homepage
    home = Home(selenium, legacy_base_url).open()

    # WHEN we login
    dashboard = home.login(legacy_username, legacy_password)

    # THEN the user is logged in (at their dashboard)
    # and the correct username is displayed
    assert type(dashboard) is Dashboard
    assert dashboard.username == legacy_username


@markers.legacy
@markers.slow
@markers.nondestructive
def test_home_login_logout(legacy_base_url, legacy_username,
                           legacy_password, selenium):
    # GIVEN the legacy homepage
    home = Home(selenium, legacy_base_url).open()

    # WHEN we login, then logout
    dashboard = home.login(legacy_username, legacy_password)
    login_page = dashboard.logout()

    # THEN the user is logged out (at the login form page)
    assert type(login_page) is LoginPage


@markers.legacy
@markers.slow
@markers.nondestructive
def test_login_page_login(legacy_base_url, legacy_username,
                          legacy_password, selenium):
    # GIVEN the legacy login form page
    login_page = LoginPage(selenium, legacy_base_url).open()

    # WHEN we login
    dashboard = login_page.login(legacy_username, legacy_password)

    # THEN the user is logged in (at their dashboard)
    # and the correct username is displayed
    assert type(dashboard) is Dashboard
    assert dashboard.username == legacy_username


@markers.legacy
@markers.slow
@markers.nondestructive
def test_login_page_login_logout(legacy_base_url, legacy_username,
                                 legacy_password, selenium):
    # GIVEN the legacy login form page
    login_page = LoginPage(selenium, legacy_base_url).open()

    # WHEN we login, then logout
    dashboard = login_page.login(legacy_username, legacy_password)
    login_page = dashboard.logout()

    # THEN the user is logged out (at the login form page)
    assert type(login_page) is LoginPage
