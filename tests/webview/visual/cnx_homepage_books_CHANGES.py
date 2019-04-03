from selenium import webdriver
from applitools.eyes import Eyes
from time import sleep
# from dotenv import load_dotenv
from applitools.eyes import MatchLevel
import os
from tests.utils import cnx_deploy_version
from pages.webview.home import Home


# load_dotenv(verbose = True)

# url_addr = os.environ['URL_HOME_PAGE']

class CnxHomePageBooksLayout:

    def test_books_homepage_layout(self, selenium, webview_base_url, request):

        # Verifies visual presence of book icons on cnx home page using applitools' eyes function
        # To see results, log in to eyes.applitools.com/app/test-results
        # Baseline images from cnx.org taken on Feb. 22, 2019

        applitools_key = os.environ['APPLITOOLS_API_KEY']
        App_Name = 'CNX HOME PAGE BOOK ICONS'

        eyes = Eyes()

        # Initialize the eyes SDK and set your private API key
        eyes.api_key = applitools_key

        # Level of matching the baseline and current screenshots
        eyes.match_level = MatchLevel.STRICT

        # current cnx deploy and webview versions
        cnx_ver = cnx_deploy_version.cnx_versions
        cnx_web_web = cnx_deploy_version.cnx_w_web

        try:

            # Open a Chrome browser
            # driver = webdriver.Chrome()

            # Navigate the browser to the cnx web-site
            page = selenium.get(webview_base_url)

            home = Home(selenium, webview_base_url).open()

            # Start the test and set the browser's viewport size to 1400x820
            eyes.open(driver=page, app_name=App_Name, test_name='Book icons', viewport_size={'width': 1400, 'height': 820})

            sleep(2)

        # Visual checkpoint - screenshot #1
            eyes.check_window('{}'.format(cnx_ver))

# finds element by xpath, scrolls it into view and clicks "Show more" links
            element = page.find_element_by_xpath("//*[@id='featured-books']/div/div[1]/div/div[1]/a/img")
            page.execute_script("return arguments[0].scrollIntoView(true);", element)

            sleep(1)

            element2 = page.find_element_by_xpath("//*[@id='featured-books']/div/div[1]/div/div[1]/div/a[1]")
            sleep(1)
            element2.click()

            element2 = page.find_element_by_xpath("//*[@id='featured-books']/div/div[1]/div/div[2]/div/a[1]")
            sleep(1)
            element2.click()

            element2 = page.find_element_by_xpath("//*[@id='featured-books']/div/div[1]/div/div[3]/div/a[1]")
            sleep(1)
            element2.click()

            element2 = driver.find_element_by_xpath("//*[@id='featured-books']/div/div[1]/div/div[4]/div/a[1]")
            sleep(1)
            element2.click()

            element2 = driver.find_element_by_xpath("//*[@id='featured-books']/div/div[1]/div/div[5]/div/a[1]")
            sleep(1)
            element2.click()

            element2 = driver.find_element_by_xpath("//*[@id='featured-books']/div/div[1]/div/div[6]/div/a[1]")
            sleep(1)
            element2.click()

            sleep(1)

        # Visual checkpoint - screenshot #2
            eyes.check_window('-> {}'.format(url_addr))

# finds element by xpath, scrolls it into view and clicks "Show more" links
            element = driver.find_element_by_xpath("//*[@id='featured-books']/div/div[1]/div/div[7]/a/img")
            driver.execute_script("return arguments[0].scrollIntoView(true);", element)

            sleep(1)

            element2 = driver.find_element_by_xpath("//*[@id='featured-books']/div/div[1]/div/div[7]/div/a[1]")
            sleep(1)
            element2.click()

            element2 = driver.find_element_by_xpath("//*[@id='featured-books']/div/div[1]/div/div[8]/div/a[1]")
            sleep(1)
            element2.click()

            element2 = driver.find_element_by_xpath("//*[@id='featured-books']/div/div[1]/div/div[9]/div/a[1]")
            sleep(1)
            element2.click()

            element2 = driver.find_element_by_xpath("//*[@id='featured-books']/div/div[1]/div/div[10]/div/a[1]")
            sleep(1)
            element2.click()

            sleep(1)

        # Visual checkpoint - screenshot #3
            eyes.check_window('- webview: {}'.format(cnx_web_web))

