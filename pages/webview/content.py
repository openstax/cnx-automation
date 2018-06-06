# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.webview.base import Page
from regions.webview.base import Region


class Content(Page):
    _content_nav_locator = (By.CSS_SELECTOR, '#content div.pinnable')
    _ncy_locator = (By.CLASS_NAME, 'not-converted-yet')

    @property
    def loaded(self):
        return '@' in self.driver.current_url

    @property
    def content_nav(self):
        return self.ContentNav(self)

    @property
    def title(self):
        return self.content_nav.title

    @property
    def share(self):
        return self.content_nav.share

    @property
    def is_ncy_displayed(self):
        return self.is_element_displayed(*self._ncy_locator)

    class ContentNav(Region):
        _root_locator = (By.CSS_SELECTOR, '#content div.pinnable')
        _title_locator = (By.CSS_SELECTOR, 'div.title .large-header')
        _book_by_locator = (By.CSS_SELECTOR, 'div.info span[data-l10n-id="textbook-view-book-by"]')
        _contents_button_locator = (By.CSS_SELECTOR,
                                    'div.media-nav button.toggle.btn[role="button"]')
        _searchbar_locator = (By.CSS_SELECTOR, 'div.media-nav div.searchbar')
        _back_link_locator = (By.CSS_SELECTOR, 'div.media-nav div.media-navbar a.nav.back')
        _progress_bar_locator = (By.CSS_SELECTOR, 'div.media-nav div.media-navbar div.progress')
        _next_link_locator = (By.CSS_SELECTOR, 'div.media-nav div.media-navbar a.nav.next')

        @property
        def is_title_displayed(self):
            return self.is_element_displayed(*self._title_locator)

        @property
        def title(self):
            return self.find_element(*self._title_locator).text

        @property
        def is_book_by_displayed(self):
            return self.is_element_displayed(*self._book_by_locator)

        @property
        def share(self):
            return self.Share(self.page)

        @property
        def is_share_displayed(self):
            return self.share.is_displayed

        @property
        def is_contents_button_displayed(self):
            return self.is_element_displayed(*self._contents_button_locator)

        @property
        def is_searchbar_displayed(self):
            return self.is_element_displayed(*self._searchbar_locator)

        @property
        def is_back_link_displayed(self):
            return self.is_element_displayed(*self._back_link_locator)

        @property
        def is_progress_bar_displayed(self):
            return self.is_element_displayed(*self._progress_bar_locator)

        @property
        def is_next_link_displayed(self):
            return self.is_element_displayed(*self._next_link_locator)

        class Share(Region):
            _root_locator = (By.CSS_SELECTOR, '#content div.pinnable div.share')

            @property
            def current_url(self):
                return self.driver.current_url

            @property
            def normalized_title(self):
                return self.page.title.replace(' ', '%20')

            def _share_link_locator(self, url):
                return (By.CSS_SELECTOR, 'a[href="{url}"]'.format(url=url))

            @property
            def _facebook_share_link_locator(self):
                url = 'https://facebook.com/sharer/sharer.php?u={url}'.format(url=self.current_url)
                return self._share_link_locator(url)

            @property
            def _twitter_share_link_locator(self):
                url = 'https://twitter.com/share?url={url}&text={title}&via=cnxorg'.format(
                      url=self.current_url, title=self.normalized_title)
                return self._share_link_locator(url)

            @property
            def _google_share_link_locator(self):
                url = 'https://plus.google.com/share?url={url}'.format(url=self.current_url)
                return self._share_link_locator(url)

            @property
            def _linkedin_share_link_locator(self):
                url = (
                    'https://www.linkedin.com/shareArticle?mini=true&url={url}&title={title}&'
                    'summary=An%20OpenStax%20CNX%20book&source=OpenStax%20CNX'
                ).format(url=self.current_url, title=self.normalized_title)
                return self._share_link_locator(url)

            @property
            def is_facebook_share_link_displayed(self):
                return self.is_element_displayed(*self._facebook_share_link_locator)

            @property
            def is_twitter_share_link_displayed(self):
                return self.is_element_displayed(*self._twitter_share_link_locator)

            @property
            def is_google_share_link_displayed(self):
                return self.is_element_displayed(*self._google_share_link_locator)

            @property
            def is_linkedin_share_link_displayed(self):
                return self.is_element_displayed(*self._linkedin_share_link_locator)
