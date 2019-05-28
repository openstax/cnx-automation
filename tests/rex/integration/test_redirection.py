import requests

from xml.etree import ElementTree

from tests import markers
from pages.webview.home import Home


@markers.rex
@markers.nondestructive
def test_redirect_for_rex_books(webview_base_url, rex_base_url):
    # end-to-end integration test for redirecting REX-available books from webview to REX.
    # see: https://github.com/openstax/cnx/issues/344

    # GIVEN a cnx book url for which there is a REX-version
    url = f"{webview_base_url}/contents/nY32AU8S@5.1:OyK47UUK@8/16-3-Policy-Arenas"

    # WHEN requesting such URL
    response = requests.get(url)

    # THEN we redirect to REX
    assert rex_base_url in response.history[0].headers["location"]


@markers.rex
@markers.nondestructive
def test_archive_is_still_reachable(legacy_base_url, rex_base_url):
    """REX still needs a way to fetch the content from Archive without being redirected
    """
    # GIVEN an archive URL for a book
    url = f"{legacy_base_url}/contents/nY32AU8S@5.1:OyK47UUK@8/16-3-Policy-Arenas"

    # WHEN making a request to Archive
    response = requests.get(url)

    # THEN we should NOT redirect to REX
    for hist in response.history:
        assert rex_base_url not in hist.headers["location"]


@markers.rex
@markers.xfail  # until https://github.com/openstax/webview/pull/2255 is deployed
@markers.nondestructive
def test_redirecting_to_rex_from_within_webview(webview_base_url, rex_base_url, selenium):
    """Webview needs to redirect to REX when one of the featured books is a REX book.
    https://github.com/openstax/cnx/issues/401
    """
    # GIVEN the home page
    home = Home(selenium, webview_base_url).open()

    # WHEN we click on a featured book
    book = home.featured_books.get_random_openstax_book()
    book.click_title_link()

    #  THEN we redirect to REX
    assert rex_base_url in home.current_url


@markers.rex
@markers.nondestructive
def test_minimal_view_for_android_apps(webview_base_url, rex_base_url):
    """All requests for REX books that come from the Android App
    should continue to pass through to the cnx site (these requests
    are indicated by the attachment of the query-string: `?minimal=true`)
    https://github.com/openstax/cnx/issues/401
    """
    # GIVEN a cnx book url for which there is a REX-version
    url = f"{webview_base_url}/contents/nY32AU8S@5.1:OyK47UUK@8/16-3-Policy-Arenas"
    response = requests.get(url)
    assert rex_base_url in response.url

    # WHEN we include the minimal view query in the request
    minimal_view_url = f"{url}?minimal=true"
    response = requests.get(minimal_view_url)

    #  THEN we do not redirect to REX
    assert rex_base_url not in response.url


@markers.rex
@markers.nondestructive
@markers.xfail  # until we resolve and deploy https://github.com/openstax/cnx/issues/357
def test_cnx_sitemap_exclusion(rex_base_url, archive_base_url):
    """CNX books that are also available in REX should be excluded
    from the CNX sitemap.
    https://github.com/openstax/cnx/issues/357
    """
    # GIVEN a cnx book for which there is a REX-version

    # WHEN included in the REX release.json / when marked as a rex book
    releases_url = f"{rex_base_url}/rex/release.json"
    releases = requests.get(releases_url)

    first_book_uuid = [b for b in releases.json()["books"].items()][0][0]

    #  THEN we exclude the book from the CNX sitemap
    metadata_url = f"{archive_base_url}/contents/{first_book_uuid}.json"
    authors = requests.get(metadata_url).json()["authors"]
    assert 1 == len(authors)
    author = authors[0]["id"]
    sitemap_url = f"{archive_base_url}/sitemap-{author}.xml"
    sitemap = requests.get(sitemap_url)

    namespace = "http://www.sitemaps.org/schemas/sitemap/0.9"
    sitemap_tree = ElementTree.fromstring(sitemap.content)
    for collection_url in sitemap_tree.iter(f"{{{namespace}}}loc"):
        assert first_book_uuid not in collection_url.text
