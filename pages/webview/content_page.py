from selenium.webdriver.common.by import By

from pages.webview.about_this_book import AboutBook
from pages.webview.content import Content
from regions.webview.base import Region
from tests.utils import retry_stale_element_reference_exception


class ContentPage(Content):
    @property
    def loaded(self):
        return bool(
            self._url_regex.search(
                self.driver.current_url)) and self.books_containing.overview_is_present

    @property
    def location(self):
        return self.table_of_contents_div.location

    # This region is reloaded when the page extras API call returns
    # So we must retry StaleElementReferenceExceptions
    @property
    @retry_stale_element_reference_exception
    def books_containing(self):
        return self.BooksContaining(self)

    class BooksContaining(Region):
        _root_locator = (By.CLASS_NAME, 'booksContaining')
        _overview_locator = (By.CLASS_NAME, 'title')
        _book_list_locator = (By.CSS_SELECTOR, 'div > ul > li')

        @property
        @retry_stale_element_reference_exception
        def book_list(self):
            return [self.Book(self.page, el) for el in self.find_elements(*self._book_list_locator)]

        @property
        @retry_stale_element_reference_exception
        def overview_is_displayed(self):
            return self.find_element(*self._overview_locator).is_displayed()

        @property
        @retry_stale_element_reference_exception
        def overview_is_present(self):
            return self.is_element_present(*self._overview_locator)

        @property
        @retry_stale_element_reference_exception
        def overview(self):
            return self.find_element(*self._overview_locator).text

        @property
        def description(self):
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
            @retry_stale_element_reference_exception
            def title(self):
                return self.find_element(*self._title_locator).text

            @retry_stale_element_reference_exception
            def click_title_link(self):
                return self.find_element(*self._title_locator).click()

            @property
            def author(self):
                return self.find_element(*self._author_locator)

            @property
            def revision_date(self):
                return self.find_element(*self._revision_date_locator)

            @property
            def click_go_to_book_link(self):
                self.offscreen_click(self.find_element(*self._go_to_book_locator))
                return AboutBook(self.driver, self.page.base_url,
                               self.page.timeout).wait_for_page_to_load()
