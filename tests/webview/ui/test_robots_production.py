# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from tests import markers

from pages.robots import Robots

import pytest


@markers.webview
@markers.requires_deployment
@markers.test_case("C593158", "C593544")
@markers.nondestructive
def test_robots_production(webview_base_url, archive_base_url, robots_production_list, selenium):
    # GIVEN the webview base url, the archive base url, robots_production_list text file and the Selenium driver

    # WHEN we visit /robots.txt in webview and archive
    webview_robots = Robots(selenium, webview_base_url).open()
    # Add leading and trailing newlines to facilitate matching
    webview_robots_text = "\n{text}\n".format(text=webview_robots.text)

    archive_robots = Robots(selenium, archive_base_url).open()
    archive_robots_text = "\n{text}\n".format(text=archive_robots.text)

    # The following directives are only present on prod:
    if "//cnx.org" in webview_base_url:

        with open(robots_production_list, "r") as file:
            readf = "\n" + file.read()

            assert readf == webview_robots_text
            assert "\nUser-agent: *\nAllow: /\n" in archive_robots_text

    else:
        pytest.skip()
