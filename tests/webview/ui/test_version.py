# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from tests import markers

from pages.webview.version import Version
from pages.webview.history import History


@markers.webview
@markers.nondestructive
def test_version(webview_base_url, selenium):
    # GIVEN the webview base url and Selenium driver

    # WHEN the version and history pages have been visited
    version = Version(selenium, webview_base_url).open()
    version_parser = version.version_parser

    history = History(selenium, webview_base_url).open()
    release_parsers = history.release_parsers

    # THEN version.txt matches the JSON in the latest release,
    #      which differs from the previous release
    assert version_parser.dict == release_parsers[0].version_parser.dict
    assert (release_parsers[0].version_parser.dict != release_parsers[1].version_parser.dict or
            release_parsers[0].requirements_parser.requirements !=
            release_parsers[1].requirements_parser.requirements)
