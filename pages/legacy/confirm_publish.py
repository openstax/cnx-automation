# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from pages.legacy.base import PrivatePage

from selenium.webdriver.common.by import By


class ConfirmPublish(PrivatePage):
    _publish_form_locator = (By.CSS_SELECTOR, 'form[action="publishContent"]')

    @property
    def publish_form(self):
        return self.find_element(*self._publish_form_locator)

    def submit(self, max_retries=3):
        from pages.legacy.content_published import ContentPublished
        content_published = ContentPublished(self.driver, self.base_url, self.timeout)

        for i in range(max_retries):
            self.publish_form.submit()
            content_published.wait_for_page_to_load()

            if not content_published.has_site_error:
                break

            self.driver.back()
            self.wait_for_page_to_load()

        return content_published
