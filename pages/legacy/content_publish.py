# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from pages.legacy.base import PrivatePage

from selenium.webdriver.common.by import By


class ContentPublish(PrivatePage):
    _publish_form_locator = (By.CSS_SELECTOR, "#content div.documentContent div div form")
    _message_textarea_locator = (By.CSS_SELECTOR, 'textarea[name="message"]')
    _submit_button_locator = (
        By.CSS_SELECTOR,
        'input[type="submit"][name="form.button.publish"], '
        'input[type="submit"][name="form.button.submit"]',
    )
    _block_msg_locator = (By.CSS_SELECTOR, "#region-content > div > div > div > div > div")

    @property
    def publish_form(self):
        return self.find_element(*self._publish_form_locator)

    @property
    def message_textarea(self):
        return self.find_element(*self._message_textarea_locator)

    @property
    def submit_button(self):
        return self.publish_form.find_element(*self._submit_button_locator)

    def fill_in_message(self, message):
        self.message_textarea.send_keys(message)
        return self

    def submit(self):
        # Unlike the other forms, we actually have to click the submit button
        # when publishing the content, otherwise we end up in an error page
        self.submit_button.click()
        from pages.legacy.confirm_publish import ConfirmPublish

        confirm_publish = ConfirmPublish(self.driver, self.base_url, self.timeout)
        return confirm_publish.wait_for_page_to_load()

    @property
    def block_msg(self):
        return self.find_element(*self._block_msg_locator)

    @property
    def is_block_msg_displayed(self):
        return self.block_msg.is_displayed()
