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


@markers.test_case("C616758")
@markers.slow
@markers.rex
@markers.nondestructive
def test_chemistry_uris_redirect_to_rex(webview_base_url, rex_base_url, chemistry_uri):
    # GIVEN a webview_base_url, rex_base_url and a chemistry_uri

    # WHEN we go to a page based on the webview_base_url and uri
    cnx_page_slug = chemistry_uri.split("/")[-1]
    cnx_url = f"{webview_base_url}{chemistry_uri}"
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


@markers.test_case("C618400")
@markers.slow
@markers.rex
@markers.nondestructive
def test_biology_uris_redirect_to_rex(webview_base_url, rex_base_url, biology_uri):
    # GIVEN a webview_base_url, rex_base_url and a biology_uri

    # WHEN we go to a page based on the webview_base_url and uri
    cnx_page_slug = biology_uri.split("/")[-1]
    cnx_url = f"{webview_base_url}{biology_uri}"
    response = get_url(cnx_url)

    # THEN we are redirected to rex
    assert response.url.startswith(rex_base_url)
    assert response.url.endswith(cnx_page_slug)


@markers.test_case("C553519")
@markers.slow
@markers.rex
@markers.nondestructive
def test_microbiology_uris_redirect_to_rex(webview_base_url, rex_base_url, microbiology_uri):
    # GIVEN a webview_base_url, rex_base_url and a microbiology_uri

    # WHEN we go to a page based on the webview_base_url and uri
    cnx_page_slug = microbiology_uri.split("/")[-1]
    cnx_url = f"{webview_base_url}{microbiology_uri}"
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


@markers.test_case("C559358")
@markers.slow
@markers.rex
@markers.nondestructive
def test_astronomy_uri_redirect_to_rex(webview_base_url, rex_base_url, astronomy_uri):
    # GIVEN a webview_base_url, rex_base_url and an astronomy_uri

    # WHEN we go to a page based on the webview_base_url and uri
    cnx_page_slug = astronomy_uri.split("/")[-1]
    cnx_url = f"{webview_base_url}{astronomy_uri}"
    response = get_url(cnx_url)

    # THEN we are redirected to rex
    assert response.url.startswith(rex_base_url)
    assert response.url.endswith(cnx_page_slug)


@markers.test_case("C559363")
@markers.slow
@markers.rex
@markers.nondestructive
def test_biology_ap_uri_redirect_to_rex(webview_base_url, rex_base_url, biology_ap_uri):
    # GIVEN a webview_base_url, rex_base_url and a biology_ap_uri

    # WHEN we go to a page based on the webview_base_url and uri
    cnx_page_slug = biology_ap_uri.split("/")[-1]
    cnx_url = f"{webview_base_url}{biology_ap_uri}"
    response = get_url(cnx_url)

    # THEN we are redirected to rex
    assert response.url.startswith(rex_base_url)
    assert response.url.endswith(cnx_page_slug)


@markers.test_case("C559362")
@markers.slow
@markers.rex
@markers.nondestructive
def test_college_physics_ap_courses_uri_redirect_to_rex(
    webview_base_url, rex_base_url, college_physics_ap_courses_uri
):
    # GIVEN a webview_base_url, rex_base_url and a college_physics_ap_courses_uri

    # WHEN we go to a page based on the webview_base_url and uri
    cnx_page_slug = college_physics_ap_courses_uri.split("/")[-1]
    cnx_url = f"{webview_base_url}{college_physics_ap_courses_uri}"
    response = get_url(cnx_url)

    # THEN we are redirected to rex
    assert response.url.startswith(rex_base_url)
    assert response.url.endswith(cnx_page_slug)


@markers.test_case("C559360")
@markers.slow
@markers.rex
@markers.nondestructive
def test_college_physics_uri_redirect_to_rex(webview_base_url, rex_base_url, college_physics_uri):
    # GIVEN a webview_base_url, rex_base_url and a college_physics_uri

    # WHEN we go to a page based on the webview_base_url and uri
    cnx_page_slug = college_physics_uri.split("/")[-1]
    cnx_url = f"{webview_base_url}{college_physics_uri}"
    response = get_url(cnx_url)

    # THEN we are redirected to rex
    assert response.url.startswith(rex_base_url)
    assert response.url.endswith(cnx_page_slug)


