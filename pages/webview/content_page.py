from selenium.webdriver.common.by import By

from tests.utils import retry_stale_element_reference_exception

from pages.webview.content import Content
from regions.webview.base import Region
from tests.utils import retry_stale_element_reference_exception


class ContentPage(Content):

    @property
    def loaded(self):
        return bool(
            self._url_regex.search(self.driver.current_url)) and self.books_containing.book_list

    # This region is reloaded when the page extras API call returns
    # So we must retry StaleElementReferenceExceptions
    @property
    @retry_stale_element_reference_exception
    def books_containing(self):
        return self.BooksContaining(self).wait_for_region_to_display()

    class BooksContaining(Region):
        _root_locator = (By.CLASS_NAME, 'booksContaining')
        _book_list_locator = (By.CSS_SELECTOR, 'div > ul > li')

        @property
        @retry_stale_element_reference_exception
        def book_list(self):
            return [self.Book(self.page, el) for el in self.find_elements(*self._book_list_locator)]

        class Book(Region):
            _title_locator = (By.CSS_SELECTOR, 'div')

            @property
            def title(self):
                return self.find_element(*self._title_locator).text
