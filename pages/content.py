# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.base import Base


class Content(Base):
    _content_locator = (By.ID, 'content')
    _title_locator = (By.CSS_SELECTOR, '.media-title h1')

    def wait_for_page_to_load(self):
        self.wait.until(lambda s: self.is_element_displayed(
            *self._content_locator))
        return self

    @property
    def title(self):
        return self.find_element(*self._title_locator).text
