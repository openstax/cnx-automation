# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from pypom import Region
from selenium.webdriver.common.by import By

from pages.webview.base import Base


class Home(Base):
    _splash_locator = (By.ID, 'splash')
    _openstax_books_locator = (By.CSS_SELECTOR, '.featured-books.openstax .books')
    _featured_books_locator = (By.ID, 'featured-books')

    @property
    def loaded(self):
        return self.find_elements(*self.featured_books._openstax_books_locator)

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
        _read_more_locator = (By.CSS_SELECTOR, '.read-more > a')
        _book_name_locator = (By.CSS_SELECTOR, 'h3')
        _book_cover_link_locator = (By.CSS_SELECTOR, '.book > a')
        _title_link_locator = (By.CSS_SELECTOR, 'h3 > a')

        @property
        def title(self):
            return self.find_element(*self._book_name_locator).text

        def click_read_more(self):
            self.find_element(*self._read_more_locator).click()
            from pages.webview.content import Content
            content = Content(self.driver, self.page.base_url, self.page.timeout)
            return content.wait_for_page_to_load()

        def click_book_cover(self):
            self.find_element(*self._book_cover_link_locator).click()
            from pages.webview.content import Content
            content = Content(self.driver, self.page.base_url, self.page.timeout)
            return content.wait_for_page_to_load()

        def click_title_link(self):
            self.find_element(*self._title_link_locator).click()
            from pages.webview.content import Content
            content = Content(self.driver, self.page.base_url, self.page.timeout)
            return content.wait_for_page_to_load()
