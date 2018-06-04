# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import re

from pages.legacy.base import PrivatePage

from selenium.webdriver.common.by import By


class CollectionEdit(PrivatePage):
    URL_TEMPLATE = '/Members/{username}/{collection_id}'
    _url_regex = re.compile('/Members/([^/]+)/([^/]+)')
    _title_regex = re.compile('^Collection: (.*)$')
    _title_header_locator = (By.CSS_SELECTOR, '#content div div h1')
    _root_collection_locator = (By.CSS_SELECTOR, 'ul.x-tree-root-ct li.x-tree-node')
    _publish_link_locator = (By.CSS_SELECTOR, 'a[href$="collection_publish"]')
    _modal_locator = (By.CSS_SELECTOR, 'div.x-window')

    @property
    def username(self):
        return re.search(self._url_regex, self.driver.current_url).group(1)

    @property
    def id(self):
        return re.search(self._url_regex, self.driver.current_url).group(2)

    @property
    def title_header(self):
        return self.find_element(*self._title_header_locator)

    @property
    def title(self):
        return re.match(self._title_regex, self.title_header.text).group(1)

    @property
    def publish_link(self):
        return self.find_element(*self._publish_link_locator)

    @property
    def root_collection(self):
        from regions.legacy.collection import Collection
        collection = Collection(self, self.find_element(*self._root_collection_locator))
        return collection.wait_for_region_to_load()

    @property
    def modal(self):
        return self.find_element(*self._modal_locator)

    def publish(self):
        self.publish_link.click()
        from pages.legacy.content_publish import ContentPublish
        content_publish = ContentPublish(self.driver, self.base_url, self.timeout)
        return content_publish.wait_for_page_to_load()
