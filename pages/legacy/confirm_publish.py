# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.legacy.base import PrivatePage

from selenium.webdriver.common.by import By


class ConfirmPublish(PrivatePage):
    _publish_form_locator = (By.CSS_SELECTOR, 'form[action="publishContent"]')

    @property
    def publish_form(self):
        return self.find_element(*self._publish_form_locator)

    def submit(self, max_tries=3):
        from pages.legacy.content_published import ContentPublished
        content_published = ContentPublished(self.driver, self.base_url, self.timeout)

        # Sometimes publishing fails with a SiteError. In those cases, we retry it a few times.
        for i in range(max_tries):
            self.publish_form.submit()
            content_published.wait_for_page_to_load()

            if not content_published.has_site_error:
                break
            elif i >= max_tries - 1:
                pytest.fail('Maximum number of tries exceeded for SiteError'
                            ' ({tries})'.format(tries=max_tries))

            self.driver.back()
            self.wait_for_page_to_load()

        return content_published