@markers.test_case("C559359")
@markers.slow
@markers.rex
@markers.nondestructive
def test_chemistry_atoms_first_2e_uri_redirect_to_rex(
    webview_base_url, rex_base_url, chemistry_atoms_first_2e_uri
):
    # GIVEN a webview_base_url, rex_base_url and a chemistry_atoms_first_2e_uri

    # WHEN we go to a page based on the webview_base_url and uri
    cnx_page_slug = chemistry_atoms_first_2e_uri.split("/")[-1]
    cnx_url = f"{webview_base_url}{chemistry_atoms_first_2e_uri}"
    response = get_url(cnx_url)

    # THEN we are redirected to rex
    assert response.url.startswith(rex_base_url)
    assert response.url.endswith(cnx_page_slug)


@markers.test_case("C616758")
@markers.slow
@markers.rex
@markers.nondestructive
def test_chemistry_atoms_first_uri_redirect_to_rex(
    webview_base_url, rex_base_url, chemistry_atoms_first_uri
):
    # GIVEN a webview_base_url, rex_base_url and a chemistry_atoms_first_uri

    # WHEN we go to a page based on the webview_base_url and uri
    cnx_page_slug = chemistry_atoms_first_uri.split("/")[-1]
    cnx_url = f"{webview_base_url}{chemistry_atoms_first_uri}"
    response = get_url(cnx_url)

    # THEN we are redirected to rex
    assert response.url.startswith(rex_base_url)
    assert response.url.endswith(cnx_page_slug)


@markers.test_case("C568292")
@markers.slow
@markers.rex
@markers.nondestructive
def test_calculus_vol_1_uri_redirect_to_rex(webview_base_url, rex_base_url, calculus_vol_1_uri):
    # GIVEN a webview_base_url, rex_base_url and a calculus_vol_1_uri

    # WHEN we go to a page based on the webview_base_url and uri
    cnx_page_slug = calculus_vol_1_uri.split("/")[-1]
    cnx_url = f"{webview_base_url}{calculus_vol_1_uri}"
    response = get_url(cnx_url)

    # THEN we are redirected to rex
    assert response.url.startswith(rex_base_url)
    assert response.url.endswith(cnx_page_slug)


@markers.test_case("C568293")
@markers.slow
@markers.rex
@markers.nondestructive
def test_calculus_vol_2_uri_redirect_to_rex(webview_base_url, rex_base_url, calculus_vol_2_uri):
    # GIVEN a webview_base_url, rex_base_url and a calculus_vol_2_uri

    # WHEN we go to a page based on the webview_base_url and uri
    cnx_page_slug = calculus_vol_2_uri.split("/")[-1]
    cnx_url = f"{webview_base_url}{calculus_vol_2_uri}"
    response = get_url(cnx_url)

    # THEN we are redirected to rex
    assert response.url.startswith(rex_base_url)
    assert response.url.endswith(cnx_page_slug)


@markers.test_case("C568294")
@markers.slow
@markers.rex
@markers.nondestructive
def test_calculus_vol_3_uri_redirect_to_rex(webview_base_url, rex_base_url, calculus_vol_3_uri):
    # GIVEN a webview_base_url, rex_base_url and a calculus_vol_3_uri

    # WHEN we go to a page based on the webview_base_url and uri
    cnx_page_slug = calculus_vol_3_uri.split("/")[-1]
    cnx_url = f"{webview_base_url}{calculus_vol_3_uri}"
    response = get_url(cnx_url)

    # THEN we are redirected to rex
    assert response.url.startswith(rex_base_url)
    assert response.url.endswith(cnx_page_slug)


@markers.test_case("C568295")
@markers.slow
@markers.rex
@markers.nondestructive
def test_univ_phys_1_uri_redirect_to_rex(webview_base_url, rex_base_url, univ_phys_1_uri):
    # GIVEN a webview_base_url, rex_base_url and a univ_phys_1_uri

    # WHEN we go to a page based on the webview_base_url and uri
    cnx_page_slug = univ_phys_1_uri.split("/")[-1]
    cnx_url = f"{webview_base_url}{univ_phys_1_uri}"
    response = get_url(cnx_url)

    # THEN we are redirected to rex
    assert response.url.startswith(rex_base_url)
    assert response.url.endswith(cnx_page_slug)


