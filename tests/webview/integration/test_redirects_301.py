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
def test_chemistry_2e_uris_redirect_to_rex(webview_base_url, rex_base_url, chemistry_2e_uri):
    # GIVEN a webview_base_url, rex_base_url and a chemistry_2e_uri

    # WHEN we go to a page based on the webview_base_url and uri
    cnx_url = f"{webview_base_url}{chemistry_2e_uri}"
    response = requests.get(cnx_url, allow_redirects=False)

    # THEN we are redirected to rex
    assert rex_base_url in response.headers["Location"]
    assert 301 == response.status_code


@markers.test_case("C568716")
@markers.slow
@markers.rex
@markers.nondestructive
def test_biology_2e_uris_redirect_to_rex(webview_base_url, rex_base_url, biology_2e_uri):
    # GIVEN a webview_base_url, rex_base_url and a biology_2e_uri

    # WHEN we go to a page based on the webview_base_url and uri
    cnx_url = f"{webview_base_url}{biology_2e_uri}"
    response = requests.get(cnx_url, allow_redirects=False)

    # THEN we are redirected to rex
    assert rex_base_url in response.headers["Location"]
    assert 301 == response.status_code


@markers.test_case("C568716")
@markers.slow
@markers.rex
@markers.nondestructive
def test_microbiology_uris_redirect_to_rex(webview_base_url, rex_base_url, microbiology_uri):
    # GIVEN a webview_base_url, rex_base_url and a microbiology_uri

    # WHEN we go to a page based on the webview_base_url and uri
    cnx_url = f"{webview_base_url}{microbiology_uri}"
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
def test_astronomy_uri_redirect_to_rex(webview_base_url, rex_base_url, astronomy_uri):
    # GIVEN a webview_base_url, rex_base_url and an astronomy_uri

    # WHEN we go to a page based on the webview_base_url and uri
    cnx_url = f"{webview_base_url}{astronomy_uri}"
    response = requests.get(cnx_url, allow_redirects=False)

    # THEN we are redirected to rex
    assert rex_base_url in response.headers["Location"]
    assert 301 == response.status_code


@markers.test_case("C568716")
@markers.slow
@markers.rex
@markers.nondestructive
def test_biology_ap_uri_redirect_to_rex(webview_base_url, rex_base_url, biology_ap_uri):
    # GIVEN a webview_base_url, rex_base_url and a biology_ap_uri

    # WHEN we go to a page based on the webview_base_url and uri
    cnx_url = f"{webview_base_url}{biology_ap_uri}"
    response = requests.get(cnx_url, allow_redirects=False)

    # THEN we are redirected to rex
    assert rex_base_url in response.headers["Location"]
    assert 301 == response.status_code


@markers.test_case("C568716")
@markers.slow
@markers.rex
@markers.nondestructive
def test_college_physics_ap_courses_uri_redirect_to_rex(
    webview_base_url, rex_base_url, college_physics_ap_courses_uri
):
    # GIVEN a webview_base_url, rex_base_url and a college_physics_ap_courses_uri

    # WHEN we go to a page based on the webview_base_url and uri
    cnx_url = f"{webview_base_url}{college_physics_ap_courses_uri}"
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
def test_college_physics_uri_redirect_to_rex(webview_base_url, rex_base_url, college_physics_uri):
    # GIVEN a webview_base_url, rex_base_url and a college_physics_uri

    # WHEN we go to a page based on the webview_base_url and uri
    cnx_url = f"{webview_base_url}{college_physics_uri}"
    response = requests.get(cnx_url, allow_redirects=False)

    # THEN we are redirected to rex
    assert rex_base_url in response.headers["Location"]
    assert 301 == response.status_code


@markers.test_case("C568716")
@markers.slow
@markers.rex
@markers.nondestructive
def test_chemistry_atoms_first_2e_uri_redirect_to_rex(
    webview_base_url, rex_base_url, chemistry_atoms_first_2e_uri
):
    # GIVEN a webview_base_url, rex_base_url and a chemistry_atoms_first_2e_uri

    # WHEN we go to a page based on the webview_base_url and uri
    cnx_url = f"{webview_base_url}{chemistry_atoms_first_2e_uri}"
    response = requests.get(cnx_url, allow_redirects=False)

    # THEN we are redirected to rex
    assert rex_base_url in response.headers["Location"]
    assert 301 == response.status_code


