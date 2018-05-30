# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.webview.base import Page


class Donate(Page):
    _form_locator = (By.CSS_SELECTOR, 'form.donation-slider')

    @property
    def form(self):
        return self.find_element(*self._form_locator)

    @property
    def loaded(self):
        return self.is_element_displayed(*self._form_locator)

    def submit(self):
        self.form.submit()
        from pages.webview.donate_form import DonateForm
        return DonateForm(self.driver, self.base_url, self.timeout).wait_for_page_to_load()
