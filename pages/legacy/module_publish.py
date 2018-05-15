# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from pages.legacy.base import PrivatePage

from selenium.webdriver.common.by import By


class ModulePublish(PrivatePage):

    _publish_form_locator = (By.CSS_SELECTOR, 'form[action="module_publish_description"]')

    @property
    def publish_form(self):
        return self.find_element(*self._publish_form_locator)

    @property
    def loaded(self):
        return super().loaded and self.is_element_displayed(*self._publish_form_locator)

    def submit(self):
        self.publish_form.submit()
        from pages.legacy.module_confirm_publish import ModuleConfirmPublish
        module_confirm_publish = ModuleConfirmPublish(self.driver, self.base_url, self.timeout)
        return module_confirm_publish.wait_for_page_to_load()
