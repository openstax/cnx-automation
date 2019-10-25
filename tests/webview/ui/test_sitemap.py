# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import requests
import lxml.etree

from tests import markers

from pages.webview.sitemap_index import SitemapIndex


def xor(a, b):
    return bool(a) ^ bool(b)


def xnor(a, b):
    # See truth table: https://en.wikipedia.org/wiki/XNOR_gate
    return not xor(a, b)


@markers.webview
@markers.smoke
@markers.requires_varnish_routing
@markers.test_case("C205363")
@markers.parametrize(
    "author_username,author_name",
    [("Beatrice_Riviere", "Beatrice Riviere"), ("richb", "Richard Baraniuk")],
)
@markers.nondestructive
def test_sitemap_is_segmented_by_author(webview_base_url, selenium, author_username, author_name):
    # GIVEN the webview base url, the Selenium driver,
    #       the sitemap index, and an author's username and name
    sitemap_index = SitemapIndex(selenium, webview_base_url).open()

    # WHEN we visit the author's sitemap
    sitemap_region = sitemap_index.find_sitemap_region(author_username)
    sitemap = sitemap_region.open()

    # THEN all the content in that sitemap is by that author
    # To make this test not take forever (and because we were having trouble
    # getting some of the modules to even load), we only test one of the modules
    url_region = sitemap.url_regions[0]
    content = url_region.open()
    assert author_name in content.content_header.authors


@markers.webview
@markers.smoke
@markers.requires_varnish_routing
@markers.nondestructive
@markers.parametrize(
    "author, uuid, should_be_present",
    [  # case parameters for the removal of derived content
        (
            "cnxbio_espanol",
            # Conceptos de Biología
            "e7a016d3-91fc-4ba0-9e05-a33e986f3d94",
            False,
        ),
        # case parameters for keeping OpenStax derived content (i.e. REX book)
        (
            "OpenStaxCollege",
            # Introduction to Sociology 2e
            "02040312-72c8-441e-a685-20e9333f3e1d",
            True,
        ),
    ],
)
def test_derived_copies_in_sitemap(webview_base_url, author, uuid, should_be_present):
    # As OpenStax, I want to remove all derived copies except OpenStax
    # books from the content, so that we begin the transition away from cnx.
    # see: https://github.com/openstax/cnx/issues/727

    # GIVEN a "sitemap" URL
    # note, this is discovered by the spider as part of /sitemap_index.xml
    url = f"{webview_base_url}/sitemap-{author}.xml"

    # WHEN a spider requests the specific author's sitemap
    response = requests.get(url)
    response.raise_for_status()
    xml = lxml.etree.fromstring(response.content)
    #: give the text for the the element named 'loc' in any namespace
    urls = xml.xpath("//*[local-name()='loc']/text()")

    # THEN non-OpenStax derived copies have been removed
    # while OpenStax books remain
    found_url = [url for url in urls if uuid in url]
    # This essentially tries to check if it should or shouldn't be found,
    # & return the correct boolean value based on it being or not being found.
    assert xnor(should_be_present, found_url)
