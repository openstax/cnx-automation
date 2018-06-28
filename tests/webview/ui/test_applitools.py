import inspect
import time

import pytest
from applitools.errors import DiffsFoundError

from pages.legacy.home import Home
from tests import markers


@markers.webview
@markers.nondestructive
def test_homepage_with_applitools(webview_base_url, selenium, applitools):
    # GIVEN the home page is loaded
    home = Home(selenium, webview_base_url).open()

    # WHEN the OpenStax books are removed
    # AND an applitools test is started

    # Executing the js is too fast. Causes `cannot read property errors`, so we'll wait
    time.sleep(1)

    js = "var aa=document.getElementsByClassName('featured-books')[0];aa.parentNode.removeChild(aa)"

    selenium.execute_script(js)

    # Sleep so we can see the books get removed
    time.sleep(2)
    # In applitools the test doesn't begin until open is called
    applitools.open(driver=selenium, app_name='webview', test_name=inspect.stack()[0][3])
    applitools.force_full_page_screenshot = True

    # Upload a screenshot to Applitools
    # It seems windows need to be tagged with a unique name.
    applitools.check_window('Home')

    # THEN stop the applitools test
    try:
        applitools.close()
    except DiffsFoundError as e:
        pytest.fail(str(e))

    return
