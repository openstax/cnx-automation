from time import sleep
from applitools import MatchLevel
from tests import markers

from pages.webview.home import Home

APP_NAME = 'CNX HOMEPAGE BOOKS VISUAL VERIFICATION'

@markers.nondestructive
def test_homepage_books(applitools, webview_base_url, selenium, deploy_version_tag, webview_version_tag):

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
        element = selenium.find_element_by_xpath("//*[@id='featured-books']/div/div[1]/div/div[1]/a/img")
        selenium.execute_script("return arguments[0].scrollIntoView(true);", element)

        # sleep(1)

        element2 = selenium.find_element_by_xpath("//*[@id='featured-books']/div/div[1]/div/div[1]/div/a[1]")
        # sleep(1)
        element2.click()

        element2 = selenium.find_element_by_xpath("//*[@id='featured-books']/div/div[1]/div/div[2]/div/a[1]")
        # sleep(1)
        element2.click()

        element2 = selenium.find_element_by_xpath("//*[@id='featured-books']/div/div[1]/div/div[3]/div/a[1]")
        # sleep(1)
        element2.click()

        element2 = selenium.find_element_by_xpath("//*[@id='featured-books']/div/div[1]/div/div[4]/div/a[1]")
        # sleep(1)
        element2.click()

        element2 = selenium.find_element_by_xpath("//*[@id='featured-books']/div/div[1]/div/div[5]/div/a[1]")
        # sleep(1)
        element2.click()

        element2 = selenium.find_element_by_xpath("//*[@id='featured-books']/div/div[1]/div/div[6]/div/a[1]")
        # sleep(1)
        element2.click()

        # sleep(1)

        # Visual checkpoint - screenshot #2
        applitools.check_window('-> {}'.format(webview_base_url))

        # finds element by xpath, scrolls it into view and clicks "Show more" links
        element = selenium.find_element_by_xpath("//*[@id='featured-books']/div/div[1]/div/div[7]/a/img")
        selenium.execute_script("return arguments[0].scrollIntoView(true);", element)

        # sleep(1)

        element2 = selenium.find_element_by_xpath("//*[@id='featured-books']/div/div[1]/div/div[7]/div/a[1]")
        # sleep(1)
        element2.click()

        element2 = selenium.find_element_by_xpath("//*[@id='featured-books']/div/div[1]/div/div[8]/div/a[1]")
        # sleep(1)
        element2.click()

        element2 = selenium.find_element_by_xpath("//*[@id='featured-books']/div/div[1]/div/div[9]/div/a[1]")
        # sleep(1)
        element2.click()

        element2 = selenium.find_element_by_xpath("//*[@id='featured-books']/div/div[1]/div/div[10]/div/a[1]")
        # sleep(1)
        element2.click()

        # sleep(1)

        # Visual checkpoint - screenshot #3
        applitools.check_window('-> webview: {}'.format(webview_version_tag))

        # finds element by xpath, scrolls it into view and clicks "Show more" links
        element = selenium.find_element_by_xpath("//*[@id='featured-books']/div/div[1]/div/div[11]/a/img")
        selenium.execute_script("return arguments[0].scrollIntoView(true);", element)

        # sleep(1)

        element2 = selenium.find_element_by_xpath("//*[@id='featured-books']/div/div[1]/div/div[11]/div/a[1]")
        # sleep(1)
        element2.click()

        element2 = selenium.find_element_by_xpath("//*[@id='featured-books']/div/div[1]/div/div[12]/div/a[1]")
        # sleep(1)
        element2.click()

        element2 = selenium.find_element_by_xpath("//*[@id='featured-books']/div/div[1]/div/div[13]/div/a[1]")
        # sleep(1)
        element2.click()

        element2 = selenium.find_element_by_xpath("//*[@id='featured-books']/div/div[1]/div/div[14]/div/a[1]")
        # sleep(1)
        element2.click()

        sleep(1)

        # Visual checkpoint - screenshot #4
        applitools.check_window('page')

        # finds element by xpath, scrolls it into view and clicks "Show more" links
        element = selenium.find_element_by_xpath("//*[@id='featured-books']/div/div[1]/div/div[15]/a/img")
        selenium.execute_script("return arguments[0].scrollIntoView(true);", element)

        # sleep(1)

        element2 = selenium.find_element_by_xpath("//*[@id='featured-books']/div/div[1]/div/div[15]/div/a[1]")
        # sleep(1)
        element2.click()

        element2 = selenium.find_element_by_xpath("//*[@id='featured-books']/div/div[1]/div/div[16]/div/a[1]")
        # sleep(1)
        element2.click()

        element2 = selenium.find_element_by_xpath("//*[@id='featured-books']/div/div[1]/div/div[17]/div/a[1]")
        # sleep(1)
        element2.click()

        element2 = selenium.find_element_by_xpath("//*[@id='featured-books']/div/div[1]/div/div[18]/div/a[1]")
        # sleep(1)
        element2.click()

        # sleep(1)

        # Visual checkpoint - screenshot #5
        applitools.check_window('{}'.format(deploy_version_tag))

        # finds element by xpath, scrolls it into view and clicks "Show more" links
        element = selenium.find_element_by_xpath("//*[@id='featured-books']/div/div[1]/div/div[19]/a/img")
        selenium.execute_script("return arguments[0].scrollIntoView(true);", element)

        # sleep(1)

        element2 = selenium.find_element_by_xpath("//*[@id='featured-books']/div/div[1]/div/div[19]/div/a[1]")
        # sleep(1)
        element2.click()

        element2 = selenium.find_element_by_xpath("//*[@id='featured-books']/div/div[1]/div/div[20]/div/a[1]")
        # sleep(1)
        element2.click()

        element2 = selenium.find_element_by_xpath("//*[@id='featured-books']/div/div[1]/div/div[21]/div/a[1]")
        # sleep(1)
        element2.click()

        element2 = selenium.find_element_by_xpath("//*[@id='featured-books']/div/div[1]/div/div[22]/div/a[1]")
        # sleep(1)
        element2.click()

        # sleep(1)

        # Visual checkpoint - screenshot #6
        applitools.check_window('-> {}'.format(webview_base_url))

        # finds element by xpath, scrolls it into view and clicks "Show more" links
        element = selenium.find_element_by_xpath("//*[@id='featured-books']/div/div[1]/div/div[23]/a/img")
        selenium.execute_script("return arguments[0].scrollIntoView(true);", element)

        # sleep(1)

        element2 = selenium.find_element_by_xpath("//*[@id='featured-books']/div/div[1]/div/div[23]/div/a[1]")
        # sleep(1)
        element2.click()

        element2 = selenium.find_element_by_xpath("//*[@id='featured-books']/div/div[1]/div/div[24]/div/a[1]")
        # sleep(1)
        element2.click()

        element2 = selenium.find_element_by_xpath("//*[@id='featured-books']/div/div[1]/div/div[25]/div/a[1]")
        # sleep(1)
        element2.click()

        element2 = selenium.find_element_by_xpath("//*[@id='featured-books']/div/div[1]/div/div[26]/div/a[1]")
        # sleep(1)
        element2.click()

        # sleep(1)

        # Visual checkpoint - screenshot #7
        applitools.check_window('-> webview: {}'.format(webview_version_tag))

        # finds element by xpath, scrolls it into view and clicks "Show more" links
        element = selenium.find_element_by_xpath("//*[@id='featured-books']/div/div[1]/div/div[27]/a/img")
        selenium.execute_script("return arguments[0].scrollIntoView(true);", element)

        # sleep(1)

        element2 = selenium.find_element_by_xpath("//*[@id='featured-books']/div/div[1]/div/div[27]/div/a[1]")
        # sleep(1)
        element2.click()

        element2 = selenium.find_element_by_xpath("//*[@id='featured-books']/div/div[1]/div/div[28]/div/a[1]")
        # sleep(1)
        element2.click()

        element2 = selenium.find_element_by_xpath("//*[@id='featured-books']/div/div[1]/div/div[29]/div/a[1]")
        # sleep(1)
        element2.click()

        element2 = selenium.find_element_by_xpath("//*[@id='featured-books']/div/div[1]/div/div[30]/div/a[1]")
        # sleep(1)
        element2.click()

        # sleep(1)

        # Visual checkpoint - screenshot #8
        applitools.check_window('page')

        # finds element by xpath, scrolls it into view and clicks "Show more" links
        element = selenium.find_element_by_xpath("//*[@id='featured-books']/div/div[1]/div/div[31]/a/img")
        selenium.execute_script("return arguments[0].scrollIntoView(true);", element)

        # sleep(1)

        element2 = selenium.find_element_by_xpath("//*[@id='featured-books']/div/div[1]/div/div[31]/div/a[1]")
        # sleep(1)
        element2.click()

        element2 = selenium.find_element_by_xpath("//*[@id='featured-books']/div/div[1]/div/div[32]/div/a[1]")
        # sleep(1)
        element2.click()

        element2 = selenium.find_element_by_xpath("//*[@id='featured-books']/div/div[1]/div/div[33]/div/a[1]")
        # sleep(1)
        element2.click()

        element2 = selenium.find_element_by_xpath("//*[@id='featured-books']/div/div[1]/div/div[34]/div/a[1]")
        # sleep(1)
        element2.click()

        # sleep(1)

        # Visual checkpoint - screenshot #9
        applitools.check_window('page')

        # finds element by xpath, scrolls it into view and clicks "Show more" links
        element = selenium.find_element_by_xpath("//*[@id='featured-books']/div/div[1]/div/div[35]/a/img")
        selenium.execute_script("return arguments[0].scrollIntoView(true);", element)

        # sleep(1)

        element2 = selenium.find_element_by_xpath("//*[@id='featured-books']/div/div[1]/div/div[35]/div/a[1]")
        # sleep(1)
        element2.click()

        element2 = selenium.find_element_by_xpath("//*[@id='featured-books']/div/div[1]/div/div[36]/div/a[1]")
        # sleep(1)
        element2.click()

        element2 = selenium.find_element_by_xpath("//*[@id='featured-books']/div/div[1]/div/div[37]/div/a[1]")
        # sleep(1)
        element2.click()

        element2 = selenium.find_element_by_xpath("//*[@id='featured-books']/div/div[1]/div/div[38]/div/a[1]")
        # sleep(1)
        element2.click()

        # sleep(1)

        # Visual checkpoint - screenshot #10
        applitools.check_window('page')

        # finds element by xpath, scrolls it into view and clicks "Show more" links
        element = selenium.find_element_by_xpath("//*[@id='featured-books']/div/div[1]/div/div[39]/a/img")
        selenium.execute_script("return arguments[0].scrollIntoView(true);", element)

        # sleep(1)

        element2 = selenium.find_element_by_xpath("//*[@id='featured-books']/div/div[1]/div/div[39]/div/a[1]")
        # sleep(1)
        element2.click()

        element2 = selenium.find_element_by_xpath("//*[@id='featured-books']/div/div[1]/div/div[40]/div/a[1]")
        # sleep(1)
        element2.click()

        element2 = selenium.find_element_by_xpath("//*[@id='featured-books']/div/div[1]/div/div[41]/div/a[1]")
        # sleep(1)
        element2.click()

        element2 = selenium.find_element_by_xpath("//*[@id='featured-books']/div/div[1]/div/div[42]/div/a[1]")
        # sleep(1)
        element2.click()

        # sleep(1)

        # Visual checkpoint - screenshot #11
        applitools.check_window('page')

        # finds element by xpath, scrolls it into view and clicks "Show more" links
        element = selenium.find_element_by_xpath("//*[@id='featured-books']/div/div[1]/div/div[43]/a/img")
        selenium.execute_script("return arguments[0].scrollIntoView(true);", element)

        # sleep(1)

        element2 = selenium.find_element_by_xpath("//*[@id='featured-books']/div/div[1]/div/div[43]/div/a[1]")
        # sleep(1)
        element2.click()

        element2 = selenium.find_element_by_xpath("//*[@id='featured-books']/div/div[1]/div/div[44]/div/a[1]")
        # sleep(1)
        element2.click()

        # sleep(1)

        # Visual checkpoint - screenshot #12
        applitools.check_window('page')

        # finds element by xpath, scrolls it into view and clicks "Show more" links
        element = selenium.find_element_by_xpath("//*[@id='featured-books']/div/div[1]/div/div[45]/a/img")
        selenium.execute_script("return arguments[0].scrollIntoView(true);", element)

        # sleep(1)

        element2 = selenium.find_element_by_xpath("//*[@id='featured-books']/div/div[1]/div/div[45]/div/a[1]")
        # sleep(1)
        element2.click()

        # sleep(1)

        # Visual checkpoint - screenshot #13
        applitools.check_window('page')

        # finds element by xpath, scrolls it into view and clicks "Show more" links
        element = selenium.find_element_by_xpath("//*[@id='featured-books']/div/div[2]/div/div[1]/a/img")
        selenium.execute_script("return arguments[0].scrollIntoView(true);", element)

        # sleep(1)

        element2 = selenium.find_element_by_xpath("//*[@id='featured-books']/div/div[2]/div/div[1]/div/a[1]")
        # sleep(1)
        element2.click()

        element2 = selenium.find_element_by_xpath("//*[@id='featured-books']/div/div[2]/div/div[2]/div/a[1]")
        # sleep(1)
        element2.click()

        # sleep(1)

        # Visual checkpoint - screenshot #14

        # finds element by xpath, scrolls it into view and clicks "Show more" links
        element = selenium.find_element_by_xpath("//*[@id='featured-books']/div/div[2]/div/div[3]/a/img")
        selenium.execute_script("return arguments[0].scrollIntoView(true);", element)

        # sleep(1)

        element2 = selenium.find_element_by_xpath("//*[@id='featured-books']/div/div[2]/div/div[3]/div/a[1]")
        # sleep(1)
        element2.click()

        element2 = selenium.find_element_by_xpath("//*[@id='featured-books']/div/div[2]/div/div[4]/div/a[1]")
        # sleep(1)
        element2.click()

        # sleep(1)

        # Visual checkpoint - screenshot #15
        applitools.check_window('page')

        # finds element by xpath, scrolls it into view and clicks "Show more" links
        element = selenium.find_element_by_xpath("//*[@id='featured-books']/div/div[2]/div/div[7]/a/img")
        selenium.execute_script("return arguments[0].scrollIntoView(true);", element)

        # sleep(1)

        element2 = selenium.find_element_by_xpath("//*[@id='featured-books']/div/div[2]/div/div[8]/div/a[1]")
        # sleep(1)
        element2.click()

        element2 = selenium.find_element_by_xpath("//*[@id='featured-books']/div/div[2]/div/div[10]/div/a[1]")
        # sleep(1)
        element2.click()

        # sleep(1)

        # Visual checkpoint - screenshot #16
        applitools.check_window('page')

        # finds element by xpath, clicks "Show more" links and scrolls to the bottom of page
        element2 = selenium.find_element_by_xpath("//*[@id='featured-books']/div/div[2]/div/div[11]/div/a[1]")
        # sleep(1)
        element2.click()
        selenium.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # sleep(1)

        # Visual checkpoint - screenshot #17
        applitools.check_window('page')

        # End the test.
        applitools.close()

        print('---->>> HOME PAGE BOOKS TESTING IS COMPLETE FOR {} and webview: {} @ {} - CHECK HTTPS://EYES.APPLITOOLS.COM/APP/TEST-RESULTS <<<----'.format(deploy_version_tag, webview_version_tag, webview_base_url))

    finally:

        # If the test was aborted before applitools.close was called, ends the test as aborted
        applitools.abort_if_not_closed()


        assert applitools.api_key