@markers.test_case("C568296")
@markers.slow
@markers.rex
@markers.nondestructive
def test_univ_phys_2_uri_redirect_to_rex(webview_base_url, rex_base_url, univ_phys_2_uri):
    # GIVEN a webview_base_url, rex_base_url and a univ_phys_2_uri

    # WHEN we go to a page based on the webview_base_url and uri
    cnx_page_slug = univ_phys_2_uri.split("/")[-1]
    cnx_url = f"{webview_base_url}{univ_phys_2_uri}"
    response = get_url(cnx_url)

    # THEN we are redirected to rex
    assert response.url.startswith(rex_base_url)
    assert response.url.endswith(cnx_page_slug)


@markers.test_case("C568297")
@markers.slow
@markers.rex
@markers.nondestructive
def test_univ_phys_3_uri_redirect_to_rex(webview_base_url, rex_base_url, univ_phys_3_uri):
    # GIVEN a webview_base_url, rex_base_url and a univ_phys_3_uri

    # WHEN we go to a page based on the webview_base_url and uri
    cnx_page_slug = univ_phys_3_uri.split("/")[-1]
    cnx_url = f"{webview_base_url}{univ_phys_3_uri}"
    response = get_url(cnx_url)

    # THEN we are redirected to rex
    assert response.url.startswith(rex_base_url)
    assert response.url.endswith(cnx_page_slug)


@markers.test_case("C568719")
@markers.slow
@markers.rex
@markers.nondestructive
def test_american_government_2e_uri_redirect_to_rex(
    webview_base_url, rex_base_url, american_government_2e_uri
):
    # GIVEN a webview_base_url, rex_base_url and an american_government_2e_uri

    # WHEN we go to a page based on the webview_base_url and uri
    cnx_page_slug = american_government_2e_uri.split("/")[-1]
    cnx_url = f"{webview_base_url}{american_government_2e_uri}"
    response = get_url(cnx_url)

    # THEN we are redirected to rex
    assert response.url.startswith(rex_base_url)
    assert response.url.endswith(cnx_page_slug)


@markers.test_case("C568718")
@markers.slow
@markers.rex
@markers.nondestructive
def test_introductory_business_statistics_uri_redirect_to_rex(
    webview_base_url, rex_base_url, introductory_business_statistics_uri
):
    # GIVEN a webview_base_url, rex_base_url and a introductory_business_statistics_uri

    # WHEN we go to a page based on the webview_base_url and uri
    cnx_page_slug = introductory_business_statistics_uri.split("/")[-1]
    cnx_url = f"{webview_base_url}{introductory_business_statistics_uri}"
    response = get_url(cnx_url)

    # THEN we are redirected to rex
    assert response.url.startswith(rex_base_url)
    assert response.url.endswith(cnx_page_slug)


@markers.test_case("C568717")
@markers.slow
@markers.rex
@markers.nondestructive
def test_introductory_statistics_uri_redirect_to_rex(
    webview_base_url, rex_base_url, introductory_statistics_uri
):
    # GIVEN a webview_base_url, rex_base_url and an introductory_statistics_uri

    # WHEN we go to a page based on the webview_base_url and uri
    cnx_page_slug = introductory_statistics_uri.split("/")[-1]
    cnx_url = f"{webview_base_url}{introductory_statistics_uri}"
    response = get_url(cnx_url)

    # THEN we are redirected to rex
    assert response.url.startswith(rex_base_url)
    assert response.url.endswith(cnx_page_slug)


@markers.test_case("C568721")
@markers.slow
@markers.rex
@markers.nondestructive
def test_principles_of_accounting_1_uri_redirect_to_rex(
    webview_base_url, rex_base_url, principles_of_accounting_1_uri
):
    # GIVEN a webview_base_url, rex_base_url and a principles_of_accounting_vol_1_uri

    # WHEN we go to a page based on the webview_base_url and uri
    cnx_page_slug = principles_of_accounting_1_uri.split("/")[-1]
    cnx_url = f"{webview_base_url}{principles_of_accounting_1_uri}"
    response = get_url(cnx_url)

    # THEN we are redirected to rex
    assert response.url.startswith(rex_base_url)
    assert response.url.endswith(cnx_page_slug)


