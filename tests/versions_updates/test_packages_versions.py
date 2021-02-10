# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from pages.webview.history import History

"""
Compares cnx packages in version.txt and history.txt on qa/staging vs production
Updated: 10/02/2021
"""


def test_packages_versions_in_version(selenium, webview_base_url, prod_url, packages_list):

    # GIVEN the webview base url and the Selenium driver

    # WHEN the version pages have been visited
    prod_history = History(selenium, prod_url).open()
    prod_release_parsers = prod_history.release_parsers
    latest_prod_release_parser = prod_release_parsers[0]
    latest_prod_version_parser = latest_prod_release_parser.version_parser.dict

    staqa_history = History(selenium, webview_base_url).open()
    staqa_release_parsers = staqa_history.release_parsers
    latest_staqa_release_parser = staqa_release_parsers[0]
    latest_staqa_version_parser = latest_staqa_release_parser.version_parser.dict

    # THEN packages in version.txt between two servers are compared
    assert any(
        latest_prod_version_parser.get(key) != latest_staqa_version_parser.get(key)
        for key in packages_list
    ), f"Packages versions in {webview_base_url} vs {prod_url} unchanged"


def test_packages_versions_in_history(selenium, webview_base_url, prod_url, packages_list):

    # GIVEN the webview base url and the Selenium driver

    # WHEN the history pages have been visited
    prod_history = History(selenium, prod_url).open()
    prod_packages = prod_history.release_parsers[0].requirements_parser.requirements_list
    prod_dict = dict([tuple(ii for ii in pack if ii is not None) for pack in prod_packages])

    staqa_history = History(selenium, webview_base_url).open()
    staqa_packages = staqa_history.release_parsers[0].requirements_parser.requirements_list
    staqa_dict = dict([tuple(ii for ii in pack if ii is not None) for pack in staqa_packages])

    # THEN packages in history.txt between two servers are compared
    assert any(
        prod_dict.get(key) != staqa_dict.get(key) for key in packages_list
    ), f"Packages versions in {webview_base_url} vs {prod_url} unchanged"
