# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.webview.base import Page
from regions.webview.base import Region


class Home(Page):
    _splash_locator = (By.ID, 'splash')
    _openstax_books_locator = (By.CSS_SELECTOR, '.featured-books.openstax .books')
    _featured_books_locator = (By.ID, 'featured-books')

    @property
    def loaded(self):
        return self.is_element_present(*self.featured_books._openstax_books_locator)

    @property
    def splash(self):
        return self.find_element(*self._splash_locator).text

    @property
    def featured_books(self):
        el = self.find_element(*self._featured_books_locator)
        return self.FeaturedBooks(self, el)

    class FeaturedBooks(Region):
        _openstax_books_locator = (By.CSS_SELECTOR, '.featured-books.openstax .book')
        _cnx_books_locator = (By.CSS_SELECTOR, '.featured-books.cnx .book')

        @property
        def openstax_list(self):
            items = self.find_elements(*self._openstax_books_locator)
            return [Home.Book(self.page, el) for el in items]

        @property
        def cnx_list(self):
            items = self.find_elements(*self._cnx_books_locator)
            return [Home.Book(self.page, el) for el in items]

    class Book(Region):
        _show_more_locator = (By.CSS_SELECTOR, 'div.show-more-less a.more')
        _show_less_locator = (By.CSS_SELECTOR, 'div.show-more-less a.less')
        _book_name_locator = (By.CSS_SELECTOR, 'h3')
        _book_intro_locator = (By.CSS_SELECTOR, 'p')
        _book_cover_link_locator = (By.CSS_SELECTOR, '.book > a')
        _book_cover_img_locator = (By.CSS_SELECTOR, '.book > a > img')
        _title_link_locator = (By.CSS_SELECTOR, 'h3 > a')

        @property
        def is_show_more_displayed(self):
            return self.is_element_displayed(*self._show_more_locator)

        @property
        def is_show_less_displayed(self):
            return self.is_element_displayed(*self._show_less_locator)

        @property
        def book_cover_link(self):
            return self.find_element(*self._book_cover_link_locator)

        @property
        def book_cover_img(self):
            return self.find_element(*self._book_cover_img_locator)

        @property
        def is_book_cover_clickable(self):
            """Returns a boolean if the book cover is clickable

            Slow connections causing images to be rendered slowly which causes errors
            when trying to click the element before it has an actual width and height.
            This property allows for us to wait until the image has an actual size before
            attempting a click.

            """
            if not self.is_element_present(*self._book_cover_img_locator):
                return False
            size = self.book_cover_img.size
            return size['width'] > 0 and size['height'] > 0

        @property
        def title(self):
            return self.find_element(*self._book_name_locator).text

        @property
        def intro(self):
            return self.find_element(*self._book_intro_locator).text

        @property
        def is_intro_collapsed(self):
            return self.intro.endswith('…')

        def click_show_more(self):
            self.offscreen_click(self.find_element(*self._show_more_locator))
            self.wait.until(lambda _: not self.is_intro_collapsed)
            return self

        def click_show_less(self):
            self.offscreen_click(self.find_element(*self._show_less_locator))
            self.wait.until(lambda _: self.is_intro_collapsed)
            return self

        def click_book_cover(self):
            self.wait.until(lambda _: self.is_book_cover_clickable)
            self.offscreen_click(self.book_cover_link)
            from pages.webview.content import Content
            content = Content(self.driver, self.page.base_url, self.page.timeout)
            return content.wait_for_page_to_load()

        def click_title_link(self):
            self.offscreen_click(self.find_element(*self._title_link_locator))
            from pages.webview.content import Content
            content = Content(self.driver, self.page.base_url, self.page.timeout)
            return content.wait_for_page_to_load()
