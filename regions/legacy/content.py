# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from regions.legacy.base import Region

from selenium.webdriver.common.by import By


class Content(Region):

    _content_node_locator = (By.CSS_SELECTOR, 'ul.x-tree-node-ct li.x-tree-node')

    _title_span_locator = (By.CSS_SELECTOR, 'a.x-tree-node-anchor span')

    def hover(self):
        from selenium.webdriver.common.action_chains import ActionChains
        ActionChains(self.page.driver).move_to_element(self.root).perform()
        return self

    @property
    def title_span(self):
        return self.find_element(*self._title_span_locator)

    @property
    def title(self):
        return self.title_span.text
