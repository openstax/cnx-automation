# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from pages.legacy.base import PrivatePage

from selenium.webdriver.common.by import By


class ModulePublish(PrivatePage):

    _publish_form_locator = (By.CSS_SELECTOR, 'form[action="module_publish_description"]')
    _submit_button_locator = (By.CSS_SELECTOR, 'input[type="submit"][name="form.button.publish"]')

    @property
    def publish_form(self):
        return self.find_element(*self._publish_form_locator)

    @property
    def submit_button(self):
        return self.publish_form.find_element(*self._submit_button_locator)

    def submit(self):
        # Unlike the other forms, we actually have to click the submit button here
        # when publishing the module, otherwise we end up in an error page
        self.submit_button.click()
        from pages.legacy.module_confirm_publish import ModuleConfirmPublish
        module_confirm_publish = ModuleConfirmPublish(self.driver, self.base_url, self.timeout)
        return module_confirm_publish.wait_for_page_to_load()
