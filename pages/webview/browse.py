# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from pypom import Region
from selenium.webdriver.common.by import By

from pages.webview.base import Base


class Browse(Base):
    URL_TEMPLATE = '/browse'

    _search_locator = (By.ID, 'find-content-input')
    _main_content_locator = (By.ID, 'main-content')
    _advanced_search_locator = (By.CLASS_NAME, 'advanced-search')
    _browse_content_locator = (By.CLASS_NAME, 'browse-content')
    _subject_list_locator = (By.CSS_SELECTOR, '.browse-content > ul > li')

    @property
    def loaded(self):
        return self.subject_list and self.is_main_content_displayed

    @property
    def is_main_content_displayed(self):
        main_content = self.find_element(*self._main_content_locator)
        return main_content.is_displayed()

    @property
    def is_search_input_displayed(self):
        return self.is_element_displayed(*self._search_locator)

    @property
    def is_advanced_search_button_displayed(self):
        return self.is_element_displayed(*self._advanced_search_locator)

    @property
    def subject_list(self):
        items = self.find_elements(*self._subject_list_locator)
        return [Browse.Subject(self, el) for el in items]

    class Subject(Region):
        _name_locator = (By.CSS_SELECTOR, 'h2')

        @property
        def name(self):
            return self.find_element(*self._name_locator).text
