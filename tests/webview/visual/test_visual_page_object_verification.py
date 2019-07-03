from time import sleep
from applitools.eyes import MatchLevel
from selenium.webdriver.common.keys import Keys
from tests import markers
from pages.webview.home import Home
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import ElementNotInteractableException

ApplName = 'Random pages visual content checking'

# FINAL VERSION: July 02, 2019

"""
Visually checks pages contents (text, tabs, graphs and images) using applitools' eyes function.
Results are in eyes.applitools.com/app/test-results
"""

@markers.webview
@markers.nondestructive
@markers.visual
def test_visual_page_object_verification(applitools, webview_base_url, selenium, width, height):

    # Level of matching the baseline and current screenshots
    # Valid match levels are:
    # 1. MatchLevel.EXACT - pixel-to-pixel  
    # 2. MatchLevel.STRICT - compares everything
    # 3. MatchLevel.CONTENT - like Strict but ignores colors 
    # 4. MatchLevel.LAYOUT - compares the layout

    applitools.match_level = MatchLevel.LAYOUT

    try:

        # Start the test and set the browser's viewport's size
        applitools.open(driver=selenium, app_name=ApplName, test_name='Page content checks', viewport_size={'width': width, 'height': height})

        home = Home(selenium, webview_base_url).open()
        obooks = home.featured_books.openstax_list

        # defines how many books will be selected
        for i in range(0, len(obooks), 4):

            home = Home(selenium, webview_base_url).open()
            book = home.featured_books.openstax_list[i]
            ccontent = book.click_book_cover()
            ccontent.header_nav.click_contents_button()
            toc = ccontent.table_of_contents

            # navigates to chapters and their sub-chapters
            for k in range(1, 5):

                try:
                    # clicks on 'k-1' number of chapters in a book
                    lchapter = toc.chapters[k]
                    cchapter = lchapter.click()
                    page = cchapter.pages[1]
                    content = page.click()

                except (IndexError, ElementNotVisibleException, StaleElementReferenceException, ElementNotInteractableException) as errors:

                    print("\n E R R O R  M E S S A G E S : \n")
                    print(errors)
                    print(' -->> moving on to next page')

                else:

                    # scrolls down on the selected sub-chapter
                    selenium.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)

                    sleep(1)

                    # takes screenshot of the scrolled chapter and stores it in applitools
                    applitools.check_window('-> {}'.format(webview_base_url))

        applitools.close()

    finally:

        # If the test was aborted before eyes.close was called, ends the test as aborted.
        applitools.abort_if_not_closed()