@markers.test_case("C568722")
@markers.slow
@markers.rex
@markers.nondestructive
def test_principles_of_accounting_2_uri_redirect_to_rex(
    webview_base_url, rex_base_url, principles_of_accounting_2_uri
):
    # GIVEN a webview_base_url, rex_base_url and a principles_of_accounting_vol_2_uri

    # WHEN we go to a page based on the webview_base_url and uri
    cnx_page_slug = principles_of_accounting_2_uri.split("/")[-1]
    cnx_url = f"{webview_base_url}{principles_of_accounting_2_uri}"
    response = get_url(cnx_url)

    # THEN we are redirected to rex
    assert response.url.startswith(rex_base_url)
    assert response.url.endswith(cnx_page_slug)


@markers.test_case("C568720")
@markers.slow
@markers.rex
@markers.nondestructive
def test_us_history_uri_redirect_to_rex(webview_base_url, rex_base_url, us_history_uri):
    # GIVEN a webview_base_url, rex_base_url and a us_history_uri

    # WHEN we go to a page based on the webview_base_url and uri
    cnx_page_slug = us_history_uri.split("/")[-1]
    cnx_url = f"{webview_base_url}{us_history_uri}"
    response = get_url(cnx_url)

    # THEN we are redirected to rex
    assert response.url.startswith(rex_base_url)
    assert response.url.endswith(cnx_page_slug)


@markers.test_case("C597392")
@markers.slow
@markers.rex
@markers.nondestructive
def test_economics_2e_uri_redirect_to_rex(webview_base_url, rex_base_url, economics_2e_uri):
    # GIVEN a webview_base_url, rex_base_url and a economics_2e_uri

    # WHEN we go to a page based on the webview_base_url and uri
    cnx_page_slug = economics_2e_uri.split("/")[-1]
    cnx_url = f"{webview_base_url}{economics_2e_uri}"
    response = get_url(cnx_url)

    # THEN we are redirected to rex
    assert response.url.startswith(rex_base_url)
    assert response.url.endswith(cnx_page_slug)


@markers.test_case("C618400")
@markers.slow
@markers.rex
@markers.nondestructive
def test_economics_uri_redirect_to_rex(webview_base_url, rex_base_url, economics_uri):
    # GIVEN a webview_base_url, rex_base_url and a economics_uri

    # WHEN we go to a page based on the webview_base_url and uri
    cnx_page_slug = economics_uri.split("/")[-1]
    cnx_url = f"{webview_base_url}{economics_uri}"
    response = get_url(cnx_url)

    # THEN we are redirected to rex
    assert response.url.startswith(rex_base_url)
    assert response.url.endswith(cnx_page_slug)


@markers.test_case("C597392")
@markers.slow
@markers.rex
@markers.nondestructive
def test_microeconomics_2e_uri_redirect_to_rex(
    webview_base_url, rex_base_url, microeconomics_2e_uri
):
    # GIVEN a webview_base_url, rex_base_url and a microeconomics_2e_uri

    # WHEN we go to a page based on the webview_base_url and uri
    cnx_page_slug = microeconomics_2e_uri.split("/")[-1]
    cnx_url = f"{webview_base_url}{microeconomics_2e_uri}"
    response = get_url(cnx_url)

    # THEN we are redirected to rex
    assert response.url.startswith(rex_base_url)
    assert response.url.endswith(cnx_page_slug)


@markers.test_case("C618400")
@markers.slow
@markers.rex
@markers.nondestructive
def test_microeconomics_uri_redirect_to_rex(webview_base_url, rex_base_url, microeconomics_uri):
    # GIVEN a webview_base_url, rex_base_url and a microeconomics_2e_uri

    # WHEN we go to a page based on the webview_base_url and uri
    cnx_page_slug = microeconomics_uri.split("/")[-1]
    cnx_url = f"{webview_base_url}{microeconomics_uri}"
    response = get_url(cnx_url)

    # THEN we are redirected to rex
    assert response.url.startswith(rex_base_url)
    assert response.url.endswith(cnx_page_slug)


@markers.test_case("C597392")
@markers.slow
@markers.rex
@markers.nondestructive
def test_macroeconomics_2e_uri_redirect_to_rex(
    webview_base_url, rex_base_url, macroeconomics_2e_uri
):
    # GIVEN a webview_base_url, rex_base_url and a macroeconomics_2e_uri

    # WHEN we go to a page based on the webview_base_url and uri
    cnx_page_slug = macroeconomics_2e_uri.split("/")[-1]
    cnx_url = f"{webview_base_url}{macroeconomics_2e_uri}"
    response = get_url(cnx_url)

    # THEN we are redirected to rex
    assert response.url.startswith(rex_base_url)
    assert response.url.endswith(cnx_page_slug)


