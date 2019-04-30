from time import sleep
from applitools import MatchLevel
from tests import markers
import itertools

from pages.webview.home import Home

APP_NAME = 'CNX HOMEPAGE BOOKS VISUAL VERIFICATION-1'

@markers.nondestructive
def test_homepage_books(applitools, webview_base_url, selenium, deploy_version_tag, webview_version_tag, shmore_xpath_ids):

    # Level of matching the baseline and current screenshots
    # Valid match levels are:
        # 1. MatchLevel.EXACT - pixel-to-pixel  
        # 2. MatchLevel.STRICT - compares everything
        # 3. MatchLevel.CONTENT - like Strict but ignores colors 
        # 4. MatchLevel.LAYOUT - compares the layout
    applitools.match_level = MatchLevel.STRICT

    try:

        home = Home(selenium, webview_base_url).open()

        # Start the test and set the browser's viewport size to 1400x820
        applitools.open(driver=selenium, app_name=APP_NAME, test_name='Test homepage books', viewport_size={'width': 1400, 'height': 820})

        # Visual checkpoint - screenshot #1
        applitools.check_window('{}'.format(deploy_version_tag))

        # finds element by xpath, scrolls it into view and clicks "Show more" links
        xpelm = selenium.find_element_by_xpath("//*[@id='featured-books']/div/div[1]/div/div[1]/a/img")
        selenium.execute_script("return arguments[0].scrollIntoView(true);", xpelm)

        # reading through a set of xpaths in the list
        for i,line in enumerate(shmore_xpath_ids):

            if i > 5: continue
            sleep(1)

            xpelm = selenium.find_element_by_xpath(shmore_xpath_ids[i])
            # sleep(1)
            xpelm.click()

            # Visual checkpoint - screenshot #2
        applitools.check_window('-> {}'.format(webview_base_url))

        # End the test.
        applitools.close()

    finally:

        # If the test was aborted before applitools.close was called, ends the test as aborted
        applitools.abort_if_not_closed()


        assert applitools.api_key


