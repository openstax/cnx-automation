from time import sleep
from applitools.eyes import MatchLevel
from selenium.webdriver.common.keys import Keys
from tests import markers
from pages.webview.home import Home
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import ElementNotInteractableException

ApplName = 'Page Content Check'

# FINAL VERSION: June 20, 2019

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
        applitools.open(driver=selenium, app_name=ApplName, test_name='Random visual page content check', viewport_size={'width': width, 'height': height})

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
                    content_title = content.clean_title

                except (ElementNotVisibleException, StaleElementReferenceException, ElementNotInteractableException) as errors:

                    print("E R R O R  M E S S A G E S : \n")
                    print(errors)

                else:

                    # scrolls down on the page
                    selenium.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)

                    sleep(1)

                    # Visual checkpoint and screenshot of the page
                    applitools.check_window('-> {} on {}'.format(content_title, webview_base_url))

        applitools.close()

    finally:

        # If the test was aborted before eyes.close was called, ends the test as aborted.
        applitools.abort_if_not_closed()