@markers.test_case("C618400")
@markers.slow
@markers.rex
@markers.nondestructive
def test_macroeconomics_uri_redirect_to_rex(webview_base_url, rex_base_url, macroeconomics_uri):
    # GIVEN a webview_base_url, rex_base_url and a macroeconomics_uri

    # WHEN we go to a page based on the webview_base_url and uri
    cnx_page_slug = macroeconomics_uri.split("/")[-1]
    cnx_url = f"{webview_base_url}{macroeconomics_uri}"
    response = get_url(cnx_url)

    # THEN we are redirected to rex
    assert response.url.startswith(rex_base_url)
    assert response.url.endswith(cnx_page_slug)


@markers.test_case("C597392")
@markers.slow
@markers.rex
@markers.nondestructive
def test_entrepreneurship_uri_redirect_to_rex(webview_base_url, rex_base_url, entrepreneurship_uri):
    # GIVEN a webview_base_url, rex_base_url and a entrepreneurship_uri

    # WHEN we go to a page based on the webview_base_url and uri
    cnx_page_slug = entrepreneurship_uri.split("/")[-1]
    cnx_url = f"{webview_base_url}{entrepreneurship_uri}"
    response = get_url(cnx_url)

    # THEN we are redirected to rex
    assert response.url.startswith(rex_base_url)
    assert response.url.endswith(cnx_page_slug)


@markers.test_case("C597392")
@markers.slow
@markers.rex
@markers.nondestructive
def test_sociology_2e_uri_redirect_to_rex(webview_base_url, rex_base_url, sociology_2e_uri):
    # GIVEN a webview_base_url, rex_base_url and a sociology_2e_uri

    # WHEN we go to a page based on the webview_base_url and uri
    cnx_page_slug = sociology_2e_uri.split("/")[-1]
    cnx_url = f"{webview_base_url}{sociology_2e_uri}"
    response = get_url(cnx_url)

    # THEN we are redirected to rex
    assert response.url.startswith(rex_base_url)
    assert response.url.endswith(cnx_page_slug)


@markers.test_case("C597392")
@markers.slow
@markers.rex
@markers.nondestructive
def test_intro_business_uri_redirect_to_rex(webview_base_url, rex_base_url, intro_business_uri):
    # GIVEN a webview_base_url, rex_base_url and a intro_business_uri

    # WHEN we go to a page based on the webview_base_url and uri
    cnx_page_slug = intro_business_uri.split("/")[-1]
    cnx_url = f"{webview_base_url}{intro_business_uri}"
    response = get_url(cnx_url)

    # THEN we are redirected to rex
    assert response.url.startswith(rex_base_url)
    assert response.url.endswith(cnx_page_slug)


@markers.test_case("C597392")
@markers.slow
@markers.rex
@markers.nondestructive
def test_business_ethics_uri_redirect_to_rex(webview_base_url, rex_base_url, business_ethics_uri):
    # GIVEN a webview_base_url, rex_base_url and a business_ethics_uri

    # WHEN we go to a page based on the webview_base_url and uri
    cnx_page_slug = business_ethics_uri.split("/")[-1]
    cnx_url = f"{webview_base_url}{business_ethics_uri}"
    response = get_url(cnx_url)

    # THEN we are redirected to rex
    assert response.url.startswith(rex_base_url)
    assert response.url.endswith(cnx_page_slug)


@markers.test_case("C597392")
@markers.slow
@markers.rex
@markers.nondestructive
def test_principles_of_mgnt_uri_redirect_to_rex(
    webview_base_url, rex_base_url, principles_of_mgnt_uri
):
    # GIVEN a webview_base_url, rex_base_url and a principles_of_mgnt_uri

    # WHEN we go to a page based on the webview_base_url and uri
    cnx_page_slug = principles_of_mgnt_uri.split("/")[-1]
    cnx_url = f"{webview_base_url}{principles_of_mgnt_uri}"
    response = get_url(cnx_url)

    # THEN we are redirected to rex
    assert response.url.startswith(rex_base_url)
    assert response.url.endswith(cnx_page_slug)


