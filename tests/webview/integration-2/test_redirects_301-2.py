import backoff
import requests

from tests import markers

"""Tests the redirect code and that the new url is that of rex"""


@backoff.on_exception(backoff.expo, requests.exceptions.ConnectionError)
def get_url(url):
    return requests.get(url)


@markers.test_case("C568716")
@markers.slow
@markers.rex
@markers.nondestructive
def test_algebra_and_trig_uri_redirect_to_rex(webview_base_url, rex_base_url, algebra_and_trig_uri):
    # GIVEN a webview_base_url, rex_base_url and a col..._uri

    # WHEN we go to a page based on the webview_base_url and uri
    cnx_url = f"{webview_base_url}{algebra_and_trig_uri}"
    response = requests.get(cnx_url, allow_redirects=False)

    # THEN we are redirected to rex
    assert rex_base_url in response.headers["Location"]
    assert 301 == response.status_code


@markers.test_case("C568716")
@markers.slow
@markers.rex
@markers.nondestructive
def test_anatomy_and_physiology_uri_redirect_to_rex(
    webview_base_url, rex_base_url, anatomy_and_physiology_uri
):
    # GIVEN a webview_base_url, rex_base_url and an anatomy_and_physiology_uri

    # WHEN we go to a page based on the webview_base_url and uri
    cnx_url = f"{webview_base_url}{anatomy_and_physiology_uri}"
    response = requests.get(cnx_url, allow_redirects=False)

    # THEN we are redirected to rex
    assert rex_base_url in response.headers["Location"]
    assert 301 == response.status_code


@markers.test_case("C568716")
@markers.slow
@markers.rex
@markers.nondestructive
def test_conceptsofbiology_uri_redirect_to_rex(
    webview_base_url, rex_base_url, conceptsofbiology_uri
):
    # GIVEN a webview_base_url, rex_base_url and a conceptsofbiology_uri

    # WHEN we go to a page based on the webview_base_url and uri
    cnx_url = f"{webview_base_url}{conceptsofbiology_uri}"
    response = requests.get(cnx_url, allow_redirects=False)

    # THEN we are redirected to rex
    assert rex_base_url in response.headers["Location"]
    assert 301 == response.status_code


@markers.test_case("C568716")
@markers.slow
@markers.rex
@markers.nondestructive
def test_precalculus_uri_redirect_to_rex(webview_base_url, rex_base_url, precalculus_uri):
    # GIVEN a webview_base_url, rex_base_url and a col..._uri

    # WHEN we go to a page based on the webview_base_url and uri
    cnx_url = f"{webview_base_url}{precalculus_uri}"
    response = requests.get(cnx_url, allow_redirects=False)

    # THEN we are redirected to rex
    assert rex_base_url in response.headers["Location"]
    assert 301 == response.status_code


@markers.test_case("C568716")
@markers.slow
@markers.rex
@markers.nondestructive
def test_amer_gov_1e_uri_redirect_to_rex(webview_base_url, rex_base_url, amer_gov_1e_uri):
    # GIVEN a webview_base_url, rex_base_url and a col..._uri

    # WHEN we go to a page based on the webview_base_url and uri
    cnx_url = f"{webview_base_url}{amer_gov_1e_uri}"
    response = requests.get(cnx_url, allow_redirects=False)

    # THEN we are redirected to rex
    assert rex_base_url in response.headers["Location"]
    assert 301 == response.status_code


@markers.test_case("C568716")
@markers.slow
@markers.rex
@markers.nondestructive
def test_col_alg_with_coreq_uri_redirect_to_rex(
    webview_base_url, rex_base_url, col_alg_with_coreq_uri
):
    # GIVEN a webview_base_url, rex_base_url and a col..._uri

    # WHEN we go to a page based on the webview_base_url and uri
    cnx_url = f"{webview_base_url}{col_alg_with_coreq_uri}"
    response = requests.get(cnx_url, allow_redirects=False)

    # THEN we are redirected to rex
    assert rex_base_url in response.headers["Location"]
    assert 301 == response.status_code