@markers.test_case("C568716")
@markers.slow
@markers.rex
@markers.nondestructive
def test_calculus_vol_1_uri_redirect_to_rex(webview_base_url, rex_base_url, calculus_vol_1_uri):
    # GIVEN a webview_base_url, rex_base_url and a calculus_vol_1_uri

    # WHEN we go to a page based on the webview_base_url and uri
    cnx_url = f"{webview_base_url}{calculus_vol_1_uri}"
    response = requests.get(cnx_url, allow_redirects=False)

    # THEN we are redirected to rex
    assert rex_base_url in response.headers["Location"]
    assert 301 == response.status_code


@markers.test_case("C568716")
@markers.slow
@markers.rex
@markers.nondestructive
def test_calculus_vol_2_uri_redirect_to_rex(webview_base_url, rex_base_url, calculus_vol_2_uri):
    # GIVEN a webview_base_url, rex_base_url and a calculus_vol_2_uri

    # WHEN we go to a page based on the webview_base_url and uri
    cnx_url = f"{webview_base_url}{calculus_vol_2_uri}"
    response = requests.get(cnx_url, allow_redirects=False)

    # THEN we are redirected to rex
    assert rex_base_url in response.headers["Location"]
    assert 301 == response.status_code


@markers.test_case("C568716")
@markers.slow
@markers.rex
@markers.nondestructive
def test_calculus_vol_3_uri_redirect_to_rex(webview_base_url, rex_base_url, calculus_vol_3_uri):
    # GIVEN a webview_base_url, rex_base_url and a calculus_vol_3_uri

    # WHEN we go to a page based on the webview_base_url and uri
    cnx_url = f"{webview_base_url}{calculus_vol_3_uri}"
    response = requests.get(cnx_url, allow_redirects=False)

    # THEN we are redirected to rex
    assert rex_base_url in response.headers["Location"]
    assert 301 == response.status_code


@markers.test_case("C568716")
@markers.slow
@markers.rex
@markers.nondestructive
def test_univ_phys_1_uri_redirect_to_rex(webview_base_url, rex_base_url, univ_phys_1_uri):
    # GIVEN a webview_base_url, rex_base_url and a univ_phys_1_uri

    # WHEN we go to a page based on the webview_base_url and uri
    cnx_url = f"{webview_base_url}{univ_phys_1_uri}"
    response = requests.get(cnx_url, allow_redirects=False)

    # THEN we are redirected to rex
    assert rex_base_url in response.headers["Location"]
    assert 301 == response.status_code


@markers.test_case("C568716")
@markers.slow
@markers.rex
@markers.nondestructive
def test_univ_phys_2_uri_redirect_to_rex(webview_base_url, rex_base_url, univ_phys_2_uri):
    # GIVEN a webview_base_url, rex_base_url and a univ_phys_2_uri

    # WHEN we go to a page based on the webview_base_url and uri
    cnx_url = f"{webview_base_url}{univ_phys_2_uri}"
    response = requests.get(cnx_url, allow_redirects=False)

    # THEN we are redirected to rex
    assert rex_base_url in response.headers["Location"]
    assert 301 == response.status_code


@markers.test_case("C568716")
@markers.slow
@markers.rex
@markers.nondestructive
def test_univ_phys_3_uri_redirect_to_rex(webview_base_url, rex_base_url, univ_phys_3_uri):
    # GIVEN a webview_base_url, rex_base_url and a univ_phys_3_uri

    # WHEN we go to a page based on the webview_base_url and uri
    cnx_url = f"{webview_base_url}{univ_phys_3_uri}"
    response = requests.get(cnx_url, allow_redirects=False)

    # THEN we are redirected to rex
    assert rex_base_url in response.headers["Location"]
    assert 301 == response.status_code


@markers.test_case("C568716")
@markers.slow
@markers.rex
@markers.nondestructive
def test_american_government_2e_uri_redirect_to_rex(
    webview_base_url, rex_base_url, american_government_2e_uri
):
    # GIVEN a webview_base_url, rex_base_url and an american_government_2e_uri

    # WHEN we go to a page based on the webview_base_url and uri
    cnx_url = f"{webview_base_url}{american_government_2e_uri}"
    response = requests.get(cnx_url, allow_redirects=False)

    # THEN we are redirected to rex
    assert rex_base_url in response.headers["Location"]
    assert 301 == response.status_code