# finds element by xpath, scrolls it into view and clicks "Show more" links
            element = driver.find_element_by_xpath("//*[@id='featured-books']/div/div[1]/div/div[11]/a/img")
            driver.execute_script("return arguments[0].scrollIntoView(true);", element)

            sleep(1)

            element2 = driver.find_element_by_xpath("//*[@id='featured-books']/div/div[1]/div/div[11]/div/a[1]")
            sleep(1)
            element2.click()

            element2 = driver.find_element_by_xpath("//*[@id='featured-books']/div/div[1]/div/div[12]/div/a[1]")
            sleep(1)
            element2.click()

            element2 = driver.find_element_by_xpath("//*[@id='featured-books']/div/div[1]/div/div[13]/div/a[1]")
            sleep(1)
            element2.click()

            element2 = driver.find_element_by_xpath("//*[@id='featured-books']/div/div[1]/div/div[14]/div/a[1]")
            sleep(1)
            element2.click()

            sleep(1)

        # Visual checkpoint - screenshot #4
            eyes.check_window('page')

# finds element by xpath, scrolls it into view and clicks "Show more" links
            element = driver.find_element_by_xpath("//*[@id='featured-books']/div/div[1]/div/div[15]/a/img")
            driver.execute_script("return arguments[0].scrollIntoView(true);", element)

            sleep(1)

            element2 = driver.find_element_by_xpath("//*[@id='featured-books']/div/div[1]/div/div[15]/div/a[1]")
            sleep(1)
            element2.click()

            element2 = driver.find_element_by_xpath("//*[@id='featured-books']/div/div[1]/div/div[16]/div/a[1]")
            sleep(1)
            element2.click()

            element2 = driver.find_element_by_xpath("//*[@id='featured-books']/div/div[1]/div/div[17]/div/a[1]")
            sleep(1)
            element2.click()

            element2 = driver.find_element_by_xpath("//*[@id='featured-books']/div/div[1]/div/div[18]/div/a[1]")
            sleep(1)
            element2.click()

            sleep(1)

        # Visual checkpoint - screenshot #5
            eyes.check_window('{}'.format(cnx_ver))

# finds element by xpath, scrolls it into view and clicks "Show more" links
            element = driver.find_element_by_xpath("//*[@id='featured-books']/div/div[1]/div/div[19]/a/img")
            driver.execute_script("return arguments[0].scrollIntoView(true);", element)

            sleep(1)

            element2 = driver.find_element_by_xpath("//*[@id='featured-books']/div/div[1]/div/div[19]/div/a[1]")
            sleep(1)
            element2.click()

            element2 = driver.find_element_by_xpath("//*[@id='featured-books']/div/div[1]/div/div[20]/div/a[1]")
            sleep(1)
            element2.click()

            element2 = driver.find_element_by_xpath("//*[@id='featured-books']/div/div[1]/div/div[21]/div/a[1]")
            sleep(1)
            element2.click()

            element2 = driver.find_element_by_xpath("//*[@id='featured-books']/div/div[1]/div/div[22]/div/a[1]")
            sleep(1)
            element2.click()

            sleep(1)

        # Visual checkpoint - screenshot #6
            eyes.check_window('-> {}'.format(url_addr))

# finds element by xpath, scrolls it into view and clicks "Show more" links
            element = driver.find_element_by_xpath("//*[@id='featured-books']/div/div[1]/div/div[23]/a/img")
            driver.execute_script("return arguments[0].scrollIntoView(true);", element)

            sleep(1)

            element2 = driver.find_element_by_xpath("//*[@id='featured-books']/div/div[1]/div/div[23]/div/a[1]")
            sleep(1)
            element2.click()

            element2 = driver.find_element_by_xpath("//*[@id='featured-books']/div/div[1]/div/div[24]/div/a[1]")
            sleep(1)
            element2.click()

            element2 = driver.find_element_by_xpath("//*[@id='featured-books']/div/div[1]/div/div[25]/div/a[1]")
            sleep(1)
            element2.click()

            element2 = driver.find_element_by_xpath("//*[@id='featured-books']/div/div[1]/div/div[26]/div/a[1]")
            sleep(1)
            element2.click()

            sleep(1)

        # Visual checkpoint - screenshot #7
            eyes.check_window('- webview: {}'.format(cnx_web_web))

