# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from pypom import Page


class Base(Page):

    def __init__(self, driver, base_url, timeout=15):
        super().__init__(driver, base_url, timeout)

    # Backported from PyPOM 2.0.0. Remove when upgrading to PyPOM 2.0.0+
    @property
    def loaded(self):
        """Loaded state of the page.
        By default the driver will try to wait for any page loads to be
        complete, however it's not uncommon for it to return early. To address
        this you can override :py:attr:`loaded` to return ``True`` when the
        page has finished loading.
        :return: ``True`` if page is loaded, else ``False``.
        :rtype: bool
        Usage (Selenium)::
          from pypom import Page
          from selenium.webdriver.common.by import By
          class Mozilla(Page):
              @property
              def loaded(self):
                  body = self.find_element(By.TAG_NAME, 'body')
                  return 'loaded' in body.get_attribute('class')
        Usage (Splinter)::
          from pypom import Page
          class Mozilla(Page):
              def loaded(self):
                  body = self.find_element('tag', 'body')
                  return 'loaded' in body['class']
        Examples::
            # wait for the seed_url value to be in the current URL
            self.seed_url in self.selenium.current_url
        """
        return True

    # Backported from PyPOM 2.0.0. Remove when upgrading to PyPOM 2.0.0+
    def wait_for_page_to_load(self):
        """Wait for the page to load."""
        self.wait.until(lambda _: self.loaded)
        return super().wait_for_page_to_load()
