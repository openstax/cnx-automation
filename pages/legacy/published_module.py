# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from pages.legacy.base import PrivatePage

from selenium.webdriver.common.by import By


class PublishedModule(PrivatePage):

    _title_locator = (By.XPATH, ("//table[contains(@class, 'leftheadings']/tbody/tr/"
                                 "th[text()='Name:']/following-sibling::td/span"))
    _id_locator = (By.XPATH, ("//table[contains(@class, 'leftheadings']/tbody/tr/"
                              "th[text()='ID:']/following-sibling::td/span"))

    @property
    def title_span(self):
        return self.find_element(*self._title_locator)

    @property
    def title(self):
        return self.title_span.text

    @property
    def id_span(self):
        return self.find_element(*self._id_locator)

    @property
    def id(self):
        return self.id_span.text

    @property
    def loaded(self):
        return (super().loaded and
                self.is_element_displayed(*self._title_locator) and
                self.is_element_displayed(*self._id_locator))
