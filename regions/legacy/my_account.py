# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from regions.legacy.base import Region


class MyAccount(Region):
    _login_form_locator = (By.CSS_SELECTOR, 'form[action$="login_form"]')
    _username_field_locator = (By.ID, "__ac_name")
    _password_field_locator = (By.ID, "__ac_password")
    _login_submit_button_locator = (
        By.CSS_SELECTOR,
        'form[action$="login_form"] > table > tbody > tr:nth-child(3) > td:nth-child(2) > input',
    )
    _username_span_locator = (By.ID, "user-name")
    _logout_form_locator = (By.CSS_SELECTOR, 'form[action$="logout"]')
    _logout_button_locator = (By.CSS_SELECTOR, 'form[action$="logout"] > input')

    @property
    def can_login(self):
        return (
            self.is_element_displayed(*self._login_form_locator)
            and self.is_element_displayed(*self._username_field_locator)
            and self.is_element_displayed(*self._password_field_locator)
        )

    @property
    def login_form(self):
        return self.find_element(*self._login_form_locator)

    @property
    def username_field(self):
        return self.find_element(*self._username_field_locator)

    @property
    def password_field(self):
        return self.find_element(*self._password_field_locator)

    @property
    def login_submit_button(self):
        return self.find_element(*self._login_submit_button_locator)

    @property
    def logout_button(self):
        return self.find_element(*self._logout_button_locator)

    @property
    def has_username(self):
        return self.is_element_displayed(*self._username_span_locator)

    @property
    def username_span(self):
        return self.find_element(*self._username_span_locator)

    @property
    def username(self):
        return self.username_span.text if self.has_username else None

    @property
    def can_logout(self):
        return self.is_element_displayed(*self._logout_form_locator)

    @property
    def logout_form(self):
        return self.find_element(*self._logout_form_locator)

    def login(self, username, password):
        self.username_field.send_keys(username)
        self.password_field.send_keys(password)
        self.login_submit_button.click()
        from pages.legacy.my_cnx import MyCnx

        my_cnx = MyCnx(self.driver, self.page.base_url, self.page.timeout)
        return my_cnx.wait_for_page_to_load()

    def logout(self):
        self.logout_button.click()
        from pages.legacy.login_form import LoginForm

        login_form = LoginForm(self.driver, self.page.base_url, self.page.timeout)
        return login_form.wait_for_page_to_load()
