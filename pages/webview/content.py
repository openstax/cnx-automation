# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from pkg_resources import parse_version
import re

from selenium.webdriver.common.by import By

from tests.utils import retry_stale_element_reference_exception

from pages.webview.base import Page
from regions.webview.base import Region
from regions.webview.content_item import ContentItem


class Content(Page):
    URL_TEMPLATE = '/contents/{id}'
    # The page is loaded when the last uuid/short id in the url has an @ version, followed by a /
    # This regex requires that version and additionally captures an optional book version
    _url_regex = re.compile(
        '/(?:[^:@/]+@(?P<book_version>[^:@/]+):)?[^:@/]+@(?P<page_version>[^:@/]+)/')
    _newer_version_link_locator = (
        By.CSS_SELECTOR, '#content div.latest span[data-l10n-id="media-latest-content"] a'
    )
    _main_content_section_locator = (By.ID, 'main-content')
    _section_title_div_locator = (By.CSS_SELECTOR, '#main-content div.media-header div.title')
    _chapter_section_span_locator = (By.CSS_SELECTOR, 'span.title-chapter,span.os-number')
    _get_this_book_button_locator = (
        By.CSS_SELECTOR, ('#main-content div.media-header div.info div.downloads'
                          ' button[type="submit"][data-l10n-id="textbook-view-btn-get-this-book"]')
    )
    _ncy_locator = (By.CLASS_NAME, 'not-converted-yet')

    @property
    def loaded(self):
        return bool(self._url_regex.search(self.driver.current_url))

    @property
    def book_version(self):
        return parse_version(self._url_regex.search(self.driver.current_url)['book_version'])

    @property
    def page_version(self):
        return parse_version(self._url_regex.search(self.driver.current_url)['page_version'])

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
    def newer_version_link(self):
        return self.find_element(*self._newer_version_link_locator)

    @property
    def main_content_section(self):
        return self.find_element(*self._main_content_section_locator)

    # The media-header div can be reloaded at seemingly random times
    # Any method that accesses an element inside this header
    # must retry StaleElementReferenceExceptions using retry_stale_element_reference_exception
    @property
    @retry_stale_element_reference_exception
    def is_section_title_displayed(self):
        return self.is_element_displayed(*self._section_title_div_locator)

    @property
    @retry_stale_element_reference_exception
    def section_title_div(self):
        return self.find_element(*self._section_title_div_locator)

    @property
    @retry_stale_element_reference_exception
    def chapter_section_span(self):
        return self.section_title_div.find_element(*self._chapter_section_span_locator)

    @property
    @retry_stale_element_reference_exception
    def chapter_section(self):
        return self.chapter_section_span.text

    @property
    @retry_stale_element_reference_exception
    def section_title(self):
        return self.section_title_div.text.replace(self.chapter_section, '').lstrip()

    @property
    @retry_stale_element_reference_exception
    def is_get_this_book_button_displayed(self):
        # Wait for the downloads load bar to disappear
        self.content_footer.downloads.wait_for_region_to_load()
        return self.is_element_displayed(*self._get_this_book_button_locator)

    @property
    @retry_stale_element_reference_exception
    def get_this_book_button(self):
        # Wait for the downloads load bar to disappear
        self.content_footer.downloads.wait_for_region_to_load()
        return self.find_element(*self._get_this_book_button_locator)

    @property
    def is_ncy_displayed(self):
        return self.is_element_displayed(*self._ncy_locator)

    @property
    def content_region(self):
        return self.ContentRegion(self)

    @property
    def content_footer(self):
        return self.ContentFooter(self)

    @property
    def footer_nav(self):
        return self.content_footer.nav

    def wait_for_url_to_change(self, current_url):
        self.wait.until(lambda _: self.driver.current_url != current_url)
        return self.wait_for_page_to_load()

    def click_newer_version_link(self):
        current_url = self.driver.current_url
        self.newer_version_link.click()
        return self.wait_for_url_to_change(current_url)

    @retry_stale_element_reference_exception
    def click_get_this_book_button(self):
        self.get_this_book_button.click()
        return self.GetThisBook(self).wait_for_region_to_load()

    class ContentHeader(Region):
        _root_locator = (By.CSS_SELECTOR, '#content div.pinnable')
        _title_locator = (By.CSS_SELECTOR, 'div.title .large-header')
        _book_by_span_locator = (By.CSS_SELECTOR,
                                 'div.info span[data-l10n-id="textbook-view-book-by"]')
        _author_span_locator = (
            By.CSS_SELECTOR,
            'div.info span[data-l10n-id="textbook-view-book-by"] span.collection-authors'
        )
        _derived_from_span_locator = (By.CSS_SELECTOR,
                                      'span[data-l10n-id="textbook-view-derived-from"]')

        # The title and author divs can be reloaded at seemingly random times so we must
        # retry StaleElementReferenceExceptions using retry_stale_element_reference_exception
        @property
        @retry_stale_element_reference_exception
        def is_title_displayed(self):
            return self.is_element_displayed(*self._title_locator)

        @property
        @retry_stale_element_reference_exception
        def title(self):
            return self.find_element(*self._title_locator).text

        @property
        @retry_stale_element_reference_exception
        def is_book_by_displayed(self):
            return self.is_element_displayed(*self._book_by_span_locator)

        @property
        @retry_stale_element_reference_exception
        def book_by_span(self):
            return self.find_element(*self._book_by_span_locator)

        @property
        @retry_stale_element_reference_exception
        def is_author_displayed(self):
            return self.is_element_displayed(*self._author_span_locator)

        @property
        @retry_stale_element_reference_exception
        def author(self):
            return self.find_element(*self._author_span_locator).text

        @property
        def is_derived_from_displayed(self):
            return self.is_element_displayed(*self._derived_from_span_locator)

        @property
        def derived_from_span(self):
            return self.find_element(*self._derived_from_span_locator)

        @property
        def derived_from_text(self):
            return self.derived_from_span.text

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
            _facebook_share_link_locator = (By.CSS_SELECTOR, 'ul li a.facebook')
            _twitter_share_link_locator = (By.CSS_SELECTOR, 'ul li a.twitter')
            _google_share_link_locator = (By.CSS_SELECTOR, 'ul li a.google')
            _linkedin_share_link_locator = (By.CSS_SELECTOR, 'ul li a.linkedin')

            @property
            def is_facebook_share_link_displayed(self):
                return self.is_element_displayed(*self._facebook_share_link_locator)

            @property
            def facebook_share_link(self):
                return self.find_element(*self._facebook_share_link_locator)

            @property
            def facebook_share_url(self):
                return self.facebook_share_link.get_attribute('href')

            @property
            def is_twitter_share_link_displayed(self):
                return self.is_element_displayed(*self._twitter_share_link_locator)

            @property
            def twitter_share_link(self):
                return self.find_element(*self._twitter_share_link_locator)

            @property
            def twitter_share_url(self):
                return self.twitter_share_link.get_attribute('href')

            @property
            def is_google_share_link_displayed(self):
                return self.is_element_displayed(*self._google_share_link_locator)

            @property
            def google_share_link(self):
                return self.find_element(*self._google_share_link_locator)

            @property
            def google_share_url(self):
                return self.google_share_link.get_attribute('href')

            @property
            def is_linkedin_share_link_displayed(self):
                return self.is_element_displayed(*self._linkedin_share_link_locator)

            @property
            def linkedin_share_link(self):
                return self.find_element(*self._linkedin_share_link_locator)

            @property
            def linkedin_share_url(self):
                return self.linkedin_share_link.get_attribute('href')

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
            def searchbar(self):
                return self.find_element(*self._searchbar_locator)

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

            @property
            def table_of_contents(self):
                return self.TableOfContents(self.page)

            @property
            def in_book_search_results(self):
                return self.InBookSearchResults(self.page)

            def click_contents_button(self):
                self.contents_button.click()
                return self.table_of_contents.wait_for_region_to_display()

            def search(self, query):
                searchbar = self.searchbar
                from selenium.webdriver.common.action_chains import ActionChains
                from selenium.webdriver.common.keys import Keys
                # For some reason self.searchbar.send_keys() fails with `cannot focus element`
                # https://stackoverflow.com/a/39205317
                ActionChains(self.driver).move_to_element(searchbar) \
                                         .click(searchbar) \
                                         .send_keys(query) \
                                         .send_keys(Keys.ENTER) \
                                         .perform()
                return self.in_book_search_results.wait_for_region_to_display()

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

            class InBookSearchResults(Region):
                _root_locator = (By.CSS_SELECTOR, '#content div.sidebar div.table-of-contents')
                _results_locator = (By.XPATH,
                                    (".//div[contains(@class, 'toc')]"
                                     "//ul//li[./div/span[contains(@class, 'name-wrapper')]//a]"))

                @property
                def results(self):
                    elements = self.find_elements(*self._results_locator)
                    return [self.InBookResult(self.page, element) for element in elements]

                class InBookResult(Region):
                    _link_locator = (By.CSS_SELECTOR, 'span.name-wrapper a')
                    _chapter_section_span_locator = (By.CSS_SELECTOR,
                                                     'span.chapter-number,span.os-number')
                    _title_span_locator = (By.CSS_SELECTOR, 'span.title')
                    _content_q_locator = (By.CSS_SELECTOR, 'div.snippet q')
                    _bold_locator = (By.CSS_SELECTOR, 'span.q-match')

                    @property
                    def is_link_present(self):
                        return self.is_element_present(*self._link_locator)

                    @property
                    def link(self):
                        return self.find_element(*self._link_locator)

                    @property
                    def chapter_section_span(self):
                        return self.link.find_element(*self._chapter_section_span_locator)

                    @property
                    def chapter_section(self):
                        return self.chapter_section_span.text

                    @property
                    def title_span(self):
                        return self.link.find_element(*self._title_span_locator)

                    @property
                    def title(self):
                        return self.title_span.text.replace(self.chapter_section, '').lstrip()

                    @property
                    def content_q(self):
                        return self.link.find_element(*self._content_q_locator)

                    @property
                    def content(self):
                        return self.content_q.text

                    @property
                    def bolds(self):
                        return self.content_q.find_elements(*self._bold_locator)

                    def count_occurrences(self, word):
                        return self.content.lower().count(word.lower())

                    def count_bold_occurrences(self, word):
                        lowercase_word = word.lower()
                        return len([bold for bold in self.bolds
                                    if lowercase_word in bold.text.lower()])

                    def click_link(self):
                        current_url = self.driver.current_url
                        self.link.click()
                        return self.page.wait_for_url_to_change(current_url)

    # This entire region can be overwritten (and the modal automatically closed) at any time,
    # so any tests that use it must be ready to retry StaleElementReferenceExceptions
    # using retry_stale_element_reference_exception
    class GetThisBook(Region):
        _root_locator = (By.CSS_SELECTOR, 'div.popover div.popover-content div.book-popover')
        _pdf_link_locator = (
            By.XPATH, ".//div[contains(@class, 'download-book')]//ul//li//a[text()='PDF']")
        _epub_link_locator = (
            By.XPATH, ".//div[contains(@class, 'download-book')]//ul//li//a[text()='EPUB']")
        _offline_zip_link_locator = (
            By.XPATH, ".//div[contains(@class, 'download-book')]//ul//li//a[text()='Offline ZIP']")
        _order_printed_book_link_locator = (
            By.CSS_SELECTOR, 'a.order[data-l10n-id="textbook-view-book-order-book"]')

        @property
        @retry_stale_element_reference_exception
        def root(self):
            return super().root

        @property
        @retry_stale_element_reference_exception
        def text(self):
            return super().text

        @property
        @retry_stale_element_reference_exception
        def loaded(self):
            return super().loaded

        @property
        @retry_stale_element_reference_exception
        def is_displayed(self):
            return super().is_displayed

        @retry_stale_element_reference_exception
        def find_element(self, strategy, locator):
            return super().find_element(strategy, locator)

        @retry_stale_element_reference_exception
        def find_elements(self, strategy, locator):
            return super().find_elements(strategy, locator)

        @retry_stale_element_reference_exception
        def is_element_present(self, strategy, locator):
            return not not super().is_element_present(strategy, locator)

        @retry_stale_element_reference_exception
        def is_element_displayed(self, strategy, locator):
            return super().is_element_displayed(strategy, locator)

        # Because of the flaky behavior of content pages (the modal keeps closing unexpectedly)
        # we use is_element_present here rather than is_element_displayed.
        # There's a chance the modal can silently close without an error,
        # which would cause is_element_displayed to fail.
        # Switch back to is_element_displayed when this modal closing bug is fixed.
        @property
        def is_pdf_link_displayed(self):
            return self.is_element_present(*self._pdf_link_locator)

        @property
        def is_epub_link_displayed(self):
            return self.is_element_present(*self._epub_link_locator)

        @property
        def is_offline_zip_link_displayed(self):
            return self.is_element_present(*self._offline_zip_link_locator)

        @property
        def is_order_printed_book_link_displayed(self):
            return self.is_element_present(*self._order_printed_book_link_locator)

    class ContentRegion(Region):
        _root_locator = (By.ID, 'content')
        _figures_locator = (By.TAG_NAME, 'figure')
        _anchor_links_locator = (By.CSS_SELECTOR, 'a[href*="#"]')
        _index_terms_locator = (By.CSS_SELECTOR, 'div.os-index-item a.os-term-section-link')

        @property
        def is_blank(self):
            return not self.text

        @property
        def has_figures(self):
            return self.is_element_present(*self._figures_locator)

        @property
        def is_figure_displayed(self):
            return self.is_element_displayed(*self._figures_locator)

        @property
        def figures(self):
            return self.find_elements(*self._figures_locator)

        @property
        def anchor_links(self):
            return self.find_elements(*self._anchor_links_locator)

        @property
        def index_terms(self):
            return self.find_elements(*self._index_terms_locator)

        def click_anchor_link(self, index=0):
            current_url = self.driver.current_url
            anchor_link = self.anchor_links[index]
            self.offscreen_click(anchor_link)
            return self.page.wait_for_url_to_change(current_url)

        def click_index_term(self, index=0):
            current_url = self.driver.current_url
            index_term = self.index_terms[index]
            self.offscreen_click(index_term)
            return self.page.wait_for_url_to_change(current_url)

    class ContentFooter(Region):
        _root_locator = (By.CSS_SELECTOR, '#main-content div.media-footer')
        _downloads_tab_locator = (By.ID, 'downloads-tab')
        _history_tab_locator = (By.ID, 'history-tab')
        _attribution_tab_locator = (By.ID, 'attribution-tab')
        _metadata_tab_locator = (By.ID, 'metadata-tab')

        @property
        def is_downloads_tab_displayed(self):
            return self.is_element_displayed(*self._downloads_tab_locator)

        @property
        def downloads_tab(self):
            return self.find_element(*self._downloads_tab_locator)

        @property
        def is_history_tab_displayed(self):
            return self.is_element_displayed(*self._history_tab_locator)

        @property
        def history_tab(self):
            return self.find_element(*self._history_tab_locator)

        @property
        def is_attribution_tab_displayed(self):
            return self.is_element_displayed(*self._attribution_tab_locator)

        @property
        def attribution_tab(self):
            return self.find_element(*self._attribution_tab_locator)

        @property
        def is_more_information_tab_displayed(self):
            return self.is_element_displayed(*self._metadata_tab_locator)

        @property
        def more_information_tab(self):
            return self.find_element(*self._metadata_tab_locator)

        @property
        def nav(self):
            return self.FooterNav(self.page)

        @property
        def downloads(self):
            return self.Downloads(self.page)

        @property
        def attribution(self):
            return self.Attribution(self.page)

        def click_downloads_tab(self):
            self.offscreen_click(self.downloads_tab)
            return self.downloads.wait_for_region_to_display()

        def click_attribution_tab(self):
            self.offscreen_click(self.attribution_tab)
            return self.attribution.wait_for_region_to_display()

        class Downloads(Region):
            _root_locator = (By.CSS_SELECTOR,
                             '#main-content div.media-footer div.downloads.tab-content')
            _progress_bar_locator = (By.CSS_SELECTOR, 'div.progress.active')
            _not_available_td_selector_template = (
                'table.table tr td[data-l10n-id="textbook-view-file-description"]'
                '[data-l10n-args=\'{{"format":"{format}"}}\']'
                ' ~ td[data-l10n-id="textbook-view-file-not-available"]'
            )

            @property
            def is_loading(self):
                return self.is_element_present(*self._progress_bar_locator)

            @property
            def loaded(self):
                return super().loaded and not self.is_loading

            @property
            def is_displayed(self):
                return super().is_displayed and not self.is_loading

            @property
            def is_pdf_available(self):
                selector = self._not_available_td_selector_template.format(format='PDF')
                return not self.is_element_present(By.CSS_SELECTOR, selector)

            @property
            def is_epub_available(self):
                selector = self._not_available_td_selector_template.format(format='EPUB')
                return not self.is_element_present(By.CSS_SELECTOR, selector)

            @property
            def is_offline_zip_available(self):
                selector = self._not_available_td_selector_template.format(format='Offline ZIP')
                return not self.is_element_present(By.CSS_SELECTOR, selector)

            @property
            def is_any_available(self):
                return (self.is_pdf_available or
                        self.is_epub_available or
                        self.is_offline_zip_available)

        class Attribution(Region):
            _root_locator = (By.CSS_SELECTOR,
                             '#main-content div.media-footer div.attribution.tab-content')

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
                self.offscreen_click(self.back_link)
                return self.page.wait_for_url_to_change(current_url)

            def click_back_to_top_link(self):
                self.offscreen_click(self.back_to_top_link)
                return self.page.wait_for_page_to_load()

            def click_next_link(self):
                current_url = self.driver.current_url
                self.offscreen_click(self.next_link)
                return self.page.wait_for_url_to_change(current_url)
