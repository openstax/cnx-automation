import backoff
import requests

from xml.etree import ElementTree

from tests import markers
from pages.webview.home import Home


@backoff.on_exception(backoff.expo, requests.exceptions.ConnectionError)
def get_url(url):
    return requests.get(url)


@markers.test_case("C553086")
@markers.rex
@markers.nondestructive
def test_archive_is_still_reachable(archive_base_url, rex_base_url):
    """REX still needs a way to fetch the content from Archive without being redirected
    """
    # GIVEN an archive URL for a book
    url = f"{archive_base_url}/contents/f8zJz5tx@11.3:Pw-p-yeP@10/10-3-Phase-Transitions"

    # WHEN making a request to Archive
    response = requests.get(url)

    # THEN we should NOT redirect to REX
    for hist in response.history:
        assert rex_base_url not in hist.headers["location"]


@markers.test_case("C553080")
@markers.rex
@markers.nondestructive
def test_redirecting_to_rex_from_within_webview(
    webview_base_url, rex_base_url, selenium, redirecting_books_titles
):
    """Webview needs to redirect to REX when any of the featured books is a REX book.
    https://github.com/openstax/cnx/issues/401
    """

    for eligible_book in redirecting_books_titles:
        # GIVEN the home page
        home = Home(selenium, webview_base_url).open()

        # WHEN we click on a REX book
        for book in home.featured_books.openstax_list:

            if book.title == eligible_book:
                book.offscreen_click(book.book_cover_link)

                # THEN we redirect to REX
                assert rex_base_url in home.current_url
                break

        else:
            assert False, f"{eligible_book} not found in featured books"


@markers.rex
@markers.nondestructive
def test_minimal_view_for_android_apps(webview_base_url, rex_base_url):
    """All requests for REX books that come from the Android App
    should continue to pass through to the cnx site (these requests
    are indicated by the attachment of the query-string: `?minimal=true`)
    https://github.com/openstax/cnx/issues/401
    """
    # GIVEN a cnx book url for which there is a REX-version
    url = f"{webview_base_url}/contents/f8zJz5tx@11.3:Pw-p-yeP@10/10-3-Phase-Transitions"
    response = requests.get(url)
    assert rex_base_url in response.url

    # WHEN we include the minimal view query in the request
    minimal_view_url = f"{url}?minimal=true"
    response = requests.get(minimal_view_url)

    #  THEN we do not redirect to REX
    assert rex_base_url not in response.url


@markers.test_case("C553081")
@markers.slow
@markers.rex
@markers.nondestructive
def test_chemistry_2e_uris_redirect_to_rex(webview_base_url, rex_base_url, chemistry_2e_uri):
    # GIVEN a webview_base_url, rex_base_url and a chemistry_2e_uri

    # WHEN we go to a page based on the webview_base_url and uri
    cnx_page_slug = chemistry_2e_uri.split("/")[-1]
    cnx_url = f"{webview_base_url}{chemistry_2e_uri}"
    response = get_url(cnx_url)

    # THEN we are redirected to rex
    assert response.url.startswith(rex_base_url)
    assert response.url.endswith(cnx_page_slug)


@markers.test_case("C553085")
@markers.slow
@markers.rex
@markers.nondestructive
def test_biology_2e_uris_redirect_to_rex(webview_base_url, rex_base_url, biology_2e_uri):
    # GIVEN a webview_base_url, rex_base_url and a biology_2e_uri

    # WHEN we go to a page based on the webview_base_url and uri
    cnx_page_slug = biology_2e_uri.split("/")[-1]
    cnx_url = f"{webview_base_url}{biology_2e_uri}"
    response = get_url(cnx_url)

    # THEN we are redirected to rex
    assert response.url.startswith(rex_base_url)
    assert response.url.endswith(cnx_page_slug)