@markers.test_case("C597392")
@markers.slow
@markers.rex
@markers.nondestructive
def test_organizational_behavior_uri_redirect_to_rex(
    webview_base_url, rex_base_url, organizational_behavior_uri
):
    # GIVEN a webview_base_url, rex_base_url and a organizational_behavior_uri

    # WHEN we go to a page based on the webview_base_url and uri
    cnx_page_slug = organizational_behavior_uri.split("/")[-1]
    cnx_url = f"{webview_base_url}{organizational_behavior_uri}"
    response = get_url(cnx_url)

    # THEN we are redirected to rex
    assert response.url.startswith(rex_base_url)
    assert response.url.endswith(cnx_page_slug)


@markers.test_case("C600020")
@markers.slow
@markers.rex
@markers.nondestructive
def test_business_law_i_ess_uri_redirect_to_rex(
    webview_base_url, rex_base_url, business_law_i_ess_uri
):
    # GIVEN a webview_base_url, rex_base_url and a ..._uri

    # WHEN we go to a page based on the webview_base_url and uri
    cnx_page_slug = business_law_i_ess_uri.split("/")[-1]
    cnx_url = f"{webview_base_url}{business_law_i_ess_uri}"
    response = get_url(cnx_url)

    # THEN we are redirected to rex
    assert response.url.startswith(rex_base_url)
    assert response.url.endswith(cnx_page_slug)


@markers.test_case("C600020")
@markers.slow
@markers.rex
@markers.nondestructive
def test_college_algebra_uri_redirect_to_rex(webview_base_url, rex_base_url, college_algebra_uri):
    # GIVEN a webview_base_url, rex_base_url and a ..._uri

    # WHEN we go to a page based on the webview_base_url and uri
    cnx_page_slug = college_algebra_uri.split("/")[-1]
    cnx_url = f"{webview_base_url}{college_algebra_uri}"
    response = get_url(cnx_url)

    # THEN we are redirected to rex
    assert response.url.startswith(rex_base_url)
    assert response.url.endswith(cnx_page_slug)


@markers.test_case("C600020")
@markers.slow
@markers.rex
@markers.nondestructive
def test_principles_microecon_ap_courses_2e_uri_redirect_to_rex(
    webview_base_url, rex_base_url, principles_microecon_ap_courses_2e_uri
):
    # GIVEN a webview_base_url, rex_base_url and a ..._uri

    # WHEN we go to a page based on the webview_base_url and uri
    cnx_page_slug = principles_microecon_ap_courses_2e_uri.split("/")[-1]
    cnx_url = f"{webview_base_url}{principles_microecon_ap_courses_2e_uri}"
    response = get_url(cnx_url)

    # THEN we are redirected to rex
    assert response.url.startswith(rex_base_url)
    assert response.url.endswith(cnx_page_slug)


@markers.test_case("C618400")
@markers.slow
@markers.rex
@markers.nondestructive
def test_principles_microecon_ap_courses_uri_redirect_to_rex(
    webview_base_url, rex_base_url, principles_microecon_ap_courses_uri
):
    # GIVEN a webview_base_url, rex_base_url and a ..._uri

    # WHEN we go to a page based on the webview_base_url and uri
    cnx_page_slug = principles_microecon_ap_courses_uri.split("/")[-1]
    cnx_url = f"{webview_base_url}{principles_microecon_ap_courses_uri}"
    response = get_url(cnx_url)

    # THEN we are redirected to rex
    assert response.url.startswith(rex_base_url)
    assert response.url.endswith(cnx_page_slug)


@markers.test_case("C600020")
@markers.slow
@markers.rex
@markers.nondestructive
def test_principles_macroecon_ap_courses_2e_uri_redirect_to_rex(
    webview_base_url, rex_base_url, principles_macroecon_ap_courses_2e_uri
):
    # GIVEN a webview_base_url, rex_base_url and a ..._uri

    # WHEN we go to a page based on the webview_base_url and uri
    cnx_page_slug = principles_macroecon_ap_courses_2e_uri.split("/")[-1]
    cnx_url = f"{webview_base_url}{principles_macroecon_ap_courses_2e_uri}"
    response = get_url(cnx_url)

    # THEN we are redirected to rex
    assert response.url.startswith(rex_base_url)
    assert response.url.endswith(cnx_page_slug)


