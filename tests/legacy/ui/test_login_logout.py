# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from tests import markers

from pages.legacy.home import Home
from pages.legacy.my_dashboard import MyDashboard
from pages.legacy.login_form import LoginForm


class TestLoginLogout(object):

    @markers.legacy
    @markers.slow
    @markers.nondestructive
    def test_home_login(self, legacy_base_url, legacy_username, legacy_password, selenium):
        # GIVEN the legacy homepage
        home = Home(selenium, legacy_base_url).open()

        # WHEN we login
        my_dashboard = home.login(legacy_username, legacy_password)

        # THEN the user is logged in (at their dashboard)
        # and the correct username is displayed
        assert type(my_dashboard) is MyDashboard
        assert my_dashboard.username == legacy_username

    @markers.legacy
    @markers.slow
    @markers.nondestructive
    def test_home_login_logout(self, legacy_base_url, legacy_username, legacy_password, selenium):
        # GIVEN the legacy homepage
        home = Home(selenium, legacy_base_url).open()

        # WHEN we login, then logout
        my_dashboard = home.login(legacy_username, legacy_password)
        login_page = my_dashboard.logout()

        # THEN the user is logged out (at the login form page)
        assert type(login_page) is LoginForm

    @markers.legacy
    @markers.slow
    @markers.nondestructive
    def test_login_page_login(self, legacy_base_url, legacy_username, legacy_password, selenium):
        # GIVEN the legacy login form page
        login_page = LoginForm(selenium, legacy_base_url).open()

        # WHEN we login
        my_dashboard = login_page.login(legacy_username, legacy_password)

        # THEN the user is logged in (at their dashboard)
        # and the correct username is displayed
        assert type(my_dashboard) is MyDashboard
        assert my_dashboard.username == legacy_username

    @markers.legacy
    @markers.slow
    @markers.nondestructive
    def test_login_page_login_logout(self, legacy_base_url, legacy_username,
                                     legacy_password, selenium):
        # GIVEN the legacy login form page
        login_page = LoginForm(selenium, legacy_base_url).open()

        # WHEN we login, then logout
        my_dashboard = login_page.login(legacy_username, legacy_password)
        login_page = my_dashboard.logout()

        # THEN the user is logged out (at the login form page)
        assert type(login_page) is LoginForm
