# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from tests import markers

from pages.webview.version import Version
from pages.webview.history import History


@markers.webview
@markers.nondestructive
def test_version(webview_base_url, selenium, capsys):
    # GIVEN the webview base url and Selenium driver

    # WHEN the version and history pages have been visited
    version = Version(selenium, webview_base_url).open()
    version_parser = version.version_parser

    history = History(selenium, webview_base_url).open()
    release_parsers = history.release_parsers
    current_release_parser = release_parsers[0]
    current_version_parser = current_release_parser.version_parser

    # THEN version.txt matches the JSON in the latest release,
    #      which differs from some previous release
    with capsys.disabled():
        print('\n')
        for index in range(len(release_parsers) - 1):
            releases_ago = index + 1
            previous_release_parser = release_parsers[releases_ago]
            if not current_release_parser.has_same_versions_as(previous_release_parser):
                break
            elif index == 0:
                print('WARNING: All versions in the previous release ({previous_release_date})'
                      ' match the current release exactly. Diff based on older release.\n'.format(
                          previous_release_date=previous_release_parser.version_parser.date
                      ))

        print('Release diff from {releases_ago} release(s) ago to current release:\n'.format(
                  releases_ago=releases_ago
              ))
        print(current_release_parser.diff(previous_release_parser))

    assert version_parser.dict == current_version_parser.dict
