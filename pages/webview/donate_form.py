# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.webview.base import Page


class DonateForm(Page):

    _form_locator = (By.CSS_SELECTOR,
                     'form[action="https://ebank.rice.edu/C21279_upay/web/index.jsp"]')
    _amount_input_locator = (By.CSS_SELECTOR, 'input[type="number"][name="AMT"]')
    _required_input_locator = (By.CSS_SELECTOR, 'input[required]')

    @property
    def loaded(self):
        return (self.is_element_displayed(*self._form_locator) and
                self.is_element_displayed(*self._amount_input_locator))

    @property
    def is_form_displayed(self):
        return self.is_element_displayed(*self._form_locator)

    @property
    def form(self):
        return self.find_element(*self._form_locator)

    @property
    def amount_input(self):
        return self.find_element(*self._amount_input_locator)

    @property
    def amount(self):
        return int(self.amount_input.get_attribute('value'))

    @property
    def required_inputs(self):
        return self.find_elements(*self._required_input_locator)

    def submit(self):
        self.form.submit()
        self.wait_for_page_to_load()
        return self
