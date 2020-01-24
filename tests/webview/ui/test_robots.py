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
def test_robots_production(
    webview_base_url, archive_base_url, robots_txt_production, selenium, webview_instance
):

    if not webview_instance == "prod":
        pytest.skip(msg="Skipping due to non-production instance")

    # GIVEN the webview base url, the archive base url, robots_production_list
    # text file and the Selenium driver

    # WHEN we visit /robots.txt in webview and archive
    webview_robots = Robots(selenium, webview_base_url).open()
    webview_robots_text = webview_robots.text

    archive_robots = Robots(selenium, archive_base_url).open()
    archive_robots_text = archive_robots.text

    # The following directives are only present on prod:
    assert robots_txt_production == webview_robots_text
    assert "User-agent: *\nAllow:" in archive_robots_text


@markers.webview
@markers.requires_deployment
@markers.test_case("C181347", "C193737")
@markers.nondestructive
def test_robots_staging(webview_base_url, archive_base_url, selenium, webview_instance):

    if not webview_instance == "staging":
        pytest.skip(msg="Skipping due to non-staging instance")

    # GIVEN the webview base url, the archive base url and the Selenium driver

    # WHEN we visit /robots.txt in webview and archive
    webview_robots = Robots(selenium, webview_base_url).open()
    webview_robots_text = webview_robots.text

    archive_robots = Robots(selenium, archive_base_url).open()
    archive_robots_text = archive_robots.text

    # THEN robots.txt has the correct content

    # The following directives are only present on staging:
    assert "User-agent: *\nDisallow: /\n" in webview_robots_text

    assert "User-agent: ScoutJet\nCrawl-delay: 10\nDisallow: /" in webview_robots_text
    assert "User-agent: Baiduspider\nCrawl-delay: 10\nDisallow: /" in webview_robots_text
    assert "User-agent: BecomeBot\nCrawl-delay: 20\nDisallow: /" in webview_robots_text
    assert "User-agent: Slurp\nCrawl-delay: 10\nDisallow: /" in webview_robots_text

    assert "User-agent: *\nDisallow: /" in archive_robots_text
