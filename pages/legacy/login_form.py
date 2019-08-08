# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.legacy.base import Page


class LoginForm(Page):
    URL_TEMPLATE = "/login_form"
    _login_form_locator = (By.ID, "login_form")
    _username_field_locator = (By.ID, "__ac_name")
    _password_field_locator = (By.ID, "__ac_password")
    _submit_button_locator = (By.CSS_SELECTOR, "#login_form > div.formControls > input")

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
    def can_login(self):
        return (
            self.is_element_displayed(*self._login_form_locator)
            and self.is_element_displayed(*self._username_field_locator)
            and self.is_element_displayed(*self._password_field_locator)
        )

    @property
    def submit_button(self):
        return self.find_element(*self._submit_button_locator)

    def login(self, username, password):
        self.username_field.send_keys(username)
        self.password_field.send_keys(password)
        self.submit_button.click()
        from pages.legacy.my_cnx import MyCnx

        my_cnx = MyCnx(self.driver, self.base_url, self.timeout)
        return my_cnx.wait_for_page_to_load()
