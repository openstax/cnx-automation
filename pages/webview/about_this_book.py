from selenium.webdriver.common.by import By

from .content import Content


class AboutBook(Content):

    _about_this_book_locator = (By.CSS_SELECTOR, '.media-body-about')

    @property
    def about_this_book_section(self):
        return self.find_element(*self._about_this_book_locator)
