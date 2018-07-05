# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import re

from selenium.webdriver.common.by import By

from pages.webview.base import Page
from regions.webview.base import Region


class Sitemap(Page):
    URL_TEMPLATE = '/sitemap-{author_username}.xml'
    _urlset_locator = (By.TAG_NAME, 'urlset')
    _urls_locator = (By.TAG_NAME, 'url')

    @property
    def urlset(self):
        return self.find_element(*self._urlset_locator)

    @property
    def url_regions(self):
        return [self.UrlRegion(self, url) for url
                in self.urlset.find_elements(*self._urls_locator)]

    class UrlRegion(Region):
        _loc_locator = (By.TAG_NAME, 'loc')
        _url_regex = re.compile('/contents?/((?:[^:@/]+@[^:@/]+:)?[^:@/]+@[^:@/]+)')

        @property
        def loc(self):
            return self.find_element(*self._loc_locator)

        @property
        def loc_url(self):
            return self.loc.get_attribute('innerHTML')

        # NOTE: we extract the id from the url and use that with Content().open() because
        #       we don't want the /slug in the url right away since we depend on its presence
        #       to detect when the Content page has fully loaded
        @property
        def content_id(self):
            return self._url_regex.search(self.loc_url)[1]

        def open(self):
            from pages.webview.content import Content
            return Content(self.driver, self.page.base_url, self.page.timeout,
                           id=self.content_id).open()