@markers.test_case("C618400")
@markers.slow
@markers.rex
@markers.nondestructive
def test_principles_macroecon_ap_courses_uri_redirect_to_rex(
    webview_base_url, rex_base_url, principles_macroecon_ap_courses_uri
):
    # GIVEN a webview_base_url, rex_base_url and a ..._uri

    # WHEN we go to a page based on the webview_base_url and uri
    cnx_page_slug = principles_macroecon_ap_courses_uri.split("/")[-1]
    cnx_url = f"{webview_base_url}{principles_macroecon_ap_courses_uri}"
    response = get_url(cnx_url)

    # THEN we are redirected to rex
    assert response.url.startswith(rex_base_url)
    assert response.url.endswith(cnx_page_slug)


@markers.test_case("C600020")
@markers.slow
@markers.rex
@markers.nondestructive
def test_prealgebra_2e_uri_redirect_to_rex(webview_base_url, rex_base_url, prealgebra_2e_uri):
    # GIVEN a webview_base_url, rex_base_url and a ..._uri

    # WHEN we go to a page based on the webview_base_url and uri
    cnx_page_slug = prealgebra_2e_uri.split("/")[-1]
    cnx_url = f"{webview_base_url}{prealgebra_2e_uri}"
    response = get_url(cnx_url)

    # THEN we are redirected to rex
    assert response.url.startswith(rex_base_url)
    assert response.url.endswith(cnx_page_slug)


@markers.test_case("C616758")
@markers.slow
@markers.rex
@markers.nondestructive
def test_prealgebra_uri_redirect_to_rex(webview_base_url, rex_base_url, prealgebra_uri):
    # GIVEN a webview_base_url, rex_base_url and a ..._uri

    # WHEN we go to a page based on the webview_base_url and uri
    cnx_page_slug = prealgebra_uri.split("/")[-1]
    cnx_url = f"{webview_base_url}{prealgebra_uri}"
    response = get_url(cnx_url)

    # THEN we are redirected to rex
    assert response.url.startswith(rex_base_url)
    assert response.url.endswith(cnx_page_slug)


@markers.test_case("C602857")
@markers.slow
@markers.rex
@markers.nondestructive
def test_elem_algebra_2e_uri_redirect_to_rex(webview_base_url, rex_base_url, elem_algebra_2e_uri):
    # GIVEN a webview_base_url, rex_base_url and a ..._uri

    # WHEN we go to a page based on the webview_base_url and uri
    cnx_page_slug = elem_algebra_2e_uri.split("/")[-1]
    cnx_url = f"{webview_base_url}{elem_algebra_2e_uri}"
    response = get_url(cnx_url)

    # THEN we are redirected to rex
    assert response.url.startswith(rex_base_url)
    assert response.url.endswith(cnx_page_slug)


@markers.test_case("C616758")
@markers.slow
@markers.rex
@markers.nondestructive
def test_elem_algebra_uri_redirect_to_rex(webview_base_url, rex_base_url, elem_algebra_uri):
    # GIVEN a webview_base_url, rex_base_url and a ..._uri

    # WHEN we go to a page based on the webview_base_url and uri
    cnx_page_slug = elem_algebra_uri.split("/")[-1]
    cnx_url = f"{webview_base_url}{elem_algebra_uri}"
    response = get_url(cnx_url)

    # THEN we are redirected to rex
    assert response.url.startswith(rex_base_url)
    assert response.url.endswith(cnx_page_slug)


@markers.test_case("C602857")
@markers.slow
@markers.rex
@markers.nondestructive
def test_stats_hs_uri_redirect_to_rex(webview_base_url, rex_base_url, stats_hs_uri):
    # GIVEN a webview_base_url, rex_base_url and a ..._uri

    # WHEN we go to a page based on the webview_base_url and uri
    cnx_page_slug = stats_hs_uri.split("/")[-1]
    cnx_url = f"{webview_base_url}{stats_hs_uri}"
    response = get_url(cnx_url)

    # THEN we are redirected to rex
    assert response.url.startswith(rex_base_url)
    assert response.url.endswith(cnx_page_slug)