@markers.test_case("C568716")
@markers.slow
@markers.rex
@markers.nondestructive
def test_introductory_business_statistics_uri_redirect_to_rex(
    webview_base_url, rex_base_url, introductory_business_statistics_uri
):
    # GIVEN a webview_base_url, rex_base_url and a introductory_business_statistics_uri

    # WHEN we go to a page based on the webview_base_url and uri
    cnx_url = f"{webview_base_url}{introductory_business_statistics_uri}"
    response = requests.get(cnx_url, allow_redirects=False)

    # THEN we are redirected to rex
    assert rex_base_url in response.headers["Location"]
    assert 301 == response.status_code


@markers.test_case("C568716")
@markers.slow
@markers.rex
@markers.nondestructive
def test_introductory_statistics_uri_redirect_to_rex(
    webview_base_url, rex_base_url, introductory_statistics_uri
):
    # GIVEN a webview_base_url, rex_base_url and an introductory_statistics_uri

    # WHEN we go to a page based on the webview_base_url and uri
    cnx_url = f"{webview_base_url}{introductory_statistics_uri}"
    response = requests.get(cnx_url, allow_redirects=False)

    # THEN we are redirected to rex
    assert rex_base_url in response.headers["Location"]
    assert 301 == response.status_code


@markers.test_case("C568716")
@markers.slow
@markers.rex
@markers.nondestructive
def test_principles_of_accounting_1_uri_redirect_to_rex(
    webview_base_url, rex_base_url, principles_of_accounting_1_uri
):
    # GIVEN a webview_base_url, rex_base_url and a principles_of_accounting_vol_1_uri

    # WHEN we go to a page based on the webview_base_url and uri
    cnx_url = f"{webview_base_url}{principles_of_accounting_1_uri}"
    response = requests.get(cnx_url, allow_redirects=False)

    # THEN we are redirected to rex
    assert rex_base_url in response.headers["Location"]
    assert 301 == response.status_code


@markers.test_case("C568716")
@markers.slow
@markers.rex
@markers.nondestructive
def test_principles_of_accounting_2_uri_redirect_to_rex(
    webview_base_url, rex_base_url, principles_of_accounting_2_uri
):
    # GIVEN a webview_base_url, rex_base_url and a principles_of_accounting_vol_2_uri

    # WHEN we go to a page based on the webview_base_url and uri
    cnx_url = f"{webview_base_url}{principles_of_accounting_2_uri}"
    response = requests.get(cnx_url, allow_redirects=False)

    # THEN we are redirected to rex
    assert rex_base_url in response.headers["Location"]
    assert 301 == response.status_code


@markers.test_case("C568716")
@markers.slow
@markers.rex
@markers.nondestructive
def test_us_history_uri_redirect_to_rex(webview_base_url, rex_base_url, us_history_uri):
    # GIVEN a webview_base_url, rex_base_url and a us_history_uri

    # WHEN we go to a page based on the webview_base_url and uri
    cnx_url = f"{webview_base_url}{us_history_uri}"
    response = requests.get(cnx_url, allow_redirects=False)

    # THEN we are redirected to rex
    assert rex_base_url in response.headers["Location"]
    assert 301 == response.status_code


@markers.test_case("C568716")
@markers.slow
@markers.rex
@markers.nondestructive
def test_economics_2e_uri_redirect_to_rex(webview_base_url, rex_base_url, economics_2e_uri):
    # GIVEN a webview_base_url, rex_base_url and a col..._uri

    # WHEN we go to a page based on the webview_base_url and uri
    cnx_url = f"{webview_base_url}{economics_2e_uri}"
    response = requests.get(cnx_url, allow_redirects=False)

    # THEN we are redirected to rex
    assert rex_base_url in response.headers["Location"]
    assert 301 == response.status_code


@markers.test_case("C568716")
@markers.slow
@markers.rex
@markers.nondestructive
def test_microeconomics_2e_uri_redirect_to_rex(
    webview_base_url, rex_base_url, microeconomics_2e_uri
):
    # GIVEN a webview_base_url, rex_base_url and a col..._uri

    # WHEN we go to a page based on the webview_base_url and uri
    cnx_url = f"{webview_base_url}{microeconomics_2e_uri}"
    response = requests.get(cnx_url, allow_redirects=False)

    # THEN we are redirected to rex
    assert rex_base_url in response.headers["Location"]
    assert 301 == response.status_code


