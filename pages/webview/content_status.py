# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.webview.base import Page
from regions.webview.base import Region


class ContentStatus(Page):
    URL_TEMPLATE = "/a/content-status/?number={number}&page={page}"
    _status_filters_locator = (
        By.XPATH,
        (
            ".//form[contains(@action, '/a/content-status')]//label"
            "[.//i[contains(@class, 'state-icon')]]"
        ),
    )
    _tds_locator = (By.CSS_SELECTOR, "table td")

    def __init__(self, *args, **kwargs):
        if "number" not in kwargs:
            kwargs["number"] = 10
        if "page" not in kwargs:
            kwargs["page"] = 1

        super().__init__(*args, **kwargs)

    @property
    def are_status_filters_displayed(self):
        return self.is_element_displayed(*self._status_filters_locator)

    @property
    def status_filters(self):
        labels = self.find_elements(*self._status_filters_locator)
        return [self.StatusFilter(self, label) for label in labels]

    @property
    def are_tds_displayed(self):
        return self.is_element_displayed(*self._tds_locator)

    @property
    def tds(self):
        elements = self.find_elements(*self._tds_locator)
        return [self.ContentStatusTd(self, element) for element in elements]

    class StatusFilter(Region):
        _checkbox_locator = (By.CSS_SELECTOR, 'input[type="checkbox"][name="status_filter"]')
        _icon_locator = (By.CSS_SELECTOR, "i.fa.state-icon")

        @property
        def is_checkbox_displayed(self):
            return self.is_element_displayed(*self._checkbox_locator)

        @property
        def checkbox(self):
            return self.find_element(*self._checkbox_locator)

        @property
        def status(self):
            return self.checkbox.get_attribute("value").lower()

        @property
        def is_icon_displayed(self):
            return self.is_element_displayed(*self._icon_locator)

        @property
        def icon(self):
            return self.find_element(*self._icon_locator)

        @property
        def icon_class(self):
            return self.icon.get_attribute("class")

        @property
        def icon_color(self):
            return self.icon.value_of_css_property("color")

    class ContentStatusTd(Region):
        @property
        def border_style(self):
            return self.root.value_of_css_property("border-style")

        @property
        def border_width(self):
            return self.root.value_of_css_property("border-width")

        @property
        def border_color(self):
            return self.root.value_of_css_property("border-color")
