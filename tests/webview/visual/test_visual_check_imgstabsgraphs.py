from time import sleep
from applitools.eyes import MatchLevel
from selenium.webdriver.common.keys import Keys
from tests import markers
from pages.webview.home import Home
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import ElementNotInteractableException, TimeoutException

ApplName = 'Webview_Page Contents'

# FINAL VERSION: June 19, 2019

# Visual page content verification using applitools' eyes function
# To see results, log in to eyes.applitools.com/app/test-results

@markers.webview
@markers.nondestructive
@markers.parametrize("width, height", [(1400, 820)])
def test_page_objects(applitools, webview_base_url, selenium, width, height):

    # Level of matching the baseline and current screenshots
    # Valid match levels are:
    # 1. MatchLevel.EXACT - pixel-to-pixel  
    # 2. MatchLevel.STRICT - compares everything
    # 3. MatchLevel.CONTENT - like Strict but ignores colors 
    # 4. MatchLevel.LAYOUT - compares the layout

    applitools.match_level = MatchLevel.LAYOUT

    try:

        # Start the test and set the browser's viewport size to 1400x820.
        applitools.open(driver=selenium, app_name=ApplName, test_name='Book:Pages', viewport_size={'width': width, 'height': height})

        home = Home(selenium, webview_base_url).open()
        obooks = home.featured_books.openstax_list

        for i in range(0, len(obooks)-2, 3):

            home = Home(selenium, webview_base_url).open()
            book = home.featured_books.openstax_list[i]
            ccontent = book.click_book_cover()
            ccontent.header_nav.click_contents_button()
            toc = ccontent.table_of_contents

            # navigates to chapters and pages
            for k in range(1, 3):
                try:
                    lchapter = toc.chapters[k]
                    cchapter = lchapter.click()
                    page = cchapter.pages[k]
                    content = page.click()

                except (ElementNotVisibleException, StaleElementReferenceException, ElementNotInteractableException, TimeoutException) as errors:

                    print(" ---> ERROR MESSAGES:")
                    print(errors)

                else:

                    # scrolls down on the page
                    selenium.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)

                    sleep(1)

                    # Visual checkpoint - screenshot of the page
                    applitools.check_window('-> {}'.format(webview_base_url))

        applitools.close()

    finally:

        # If the test was aborted before eyes.close was called, ends the test as aborted.
        applitools.abort_if_not_closed()

