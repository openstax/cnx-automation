import backoff
import requests

from tests import markers
from pages.webview.home import Home

"""Tests pages of redirecting collections for correct rex url and page slug titles"""


@backoff.on_exception(backoff.expo, requests.exceptions.ConnectionError)
def get_url(url):
    return requests.get(url)


@markers.rex
@markers.test_case("C553080")
@markers.nondestructive
def test_redirecting_to_rex_from_within_webview(
    webview_base_url, selenium, rex_base_url, rex_released_books
):

    # GIVEN the home page and REX released books list
    for rex_book in rex_released_books:

        home = Home(selenium, webview_base_url).open()

        for cnx_book in home.featured_books.openstax_list:

            # WHEN we click on a featured book
            if cnx_book.cnx_id in rex_book:

                book_title = cnx_book.title

                title_link = home.driver.find_element_by_link_text(book_title)
                title_link.click()

                current_url = home.current_url

                # THEN we redirect to REX
                assert rex_base_url in current_url
                break

        else:
            assert False, f"{rex_book} not a rex book"


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


@markers.test_case("C600020")
@markers.slow
@markers.rex
@markers.nondestructive
def test_precalculus_uri_redirect_to_rex(webview_base_url, rex_base_url, precalculus_uri):
    # GIVEN a webview_base_url, rex_base_url and a ..._uri

    # WHEN we go to a page based on the webview_base_url and uri
    cnx_page_slug = precalculus_uri.split("/")[-1]
    cnx_url = f"{webview_base_url}{precalculus_uri}"
    response = get_url(cnx_url)

    # THEN we are redirected to rex
    assert response.url.startswith(rex_base_url)
    assert response.url.endswith(cnx_page_slug)


@markers.test_case("C600020")
@markers.slow
@markers.rex
@markers.nondestructive
def test_algebra_and_trig_uri_redirect_to_rex(webview_base_url, rex_base_url, algebra_and_trig_uri):
    # GIVEN a webview_base_url, rex_base_url and a ..._uri

    # WHEN we go to a page based on the webview_base_url and uri
    cnx_page_slug = algebra_and_trig_uri.split("/")[-1]
    cnx_url = f"{webview_base_url}{algebra_and_trig_uri}"
    response = get_url(cnx_url)

    # THEN we are redirected to rex
    assert response.url.startswith(rex_base_url)
    assert response.url.endswith(cnx_page_slug)


@markers.test_case("C559361")
@markers.slow
@markers.rex
@markers.nondestructive
def test_anatomy_and_physiology_uri_redirect_to_rex(
    webview_base_url, rex_base_url, anatomy_and_physiology_uri
):
    # GIVEN a webview_base_url, rex_base_url and an anatomy_and_physiology_uri

    # WHEN we go to a page based on the webview_base_url and uri
    cnx_page_slug = anatomy_and_physiology_uri.split("/")[-1]
    cnx_url = f"{webview_base_url}{anatomy_and_physiology_uri}"
    response = get_url(cnx_url)

    # THEN we are redirected to rex
    assert response.url.startswith(rex_base_url)
    assert response.url.endswith(cnx_page_slug)


@markers.test_case("C553520")
@markers.slow
@markers.rex
@markers.nondestructive
def test_conceptsofbiology_uri_redirect_to_rex(
    webview_base_url, rex_base_url, conceptsofbiology_uri
):
    # GIVEN a webview_base_url, rex_base_url and a conceptsofbiology_uri

    # WHEN we go to a page based on the webview_base_url and uri
    cnx_page_slug = conceptsofbiology_uri.split("/")[-1]
    cnx_url = f"{webview_base_url}{conceptsofbiology_uri}"
    response = get_url(cnx_url)

    # THEN we are redirected to rex
    assert response.url.startswith(rex_base_url)
    assert response.url.endswith(cnx_page_slug)


@markers.test_case("C615597")
@markers.slow
@markers.rex
@markers.nondestructive
def test_amer_gov_1e_uri_redirect_to_rex(webview_base_url, rex_base_url, amer_gov_1e_uri):
    # GIVEN a webview_base_url, rex_base_url and a ..._uri

    # WHEN we go to a page based on the webview_base_url and uri
    cnx_page_slug = amer_gov_1e_uri.split("/")[-1]
    cnx_url = f"{webview_base_url}{amer_gov_1e_uri}"
    response = get_url(cnx_url)

    # THEN we are redirected to rex
    assert response.url.startswith(rex_base_url)
    assert response.url.endswith(cnx_page_slug)


@markers.test_case("C615597")
@markers.slow
@markers.rex
@markers.nondestructive
def test_col_alg_with_coreq_uri_redirect_to_rex(
    webview_base_url, rex_base_url, col_alg_with_coreq_uri
):
    # GIVEN a webview_base_url, rex_base_url and a ..._uri

    # WHEN we go to a page based on the webview_base_url and uri
    cnx_page_slug = col_alg_with_coreq_uri.split("/")[-1]
    cnx_url = f"{webview_base_url}{col_alg_with_coreq_uri}"
    response = get_url(cnx_url)

    # THEN we are redirected to rex
    assert response.url.startswith(rex_base_url)
    assert response.url.endswith(cnx_page_slug)
