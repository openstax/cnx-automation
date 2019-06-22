import inspect

import pytest
from applitools.common import DiffsFoundError, MatchLevel
from applitools.selenium import StitchMode

from tests import markers
from pages.webview.home import Home


@markers.webview
@markers.visual
@markers.nondestructive
@markers.parametrize("width, height", [(1400, 820)])
def test_home_page_full_strict(
    applitools, webview_base_url, webview_instance, selenium, width, height
):
    if webview_instance == "qa":
        pytest.skip(f"Skipping test on {webview_instance}")

    applitools.match_level = MatchLevel.STRICT
    applitools.force_full_page_screenshot = True
    applitools.stitch_mode = StitchMode.CSS
    applitools.hide_scrollbars = True

    Home(selenium, webview_base_url).open()

    applitools.open(
        driver=selenium,
        app_name="webview",
        test_name=inspect.stack()[0][3],
        viewport_size={"width": width, "height": height},
    )

    applitools.check_window("Home Full Page")

    try:
        applitools.close()
    except DiffsFoundError as e:
        pytest.fail(f"{e.message}")
    finally:
        applitools.abort_if_not_closed()


@markers.webview
@markers.visual
@markers.nondestructive
@markers.parametrize("width, height", [(1400, 820)])
def test_home_openstax_books_show_more_strict(
    applitools, webview_base_url, selenium, webview_instance, width, height
):

    if webview_instance == "qa":
        pytest.skip(f"Skipping test on {webview_instance}")

    applitools.match_level = MatchLevel.STRICT

    home = Home(selenium, webview_base_url).open()

    applitools.open(
        driver=selenium,
        app_name="webview",
        test_name=inspect.stack()[0][3],
        viewport_size={"width": width, "height": height},
    )

    openstax_books = home.featured_books.openstax_list

    for i in range(len(openstax_books)):
        openstax_books[i].click_show_more()

        if i % 4 == 0:
            applitools.check_window(f"Home {i}")

    try:
        applitools.close()
    except DiffsFoundError as e:
        pytest.fail(f"{e.message}")
    finally:
        applitools.abort_if_not_closed()