# finds element by xpath, scrolls it into view and clicks "Show more" links
            element = driver.find_element_by_xpath("//*[@id='featured-books']/div/div[1]/div/div[27]/a/img")
            driver.execute_script("return arguments[0].scrollIntoView(true);", element)

            sleep(1)

            element2 = driver.find_element_by_xpath("//*[@id='featured-books']/div/div[1]/div/div[27]/div/a[1]")
            sleep(1)
            element2.click()

            element2 = driver.find_element_by_xpath("//*[@id='featured-books']/div/div[1]/div/div[28]/div/a[1]")
            sleep(1)
            element2.click()

            element2 = driver.find_element_by_xpath("//*[@id='featured-books']/div/div[1]/div/div[29]/div/a[1]")
            sleep(1)
            element2.click()

            element2 = driver.find_element_by_xpath("//*[@id='featured-books']/div/div[1]/div/div[30]/div/a[1]")
            sleep(1)
            element2.click()

            sleep(1)

        # Visual checkpoint - screenshot #8
            eyes.check_window('page')

# finds element by xpath, scrolls it into view and clicks "Show more" links
            element = driver.find_element_by_xpath("//*[@id='featured-books']/div/div[1]/div/div[31]/a/img")
            driver.execute_script("return arguments[0].scrollIntoView(true);", element)

            sleep(1)

            element2 = driver.find_element_by_xpath("//*[@id='featured-books']/div/div[1]/div/div[31]/div/a[1]")
            sleep(1)
            element2.click()

            element2 = driver.find_element_by_xpath("//*[@id='featured-books']/div/div[1]/div/div[32]/div/a[1]")
            sleep(1)
            element2.click()

            element2 = driver.find_element_by_xpath("//*[@id='featured-books']/div/div[1]/div/div[33]/div/a[1]")
            sleep(1)
            element2.click()

            element2 = driver.find_element_by_xpath("//*[@id='featured-books']/div/div[1]/div/div[34]/div/a[1]")
            sleep(1)
            element2.click()

            sleep(1)

        # Visual checkpoint - screenshot #9
            eyes.check_window('page')

# finds element by xpath, scrolls it into view and clicks "Show more" links
            element = driver.find_element_by_xpath("//*[@id='featured-books']/div/div[1]/div/div[35]/a/img")
            driver.execute_script("return arguments[0].scrollIntoView(true);", element)

            sleep(1)

            element2 = driver.find_element_by_xpath("//*[@id='featured-books']/div/div[1]/div/div[35]/div/a[1]")
            sleep(1)
            element2.click()

            element2 = driver.find_element_by_xpath("//*[@id='featured-books']/div/div[1]/div/div[36]/div/a[1]")
            sleep(1)
            element2.click()

            element2 = driver.find_element_by_xpath("//*[@id='featured-books']/div/div[1]/div/div[37]/div/a[1]")
            sleep(1)
            element2.click()

            element2 = driver.find_element_by_xpath("//*[@id='featured-books']/div/div[1]/div/div[38]/div/a[1]")
            sleep(1)
            element2.click()

            sleep(1)

        # Visual checkpoint - screenshot #10
            eyes.check_window('page')

# finds element by xpath, scrolls it into view and clicks "Show more" links
            element = driver.find_element_by_xpath("//*[@id='featured-books']/div/div[1]/div/div[39]/a/img")
            driver.execute_script("return arguments[0].scrollIntoView(true);", element)

            sleep(1)

            element2 = driver.find_element_by_xpath("//*[@id='featured-books']/div/div[1]/div/div[39]/div/a[1]")
            sleep(1)
            element2.click()

            element2 = driver.find_element_by_xpath("//*[@id='featured-books']/div/div[1]/div/div[40]/div/a[1]")
            sleep(1)
            element2.click()

            element2 = driver.find_element_by_xpath("//*[@id='featured-books']/div/div[1]/div/div[41]/div/a[1]")
            sleep(1)
            element2.click()

            element2 = driver.find_element_by_xpath("//*[@id='featured-books']/div/div[1]/div/div[42]/div/a[1]")
            sleep(1)
            element2.click()

            sleep(1)

        # Visual checkpoint - screenshot #11
            eyes.check_window('page')

