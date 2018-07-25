from selenium.webdriver.common.by import By

from tests.utils import retry_stale_element_reference_exception

from pages.webview.content import Content
from regions.webview.base import Region


class ContentPage(Content):

    @property
    def loaded(self):
        return bool(
            self._url_regex.search(self.driver.current_url)) and self.books_containing.book_list

    # This region is reloaded when the pages extras API call returns
    # So we must retry StaleElementReferenceExceptions
    @property
    @retry_stale_element_reference_exception
    def books_containing(self):
        return self.BooksContaining(self).wait_for_region_to_display()

    class BooksContaining(Region):
        _root_locator = (By.CLASS_NAME, 'booksContaining')
        _overview_locator = (By.CLASS_NAME, 'title')
        _book_list_locator = (By.CSS_SELECTOR, 'div > ul > li')

        @property
        def is_displayed(self):
            return self.is_element_displayed(*self._book_list_locator)

        @property
        def book_list(self):
            return [self.Book(self.page, el) for el in self.find_elements(*self._book_list_locator)]

        @property
        def description(self):
            self.find_element(*self._root_locator)
            return self.find_element(*self._overview_locator).text

        @property
        def date_list(self):
            return [self.Book(self.page, el).revision_date.text.split(":")[1:]
                    for el in self.find_elements(*self._book_list_locator)]

        @property
        def author_list(self):
            return [(self.Book(self.page, el).author.text.split(': ')[1:])
                    for el in self.find_elements(*self._book_list_locator)]

        class Book(Region):
            _title_locator = (By.CSS_SELECTOR, 'div')
            _author_locator = (By.CSS_SELECTOR, 'li > ul > li:nth-child(1) > div')
            _revision_date_locator = (By.CSS_SELECTOR, 'ul > li:nth-child(2) > div')
            _go_to_book_locator = (By.CSS_SELECTOR,
                                   'ul > li > ul > li:nth-child(3) > div > a')

            @property
            def title(self):
                return self.find_element(*self._title_locator).text

            @property
            def author(self):
                return self.find_element(*self._author_locator)

            @property
            def revision_date(self):
                return self.find_element(*self._revision_date_locator)

            @property
            def click_go_to_book_link(self):
                self.offscreen_click(self.find_element(*self._go_to_book_locator))
                return Content(self.driver, self.page.base_url,
                               self.page.timeout).wait_for_page_to_load()
