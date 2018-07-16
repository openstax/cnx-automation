from selenium.webdriver.common.by import By

from pages.webview.content import Content
from regions.webview.base import Region


class ContentPage(Content):

    @property
    def loaded(self):
        return bool(self._url_regex.search(
            self.driver.current_url)) and self.books_containing.overview_is_displayed

    @property
    def books_containing(self):
        return self.BooksContaining(self).wait_for_region_to_display()

    class BooksContaining(Region):
        _root_locator = (By.CLASS_NAME, 'booksContaining')
        _overview_locator = (By.CLASS_NAME, 'title')
        _book_list_locator = (By.CSS_SELECTOR, 'div > ul > li')

        @property
        def book_list(self):
            return [self.Book(self.page, el) for el in self.find_elements(*self._book_list_locator)]

        @property
        def overview_is_displayed(self):
            return self.find_element(*self._overview_locator).is_displayed()

        @property
        def overview(self):
            return self.find_element(*self._overview_locator).text

        class Book(Region):
            _title_locator = (By.CSS_SELECTOR, 'div')

            @property
            def title(self):
                return self.find_element(*self._title_locator).text
