# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import re

from selenium.webdriver.common.by import By

from pages.webview.base import Page
from regions.webview.base import Region
from regions.webview.content_item import ContentItem


class Content(Page):
    _url_regex = re.compile('@[^:]+$')
    _section_title_div_locator = (By.CSS_SELECTOR, '#main-content div.media-header div.title')
    _chapter_section_span_locator = (By.CSS_SELECTOR, 'span.title-chapter')
    _ncy_locator = (By.CLASS_NAME, 'not-converted-yet')

    @property
    def loaded(self):
        return self._url_regex.search(self.driver.current_url)

    @property
    def content_header(self):
        return self.ContentHeader(self)

    @property
    def header_nav(self):
        return self.content_header.nav

    @property
    def title(self):
        return self.content_header.title

    @property
    def share(self):
        return self.content_header.share

    @property
    def is_section_title_displayed(self):
        return self.is_element_displayed(*self._section_title_div_locator)

    @property
    def section_title_div(self):
        return self.find_element(*self._section_title_div_locator)

    @property
    def chapter_section_span(self):
        return self.section_title_div.find_element(*self._chapter_section_span_locator)

    @property
    def chapter_section(self):
        return self.chapter_section_span.text

    @property
    def section_title(self):
        return self.section_title_div.text.replace(self.chapter_section, '').strip()

    @property
    def is_ncy_displayed(self):
        return self.is_element_displayed(*self._ncy_locator)

    @property
    def content(self):
        return self.Content(self)

    @property
    def footer(self):
        return self.Footer(self)

    @property
    def footer_nav(self):
        return self.footer.nav

    def wait_for_url_to_change(self, current_url):
        self.wait.until(lambda _: self.driver.current_url != current_url)
        return self.wait_for_page_to_load()

    class ContentHeader(Region):
        _root_locator = (By.CSS_SELECTOR, '#content div.pinnable')
        _title_locator = (By.CSS_SELECTOR, 'div.title .large-header')
        _book_by_locator = (By.CSS_SELECTOR, 'div.info span[data-l10n-id="textbook-view-book-by"]')

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
        def nav(self):
            return self.HeaderNav(self.page)

        @property
        def is_share_displayed(self):
            return self.share.is_displayed

        class Share(Region):
            _root_locator = (By.CSS_SELECTOR, '#content div.pinnable div.share')

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

        class HeaderNav(Region):
            _root_locator = (By.CSS_SELECTOR, 'div.media-nav')
            _contents_button_locator = (By.CSS_SELECTOR, 'button.toggle.btn[role="button"]')
            _searchbar_locator = (By.CSS_SELECTOR, 'div.searchbar')
            _back_link_locator = (By.CSS_SELECTOR, 'div.media-navbar a.nav.back')
            _progress_bar_locator = (By.CSS_SELECTOR, 'div.media-navbar div.progress')
            _secondary_progress_bar_locator = (By.CSS_SELECTOR, 'div.secondary.progress-bar')
            _next_link_locator = (By.CSS_SELECTOR, 'div.media-navbar a.nav.next')

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

            @property
            def contents_button(self):
                return self.find_element(*self._contents_button_locator)

            @property
            def back_link(self):
                return self.find_element(*self._back_link_locator)

            @property
            def progress_bar(self):
                return self.find_element(*self._progress_bar_locator)

            @property
            def secondary_progress_bar(self):
                return self.progress_bar.find_element(*self._secondary_progress_bar_locator)

            def width_as_float(self, element):
                return float(element.value_of_css_property('width').replace('px', ''))

            @property
            def progress_bar_fraction(self):
                return (self.width_as_float(self.secondary_progress_bar) /
                        self.width_as_float(self.progress_bar))

            @property
            def next_link(self):
                return self.find_element(*self._next_link_locator)

            def click_contents_button(self):
                self.contents_button.click()
                return self.TableOfContents(self.page).wait_for_region_to_display()

            def click_back_link(self):
                current_url = self.driver.current_url
                self.back_link.click()
                return self.page.wait_for_url_to_change(current_url)

            def progress_bar_fraction_is(self, value):
                return abs(self.progress_bar_fraction - value) < 1e-3

            def click_next_link(self):
                current_url = self.driver.current_url
                self.next_link.click()
                return self.page.wait_for_url_to_change(current_url)

            class TableOfContents(Region):
                _root_locator = (By.CSS_SELECTOR,
                                 '#content div.sidebar div.table-of-contents div.toc')
                _chapter_div_locator = (By.CSS_SELECTOR, 'ul li div[data-expandable="true"]')
                _page_link_locator = (By.CSS_SELECTOR, 'ul li a')

                @property
                def number_of_chapters(self):
                    return len(self.find_elements(*self._chapter_div_locator))

                @property
                def number_of_pages(self):
                    return len(self.find_elements(*self._page_link_locator))

                @property
                def chapters(self):
                    return [self.ContentChapter(self.page, self.root, index) for index
                            in range(len(self.find_elements(*self._chapter_div_locator)))]

                class ContentChapter(ContentItem):
                    _root_locator_template = ("(.//ul//li[descendant::div"
                                              "[@data-expandable='true']])[{index}]")
                    _page_link_locator = (By.CSS_SELECTOR, 'ul li a')

                    @property
                    def has_pages(self):
                        return self.is_element_displayed(*self._page_link_locator)

                    @property
                    def pages(self):
                        return [self.ContentPage(self.page, self.root, index) for index
                                in range(len(self.find_elements(*self._page_link_locator)))]

                    def click(self):
                        self.root.click()
                        chapter = self.__class__(self.page, self.parent_root, self.index)
                        return chapter.wait_for_region_to_display()

                    class ContentPage(ContentItem):
                        _root_locator_template = "(.//ul[@data-expanded='true']//li//a)[{index}]"

                        def click(self):
                            current_url = self.driver.current_url
                            self.root.click()
                            return self.page.wait_for_url_to_change(current_url)

    class Content(Region):
        _root_locator = (By.ID, 'content')
        _figure_locator = (By.TAG_NAME, 'figure')

        @property
        def is_blank(self):
            return not self.text

        @property
        def has_figures(self):
            return self.is_element_present(*self._figure_locator)

    class Footer(Region):
        _root_locator = (By.CSS_SELECTOR, '#main-content div.media-footer')
        _downloads_tab_locator = (By.ID, 'downloads-tab')
        _history_tab_locator = (By.ID, 'history-tab')
        _attribution_tab_locator = (By.ID, 'attribution-tab')
        _metadata_tab_locator = (By.ID, 'metadata-tab')

        @property
        def is_downloads_tab_displayed(self):
            return self.is_element_displayed(*self._downloads_tab_locator)

        @property
        def is_history_tab_displayed(self):
            return self.is_element_displayed(*self._history_tab_locator)

        @property
        def is_attribution_tab_displayed(self):
            return self.is_element_displayed(*self._attribution_tab_locator)

        @property
        def is_more_information_tab_displayed(self):
            return self.is_element_displayed(*self._metadata_tab_locator)

        @property
        def nav(self):
            return self.FooterNav(self.page)

        class FooterNav(Region):
            _root_locator = (By.CSS_SELECTOR, '#main-content div.footer-nav')
            _back_link_locator = (By.CSS_SELECTOR, 'a.nav.back')
            _back_to_top_link_locator = (By.CSS_SELECTOR, 'div.back-to-top a')
            _next_link_locator = (By.CSS_SELECTOR, 'a.nav.next')

            @property
            def back_link(self):
                return self.find_element(*self._back_link_locator)

            @property
            def back_to_top_link(self):
                return self.find_element(*self._back_to_top_link_locator)

            @property
            def next_link(self):
                return self.find_element(*self._next_link_locator)

            def click_back_link(self):
                current_url = self.driver.current_url
                self.back_link.click()
                return self.page.wait_for_url_to_change(current_url)

            def click_back_to_top_link(self):
                self.back_to_top_link.click()
                return self.page.wait_for_page_to_load()

            def click_next_link(self):
                current_url = self.driver.current_url
                self.next_link.click()
                return self.page.wait_for_url_to_change(current_url)