@markers.test_case("C602857")
@markers.slow
@markers.rex
@markers.nondestructive
def test_co_success_uri_redirect_to_rex(webview_base_url, rex_base_url, cosu_uri):
    # GIVEN a webview_base_url, rex_base_url and a ..._uri

    # WHEN we go to a page based on the webview_base_url and uri
    cnx_page_slug = cosu_uri.split("/")[-1]
    cnx_url = f"{webview_base_url}{cosu_uri}"
    response = get_url(cnx_url)

    # THEN we are redirected to rex
    assert response.url.startswith(rex_base_url)
    assert response.url.endswith(cnx_page_slug)


@markers.test_case("C602857")
@markers.slow
@markers.rex
@markers.nondestructive
def test_psych_2e_uri_redirect_to_rex(webview_base_url, rex_base_url, psych_2e_uri):
    # GIVEN a webview_base_url, rex_base_url and a ..._uri

    # WHEN we go to a page based on the webview_base_url and uri
    cnx_page_slug = psych_2e_uri.split("/")[-1]
    cnx_url = f"{webview_base_url}{psych_2e_uri}"
    response = get_url(cnx_url)

    # THEN we are redirected to rex
    assert response.url.startswith(rex_base_url)
    assert response.url.endswith(cnx_page_slug)


@markers.test_case("C605719")
@markers.slow
@markers.rex
@markers.nondestructive
def test_interm_algebra_2e_uri_redirect_to_rex(
    webview_base_url, rex_base_url, interm_algebra_2e_uri
):
    # GIVEN a webview_base_url, rex_base_url and a ..._uri

    # WHEN we go to a page based on the webview_base_url and uri
    cnx_page_slug = interm_algebra_2e_uri.split("/")[-1]
    cnx_url = f"{webview_base_url}{interm_algebra_2e_uri}"
    response = get_url(cnx_url)

    # THEN we are redirected to rex
    assert response.url.startswith(rex_base_url)
    assert response.url.endswith(cnx_page_slug)


@markers.test_case("C616758")
@markers.slow
@markers.rex
@markers.nondestructive
def test_interm_algebra_uri_redirect_to_rex(webview_base_url, rex_base_url, interm_algebra_uri):
    # GIVEN a webview_base_url, rex_base_url and a ..._uri

    # WHEN we go to a page based on the webview_base_url and uri
    cnx_page_slug = interm_algebra_uri.split("/")[-1]
    cnx_url = f"{webview_base_url}{interm_algebra_uri}"
    response = get_url(cnx_url)

    # THEN we are redirected to rex
    assert response.url.startswith(rex_base_url)
    assert response.url.endswith(cnx_page_slug)


@markers.test_case("C608129")
@markers.slow
@markers.rex
@markers.nondestructive
def test_psychology_uri_redirect_to_rex(webview_base_url, rex_base_url, psychology_uri):
    # GIVEN a webview_base_url, rex_base_url and a ..._uri

    # WHEN we go to a page based on the webview_base_url and uri
    cnx_page_slug = psychology_uri.split("/")[-1]
    cnx_url = f"{webview_base_url}{psychology_uri}"
    response = get_url(cnx_url)

    # THEN we are redirected to rex
    assert response.url.startswith(rex_base_url)
    assert response.url.endswith(cnx_page_slug)


@markers.test_case("C608129")
@markers.slow
@markers.rex
@markers.nondestructive
def test_physics_hs_uri_redirect_to_rex(webview_base_url, rex_base_url, physics_hs_uri):
    # GIVEN a webview_base_url, rex_base_url and a ..._uri

    # WHEN we go to a page based on the webview_base_url and uri
    cnx_page_slug = physics_hs_uri.split("/")[-1]
    cnx_url = f"{webview_base_url}{physics_hs_uri}"
    response = get_url(cnx_url)

    # THEN we are redirected to rex
    assert response.url.startswith(rex_base_url)
    assert response.url.endswith(cnx_page_slug)


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


@markers.test_case("C616758")
@markers.slow
@markers.rex
@markers.nondestructive
def test_intro_to_soc_uri_redirect_to_rex(webview_base_url, rex_base_url, intro_to_soc_uri):
    # GIVEN a webview_base_url, rex_base_url and a sociology_2e_uri

    # WHEN we go to a page based on the webview_base_url and uri
    cnx_page_slug = intro_to_soc_uri.split("/")[-1]
    cnx_url = f"{webview_base_url}{intro_to_soc_uri}"
    response = get_url(cnx_url)

    # THEN we are redirected to rex
    assert response.url.startswith(rex_base_url)
    assert response.url.endswith(cnx_page_slug)