# finds element by xpath, scrolls it into view and clicks "Show more" links
            element = driver.find_element_by_xpath("//*[@id='featured-books']/div/div[1]/div/div[43]/a/img")
            driver.execute_script("return arguments[0].scrollIntoView(true);", element)

            sleep(1)

            element2 = driver.find_element_by_xpath("//*[@id='featured-books']/div/div[1]/div/div[43]/div/a[1]")
            sleep(1)
            element2.click()

            element2 = driver.find_element_by_xpath("//*[@id='featured-books']/div/div[1]/div/div[44]/div/a[1]")
            sleep(1)
            element2.click()

            sleep(1)

        # Visual checkpoint - screenshot #12
            eyes.check_window('page')

# finds element by xpath, scrolls it into view and clicks "Show more" links
            element = driver.find_element_by_xpath("//*[@id='featured-books']/div/div[1]/div/div[45]/a/img")
            driver.execute_script("return arguments[0].scrollIntoView(true);", element)

            sleep(1)

            element2 = driver.find_element_by_xpath("//*[@id='featured-books']/div/div[1]/div/div[45]/div/a[1]")
            sleep(1)
            element2.click()

            sleep(1)

        # Visual checkpoint - screenshot #13
            eyes.check_window('page')

# finds element by xpath, scrolls it into view and clicks "Show more" links
            element = driver.find_element_by_xpath("//*[@id='featured-books']/div/div[2]/div/div[1]/a/img")
            driver.execute_script("return arguments[0].scrollIntoView(true);", element)

            sleep(1)

            element2 = driver.find_element_by_xpath("//*[@id='featured-books']/div/div[2]/div/div[1]/div/a[1]")
            sleep(1)
            element2.click()

            element2 = driver.find_element_by_xpath("//*[@id='featured-books']/div/div[2]/div/div[2]/div/a[1]")
            sleep(1)
            element2.click()

            sleep(1)

        # Visual checkpoint - screenshot #14

# finds element by xpath, scrolls it into view and clicks "Show more" links
            element = driver.find_element_by_xpath("//*[@id='featured-books']/div/div[2]/div/div[3]/a/img")
            driver.execute_script("return arguments[0].scrollIntoView(true);", element)

            sleep(1)

            element2 = driver.find_element_by_xpath("//*[@id='featured-books']/div/div[2]/div/div[3]/div/a[1]")
            sleep(1)
            element2.click()

            element2 = driver.find_element_by_xpath("//*[@id='featured-books']/div/div[2]/div/div[4]/div/a[1]")
            sleep(1)
            element2.click()

            sleep(1)

        # Visual checkpoint - screenshot #15
            eyes.check_window('page')

# finds element by xpath, scrolls it into view and clicks "Show more" links
            element = driver.find_element_by_xpath("//*[@id='featured-books']/div/div[2]/div/div[7]/a/img")
            driver.execute_script("return arguments[0].scrollIntoView(true);", element)

            sleep(1)

            element2 = driver.find_element_by_xpath("//*[@id='featured-books']/div/div[2]/div/div[8]/div/a[1]")
            sleep(1)
            element2.click()

            element2 = driver.find_element_by_xpath("//*[@id='featured-books']/div/div[2]/div/div[10]/div/a[1]")
            sleep(1)
            element2.click()

            sleep(1)

        # Visual checkpoint - screenshot #16
            eyes.check_window('page')

# finds element by xpath, clicks "Show more" links and scrolls to the bottom of page
            element2 = driver.find_element_by_xpath("//*[@id='featured-books']/div/div[2]/div/div[11]/div/a[1]")
            sleep(1)
            element2.click()
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            sleep(1)

            # Visual checkpoint - screenshot #17
            eyes.check_window('page')

            # End the test.
            eyes.close()

            print('---->>> HOME PAGE BOOKS TESTING IS COMPLETE FOR {} and webview: {} @ {} - CHECK EYES.APPLITOOLS.COM/APP/TEST-RESULTS <<<----'.format(cnx_ver, cnx_web_web, url_addr))

        finally:

            # Close the browser
            driver.quit()

            # If the test was aborted before eyes.close was called, ends the test as aborted
            eyes.abort_if_not_closed()