@markers.test_case("C568716")
@markers.slow
@markers.rex
@markers.nondestructive
def test_macroeconomics_2e_uri_redirect_to_rex(
    webview_base_url, rex_base_url, macroeconomics_2e_uri
):
    # GIVEN a webview_base_url, rex_base_url and a col..._uri

    # WHEN we go to a page based on the webview_base_url and uri
    cnx_url = f"{webview_base_url}{macroeconomics_2e_uri}"
    response = requests.get(cnx_url, allow_redirects=False)

    # THEN we are redirected to rex
    assert rex_base_url in response.headers["Location"]
    assert 301 == response.status_code


@markers.otto5
@markers.test_case("C568716")
@markers.slow
@markers.rex
@markers.nondestructive
def test_entrepreneurship_uri_redirect_to_rex(webview_base_url, rex_base_url, entrepreneurship_uri):
    # GIVEN a webview_base_url, rex_base_url and a col..._uri

    # WHEN we go to a page based on the webview_base_url and uri
    cnx_url = f"{webview_base_url}{entrepreneurship_uri}"
    response = requests.get(cnx_url, allow_redirects=False)

    # THEN we are redirected to rex
    assert rex_base_url in response.headers["Location"]
    assert 301 == response.status_code


@markers.test_case("C568716")
@markers.slow
@markers.rex
@markers.nondestructive
def test_sociology_2e_uri_redirect_to_rex(webview_base_url, rex_base_url, sociology_2e_uri):
    # GIVEN a webview_base_url, rex_base_url and a col..._uri

    # WHEN we go to a page based on the webview_base_url and uri
    cnx_url = f"{webview_base_url}{sociology_2e_uri}"
    response = requests.get(cnx_url, allow_redirects=False)

    # THEN we are redirected to rex
    assert rex_base_url in response.headers["Location"]
    assert 301 == response.status_code


@markers.test_case("C568716")
@markers.slow
@markers.rex
@markers.nondestructive
def test_intro_business_uri_redirect_to_rex(webview_base_url, rex_base_url, intro_business_uri):
    # GIVEN a webview_base_url, rex_base_url and a col..._uri

    # WHEN we go to a page based on the webview_base_url and uri
    cnx_url = f"{webview_base_url}{intro_business_uri}"
    response = requests.get(cnx_url, allow_redirects=False)

    # THEN we are redirected to rex
    assert rex_base_url in response.headers["Location"]
    assert 301 == response.status_code


@markers.test_case("C568716")
@markers.slow
@markers.rex
@markers.nondestructive
def test_business_ethics_uri_redirect_to_rex(webview_base_url, rex_base_url, business_ethics_uri):
    # GIVEN a webview_base_url, rex_base_url and a col..._uri

    # WHEN we go to a page based on the webview_base_url and uri
    cnx_url = f"{webview_base_url}{business_ethics_uri}"
    response = requests.get(cnx_url, allow_redirects=False)

    # THEN we are redirected to rex
    assert rex_base_url in response.headers["Location"]
    assert 301 == response.status_code


@markers.test_case("C568716")
@markers.slow
@markers.rex
@markers.nondestructive
def test_principles_of_mgnt_uri_redirect_to_rex(
    webview_base_url, rex_base_url, principles_of_mgnt_uri
):
    # GIVEN a webview_base_url, rex_base_url and a col..._uri

    # WHEN we go to a page based on the webview_base_url and uri
    cnx_url = f"{webview_base_url}{principles_of_mgnt_uri}"
    response = requests.get(cnx_url, allow_redirects=False)

    # THEN we are redirected to rex
    assert rex_base_url in response.headers["Location"]
    assert 301 == response.status_code


@markers.test_case("C568716")
@markers.slow
@markers.rex
@markers.nondestructive
def test_organizational_behavior_uri_redirect_to_rex(
    webview_base_url, rex_base_url, organizational_behavior_uri
):
    # GIVEN a webview_base_url, rex_base_url and a col..._uri

    # WHEN we go to a page based on the webview_base_url and uri
    cnx_url = f"{webview_base_url}{organizational_behavior_uri}"
    response = requests.get(cnx_url, allow_redirects=False)

    # THEN we are redirected to rex
    assert rex_base_url in response.headers["Location"]
    assert 301 == response.status_code
