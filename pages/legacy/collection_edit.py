# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import re

from selenium.webdriver.common.by import By

from pages.legacy.base import PrivatePage


class CollectionEdit(PrivatePage):
    URL_TEMPLATE = '/Members/{username}/{collection_id}'
    _url_regex = re.compile('/Members/([^/]+)/([^/]+)')
    _title_regex = re.compile('^Collection: (.*)$')
    _title_header_locator = (By.CSS_SELECTOR, '#content div div h1')
    _root_collection_locator = (By.CSS_SELECTOR, 'ul.x-tree-root-ct li.x-tree-node')
    _publish_link_locator = (By.CSS_SELECTOR, 'a[href$="collection_publish"]')
    _modal_locator = (By.CSS_SELECTOR, 'div.x-window')
    _metadata_tab_locator = (By.ID, 'contentview-edit')
    _portal_msg_locator = (By.CLASS_NAME, 'portalMessage')

    @property
    def username(self):
        return self._url_regex.search(self.driver.current_url).group(1)

    @property
    def id(self):
        return self._url_regex.search(self.driver.current_url).group(2)

    @property
    def title_header(self):
        return self.find_element(*self._title_header_locator)

    @property
    def title(self):
        return self._title_regex.match(self.title_header.text).group(1)

    @property
    def is_portal_msg_present(self):
        return self.is_element_present(By.CLASS_NAME, 'portalMessage')

    @property
    def portal_msg(self):
        self.wait.until(lambda _: self.is_portal_msg_present)
        return self.find_element(*self._portal_msg_locator).text

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

    @property
    def is_metadata_tab_present(self):
        return self.is_element_present(By.ID, 'contentview-edit')

    def metadata(self):
        self.wait.until(lambda _: self.is_metadata_tab_present)

        metadata_tab = self.find_element(*self._metadata_tab_locator)
        metadata_tab.click()

        from pages.legacy.metadata_edit import MetadataEdit
        metadata_edit = MetadataEdit(self.driver, self.base_url, self.timeout)
        return metadata_edit.wait_for_page_to_load()
