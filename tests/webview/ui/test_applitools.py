import inspect
import time

import pytest
from applitools.errors import DiffsFoundError

from pages.webview.home import Home
from tests import markers


@markers.webview
@markers.visual
@markers.nondestructive
def test_homepage_with_applitools(webview_base_url, selenium, applitools):
    # GIVEN the home page is loaded
    home = Home(selenium, webview_base_url, eyes=applitools).open()

    # WHEN the OpenStax books are removed
    # AND an applitools test is started

    # Executing the js is too fast. Causes `cannot read property errors`, so we'll wait
    # Uncomment next 4 lines to cause test to fail
    # time.sleep(1)

    # js = "var aa=document.getElementsByClassName('featured-books')[0];aa.parentNode.removeChild(aa)"

    # selenium.execute_script(js)

    # Sleep so we can see the books get removed
    # time.sleep(2)
    # In applitools the test doesn't begin until open is called
    home.start_visual_test(test_name=inspect.stack()[0][3])

    # Upload a screenshot to Applitools
    # It seems windows need to be tagged with a unique name.
    home.check_window()

    # THEN the screenshot matches

    home.stop_visual_test()
    return
