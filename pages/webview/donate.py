# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import json

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from pages.webview.base import Page
from regions.webview.base import Region


class Donate(Page):
    _form_locator = (By.CSS_SELECTOR, 'form.donation-slider')

    @property
    def form(self):
        return self.find_element(*self._form_locator)

    @property
    def donation_slider(self):
        return self.DonationSlider(self, self.form)

    @property
    def donation_value(self):
        return self.donation_slider.donation_value

    @property
    def loaded(self):
        return self.is_element_displayed(*self._form_locator)

    def submit(self):
        return self.donation_slider.submit()

    class DonationSlider(Region):
        _range_input_locator = (By.CSS_SELECTOR, 'input[type="range"][name="donation"]')
        _donation_value_span_locator = (By.CSS_SELECTOR, 'span.donation-value')

        @property
        def range_input(self):
            return self.find_element(*self._range_input_locator)

        @property
        def range_input_value(self):
            return int(self.range_input.get_attribute('aria-valuenow'))

        @property
        def donation_value_span(self):
            return self.find_element(*self._donation_value_span_locator)

        @property
        def donation_value(self):
            return json.loads(self.donation_value_span.get_attribute('data-l10n-args'))['amount']

        def move_left(self):
            self.range_input.send_keys(Keys.LEFT)
            return self

        def move_right(self):
            self.range_input.send_keys(Keys.RIGHT)
            return self

        def submit(self):
            self.root.submit()
            from pages.webview.donate_form import DonateForm
            donate_form = DonateForm(self.driver, self.page.base_url, self.page.timeout)
            return donate_form.wait_for_page_to_load()
