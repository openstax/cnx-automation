from selenium.webdriver.common.by import By

from pages.webview.content import Content
from regions.webview.base import Region


class ContentPage(Content):

    @property
    def loaded(self):
        return bool(
            self._url_regex.search(self.driver.current_url)) and self.books_containing.is_displayed

    @property
    def books_containing(self):
        return self.BooksContaining(self).wait_for_region_to_display()

    class BooksContaining(Region):
        _root_locator = (By.CLASS_NAME, 'booksContaining')
        _overview_locator = (By.CLASS_NAME, "title")
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

        class Book(Region):
            _title_locator = (By.CSS_SELECTOR, 'div')
            _author_locator = (By.CSS_SELECTOR, "li > ul > li:nth-child(1) > div")
            _revision_date_locator = (By.CSS_SELECTOR, "ul > li:nth-child(2) > div > b")
            _go_to_book_locator = (By.CSS_SELECTOR,
                                   "ul > li > ul > li:nth-child(3) > div > a")

            @property
            def title(self):
                return self.find_element(*self._title_locator).text

            @property
            def author(self):
                return self.find_element(*self._author_locator).text

            @property
            def revision_date(self):
                return self.find_element(*self._revision_date_locator)

            @property
            def click_go_to_book_link(self):
                self.find_element(*self._go_to_book_locator).click()
                return Content(self.driver, self.page.base_url, self.page.timeout).wait_for_page_to_load()
