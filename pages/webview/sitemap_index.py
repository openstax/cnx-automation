# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import re

from selenium.webdriver.common.by import By

from pages.webview.base import Page
from regions.webview.base import Region


class SitemapIndex(Page):
    URL_TEMPLATE = '/sitemap_index.xml'
    _sitemapindex_locator = (By.TAG_NAME, 'sitemapindex')
    _sitemaps_locator = (By.TAG_NAME, 'sitemap')
    # [name()='tag'] is used to ignore the namespaces in the xml file
    _sitemap_locator_template = (".//*[name()='sitemap'][.//*[name()='loc']"
                                 "[contains(., '/sitemap-{author_username}.xml')]]")

    @property
    def sitemapindex(self):
        return self.find_element(*self._sitemapindex_locator)

    @property
    def sitemap_regions(self):
        return [self.SitemapRegion(self, sitemap) for sitemap
                in self.sitemapindex.find_elements(*self._sitemaps_locator)]

    def sitemap_locator_for(self, author_username):
        return self._sitemap_locator_template.format(author_username=author_username)

    def find_sitemap_region(self, author_username):
        sitemap = self.find_element(By.XPATH, self.sitemap_locator_for(author_username))
        return self.SitemapRegion(self, sitemap)

    class SitemapRegion(Region):
        _loc_locator = (By.TAG_NAME, 'loc')
        _url_regex = re.compile('/sitemap-([^\.]+).xml')

        @property
        def loc(self):
            return self.find_element(*self._loc_locator)

        @property
        def loc_url(self):
            return self.loc.get_attribute('innerHTML')

        @property
        def author_username(self):
            return self._url_regex.search(self.loc_url)[1]

        def open(self):
            from pages.webview.sitemap import Sitemap
            return Sitemap(self.driver, self.page.base_url, self.page.timeout,
                           author_username=self.author_username).open()
