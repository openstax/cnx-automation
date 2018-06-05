# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from pages.legacy.base import PrivatePage

from selenium.webdriver.common.by import By


class ContentPublished(PrivatePage):
    _tbody_locator = (By.CSS_SELECTOR, 'table.leftheadings tbody')
    _title_locator = (By.XPATH, ("./tr/th[text()='Name:']/following-sibling::td/span"))
    _id_locator = (By.XPATH, ("./tr/th[text()='ID:']/following-sibling::td"))

    @property
    def tbody(self):
        return self.find_element(*self._tbody_locator)

    @property
    def title_span(self):
        return self.tbody.find_element(*self._title_locator)

    @property
    def title(self):
        return self.title_span.text

    @property
    def id_span(self):
        return self.tbody.find_element(*self._id_locator)

    @property
    def id(self):
        return self.id_span.text
