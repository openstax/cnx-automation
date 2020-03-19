# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os
import pytest
import requests

import tldextract
from rex_redirects import get_rex_release_json_url

from tests.utils import gen_from_file, skip_if_destructive_and_sensitive

DATA_DIR = os.path.join(os.path.realpath(os.path.dirname(__file__)), "data", "webview")

__all__ = ["american_gov_uuid", "webview_base_url"]


@pytest.fixture(params=gen_from_file(os.path.join(DATA_DIR, "american_gov_uuids.txt")))
def american_gov_uuid(request):
    """Yields American Government UUIDs from the american_gov_uuids.txt file

    Example: c6ee95dd-d10b-430c-8a83-20d5a28334a9
    """
    yield request.param


@pytest.fixture(
    params=gen_from_file(os.path.join(DATA_DIR, "7fccc9cf-9b71-44f6-800b-f9457fd64335.txt"))
)
def chemistry_2e_uri(request):
    """Yields a URI from the Chemistry 2e book located on a cnx.org instance

    Example: /contents/f8zJz5tx@0.0:2po7o99e/1-essential-ideas
    """
    yield request.param


@pytest.fixture(
    params=gen_from_file(os.path.join(DATA_DIR, "8d50a0af-948b-4204-a71d-4826cba765b8.txt"))
)
def biology_2e_uri(request):
    """Yields a URI from the Biology 2e book located on a cnx.org instance

    Example: /contents/f8zJz5tx@0.0:2po7o99e/1-essential-ideas
    """
    yield request.param


@pytest.fixture(
    params=gen_from_file(os.path.join(DATA_DIR, "e42bd376-624b-4c0f-972f-e0c57998e765.txt"))
)
def microbiology_uri(request):
    """Yields a URI from the Microbiology book located on a cnx.org instance

    Example: /contents/f8zJz5tx@0.0:2po7o99e/1-essential-ideas
    """
    yield request.param


@pytest.fixture(
    params=gen_from_file(os.path.join(DATA_DIR, "b3c1e1d2-839c-42b0-a314-e119a8aafbdd.txt"))
)
def conceptsofbiology_uri(request):
    """Yields a URI from the Concepts of Biology book located on a cnx.org instance

    Example: /contents/f8zJz5tx@0.0:2po7o99e/1-essential-ideas
    """
    yield request.param


@pytest.fixture(
    params=gen_from_file(os.path.join(DATA_DIR, "2e737be8-ea65-48c3-aa0a-9f35b4c6a966.txt"))
)
def astronomy_uri(request):
    """Yields a URI from the Astronomy book located on a cnx.org instance

    Example: /contents/f8zJz5tx@0.0:2po7o99e/1-essential-ideas
    """
    yield request.param


@pytest.fixture(
    params=gen_from_file(os.path.join(DATA_DIR, "6c322e32-9fb0-4c4d-a1d7-20c95c5c7af2.txt"))
)
def biology_ap_uri(request):
    """Yields a URI from the Biology AP book located on a cnx.org instance

    Example: /contents/f8zJz5tx@0.0:2po7o99e/1-essential-ideas
    """
    yield request.param


@pytest.fixture(
    params=gen_from_file(os.path.join(DATA_DIR, "8d04a686-d5e8-4798-a27d-c608e4d0e187.txt"))
)
def college_physics_ap_courses_uri(request):
    """Yields a URI from the College Physics AP Courses book located on a cnx.org instance

    Example: /contents/f8zJz5tx@0.0:2po7o99e/1-essential-ideas
    """
    yield request.param


@pytest.fixture(
    params=gen_from_file(os.path.join(DATA_DIR, "14fb4ad7-39a1-4eee-ab6e-3ef2482e3e22.txt"))
)
def anatomy_and_physiology_uri(request):
    """Yields a URI from the Anatomy And Physiology book located on a cnx.org instance

    Example: /contents/f8zJz5tx@0.0:2po7o99e/1-essential-ideas
    """
    yield request.param


@pytest.fixture(
    params=gen_from_file(os.path.join(DATA_DIR, "031da8d3-b525-429c-80cf-6c8ed997733a.txt"))
)
def college_physics_uri(request):
    """Yields a URI from the College Physics book located on a cnx.org instance

    Example: /contents/f8zJz5tx@0.0:2po7o99e/1-essential-ideas
    """
    yield request.param


@pytest.fixture(
    params=gen_from_file(os.path.join(DATA_DIR, "d9b85ee6-c57f-4861-8208-5ddf261e9c5f.txt"))
)
def chemistry_atoms_first_2e_uri(request):
    """Yields a URI from the Chemistry: Atoms First 2e book located on a cnx.org instance

    Example: /contents/f8zJz5tx@0.0:2po7o99e/1-essential-ideas
    """
    yield request.param


@pytest.fixture(
    params=gen_from_file(os.path.join(DATA_DIR, "d50f6e32-0fda-46ef-a362-9bd36ca7c97d.txt"))
)
def univ_phys_1_uri(request):
    """Yields a URI from the University Physics vol 1 book located on a cnx.org instance

    Example: /contents/f8zJz5tx@0.0:2po7o99e/1-essential-ideas
    """
    yield request.param


@pytest.fixture(
    params=gen_from_file(os.path.join(DATA_DIR, "7a0f9770-1c44-4acd-9920-1cd9a99f2a1e.txt"))
)
def univ_phys_2_uri(request):
    """Yields a URI from the University Physics vol 2 book located on a cnx.org instance

    Example: /contents/f8zJz5tx@0.0:2po7o99e/1-essential-ideas
    """
    yield request.param


@pytest.fixture(
    params=gen_from_file(os.path.join(DATA_DIR, "af275420-6050-4707-995c-57b9cc13c358.txt"))
)
def univ_phys_3_uri(request):
    """Yields a URI from the University Physics vol 3 book located on a cnx.org instance

    Example: /contents/f8zJz5tx@0.0:2po7o99e/1-essential-ideas
    """
    yield request.param


@pytest.fixture(
    params=gen_from_file(os.path.join(DATA_DIR, "8b89d172-2927-466f-8661-01abc7ccdba4.txt"))
)
def calculus_vol_1_uri(request):
    """Yields a URI from the Calculus vol 1 book located on a cnx.org instance

    Example: /contents/f8zJz5tx@0.0:2po7o99e/1-essential-ideas
    """
    yield request.param


@pytest.fixture(
    params=gen_from_file(os.path.join(DATA_DIR, "1d39a348-071f-4537-85b6-c98912458c3c.txt"))
)
def calculus_vol_2_uri(request):
    """Yields a URI from the Calculus vol 2 book located on a cnx.org instance

    Example: /contents/f8zJz5tx@0.0:2po7o99e/1-essential-ideas
    """
    yield request.param


@pytest.fixture(
    params=gen_from_file(os.path.join(DATA_DIR, "a31cd793-2162-4e9e-acb5-6e6bbd76a5fa.txt"))
)
def calculus_vol_3_uri(request):
    """Yields a URI from the Calculus vol 3 book located on a cnx.org instance

    Example: /contents/f8zJz5tx@0.0:2po7o99e/1-essential-ideas
    """
    yield request.param


@pytest.fixture(
    params=gen_from_file(os.path.join(DATA_DIR, "9ab4ba6d-1e48-486d-a2de-38ae1617ca84.txt"))
)
def principles_of_accounting_1_uri(request):
    """Yields a URI from the principles of accounting 1 book located on a cnx.org instance

    Example: /contents/f8zJz5tx@0.0:2po7o99e/1-essential-ideas
    """
    yield request.param


@pytest.fixture(
    params=gen_from_file(os.path.join(DATA_DIR, "920d1c8a-606c-4888-bfd4-d1ee27ce1795.txt"))
)
def principles_of_accounting_2_uri(request):
    """Yields a URI from the principles of accounting 2 book located on a cnx.org instance

    Example: /contents/f8zJz5tx@0.0:2po7o99e/1-essential-ideas
    """
    yield request.param


@pytest.fixture(
    params=gen_from_file(os.path.join(DATA_DIR, "9d8df601-4f12-4ac1-8224-b450bf739e5f.txt"))
)
def american_government_2e_uri(request):
    """Yields a URI from the american government 2e book located on a cnx.org instance

    Example: /contents/f8zJz5tx@0.0:2po7o99e/1-essential-ideas
    """
    yield request.param


@pytest.fixture(
    params=gen_from_file(os.path.join(DATA_DIR, "30189442-6998-4686-ac05-ed152b91b9de.txt"))
)
def introductory_statistics_uri(request):
    """Yields a URI from the introductory statistics book located on a cnx.org instance

    Example: /contents/f8zJz5tx@0.0:2po7o99e/1-essential-ideas
    """
    yield request.param


@pytest.fixture(
    params=gen_from_file(os.path.join(DATA_DIR, "a7ba2fb8-8925-4987-b182-5f4429d48daa.txt"))
)
def us_history_uri(request):
    """Yields a URI from the us history book located on a cnx.org instance

    Example: /contents/f8zJz5tx@0.0:2po7o99e/1-essential-ideas
    """
    yield request.param


@pytest.fixture(
    params=gen_from_file(os.path.join(DATA_DIR, "b56bb9e9-5eb8-48ef-9939-88b1b12ce22f.txt"))
)
def introductory_business_statistics_uri(request):
    """Yields a URI from the introductory business statistics book located on a cnx.org instance

    Example: /contents/f8zJz5tx@0.0:2po7o99e/1-essential-ideas
    """
    yield request.param


@pytest.fixture(
    params=gen_from_file(os.path.join(DATA_DIR, "bc498e1f-efe9-43a0-8dea-d3569ad09a82.txt"))
)
def economics_2e_uri(request):
    """Yields a URI from collection

    Example: /contents/f8zJz5tx@0.0:2po7o99e/1-essential-ideas
    """
    yield request.param


@pytest.fixture(
    params=gen_from_file(os.path.join(DATA_DIR, "5c09762c-b540-47d3-9541-dda1f44f16e5.txt"))
)
def microeconomics_2e_uri(request):
    """Yields a URI from collection

    Example: /contents/f8zJz5tx@0.0:2po7o99e/1-essential-ideas
    """
    yield request.param


@pytest.fixture(
    params=gen_from_file(os.path.join(DATA_DIR, "27f59064-990e-48f1-b604-5188b9086c29.txt"))
)
def macroeconomics_2e_uri(request):
    """Yields a URI from collection

    Example: /contents/f8zJz5tx@0.0:2po7o99e/1-essential-ideas
    """
    yield request.param


@pytest.fixture(
    params=gen_from_file(os.path.join(DATA_DIR, "d380510e-6145-4625-b19a-4fa68204b6b1.txt"))
)
def entrepreneurship_uri(request):
    """Yields a URI from collection

    Example: /contents/f8zJz5tx@0.0:2po7o99e/1-essential-ideas
    """
    yield request.param


@pytest.fixture(
    params=gen_from_file(os.path.join(DATA_DIR, "02040312-72c8-441e-a685-20e9333f3e1d.txt"))
)
def sociology_2e_uri(request):
    """Yields a URI from collection

    Example: /contents/f8zJz5tx@0.0:2po7o99e/1-essential-ideas
    """
    yield request.param


@pytest.fixture(
    params=gen_from_file(os.path.join(DATA_DIR, "4e09771f-a8aa-40ce-9063-aa58cc24e77f.txt"))
)
def intro_business_uri(request):
    """Yields a URI from collection

    Example: /contents/f8zJz5tx@0.0:2po7o99e/1-essential-ideas
    """
    yield request.param


@pytest.fixture(
    params=gen_from_file(os.path.join(DATA_DIR, "914ac66e-e1ec-486d-8a9c-97b0f7a99774.txt"))
)
def business_ethics_uri(request):
    """Yields a URI from collection

    Example: /contents/f8zJz5tx@0.0:2po7o99e/1-essential-ideas
    """
    yield request.param


@pytest.fixture(
    params=gen_from_file(os.path.join(DATA_DIR, "c3acb2ab-7d5c-45ad-b3cd-e59673fedd4e.txt"))
)
def principles_of_mgnt_uri(request):
    """Yields a URI from collection

    Example: /contents/f8zJz5tx@0.0:2po7o99e/1-essential-ideas
    """
    yield request.param


@pytest.fixture(
    params=gen_from_file(os.path.join(DATA_DIR, "2d941ab9-ac5b-4eb8-b21c-965d36a4f296.txt"))
)
def organizational_behavior_uri(request):
    """Yields a URI from collection

    Example: /contents/f8zJz5tx@0.0:2po7o99e/1-essential-ideas
    """
    yield request.param


@pytest.fixture(
    params=gen_from_file(os.path.join(DATA_DIR, "464a3fba-68c1-426a-99f9-597e739dc911.txt"))
)
def business_law_i_ess_uri(request):
    """Yields a URI from collection

    Example: /contents/f8zJz5tx@0.0:2po7o99e/1-essential-ideas
    """
    yield request.param


@pytest.fixture(
    params=gen_from_file(os.path.join(DATA_DIR, "9b08c294-057f-4201-9f48-5d6ad992740d.txt"))
)
def college_algebra_uri(request):
    """Yields a URI from collection

    Example: /contents/f8zJz5tx@0.0:2po7o99e/1-essential-ideas
    """
    yield request.param


@pytest.fixture(
    params=gen_from_file(os.path.join(DATA_DIR, "13ac107a-f15f-49d2-97e8-60ab2e3b519c.txt"))
)
def algebra_and_trig_uri(request):
    """Yields a URI from collection

    Example: /contents/f8zJz5tx@0.0:2po7o99e/1-essential-ideas
    """
    yield request.param


@pytest.fixture(
    params=gen_from_file(os.path.join(DATA_DIR, "fd53eae1-fa23-47c7-bb1b-972349835c3c.txt"))
)
def precalculus_uri(request):
    """Yields a URI from collection

    Example: /contents/f8zJz5tx@0.0:2po7o99e/1-essential-ideas
    """
    yield request.param


@pytest.fixture(
    params=gen_from_file(os.path.join(DATA_DIR, "636cbfd9-4e37-4575-83ab-9dec9029ca4e.txt"))
)
def principles_microecon_ap_courses_2e_uri(request):
    """Yields a URI from collection

    Example: /contents/f8zJz5tx@0.0:2po7o99e/1-essential-ideas
    """
    yield request.param


@pytest.fixture(
    params=gen_from_file(os.path.join(DATA_DIR, "9117cf8c-a8a3-4875-8361-9cb0f1fc9362.txt"))
)
def principles_macroecon_ap_courses_2e_uri(request):
    """Yields a URI from collection

    Example: /contents/f8zJz5tx@0.0:2po7o99e/1-essential-ideas
    """
    yield request.param


@pytest.fixture(
    params=gen_from_file(os.path.join(DATA_DIR, "f0fa90be-fca8-43c9-9aad-715c0a2cee2b.txt"))
)
def prealgebra_2e_uri(request):
    """Yields a URI from collection

    Example: /contents/f8zJz5tx@0.0:2po7o99e/1-essential-ideas
    """
    yield request.param


@pytest.fixture
def robots_txt_production():
    """Returns the text file location which includes all the robots.txt lines for production env
    """
    data_file = DATA_DIR + "/robots.prod.txt"

    with open(data_file, "r") as infile:

        data = infile.read()

    return data.strip()


@pytest.fixture
def webview_base_url(request):
    """Return a base URL for CNX webview"""
    config = request.config
    base_url = config.getoption("webview_base_url") or config.getini("webview_base_url")
    if base_url is not None:
        skip_if_destructive_and_sensitive(request, base_url)
        return base_url


@pytest.fixture
def rex_base_url(request):
    """Return a base URL for REX used for integration testing"""
    config = request.config
    base_url = config.getoption("rex_base_url") or config.getini("rex_base_url")
    if base_url is not None:
        skip_if_destructive_and_sensitive(request, base_url)
        return base_url


@pytest.fixture
def rex_released_books(rex_base_url):
    rex_host = rex_base_url.split("://")[-1]

    release_json_url = get_rex_release_json_url(rex_host)
    response = requests.get(release_json_url)
    response.raise_for_status()

    return response.json()["books"]


@pytest.fixture(params=gen_from_file(os.path.join(DATA_DIR, "openstax_books_uuids.txt")))
def openstax_all_books_uuids(request):
    """Yields UUIDs for all openstax books
    """
    yield request.param


@pytest.fixture
def vendor_base_url(request):
    """Return a base URL for Vendor cnx page"""
    config = request.config
    base_url = config.getoption("vendor_base_url") or config.getini("vendor_base_url")
    if base_url is not None:
        skip_if_destructive_and_sensitive(request, base_url)
        return base_url


@pytest.fixture
def webview_instance(webview_base_url):
    url = tldextract.extract(webview_base_url)
    if url.subdomain:
        return url.subdomain
    else:
        return "prod"


@pytest.fixture
def s3_base_url(request):
    """Return a base URL for AWS S3 bucket"""
    config = request.config
    base_url = config.getoption("s3_base_url") or config.getini("s3_base_url")
    if base_url is not None:
        skip_if_destructive_and_sensitive(request, base_url)
        return base_url


@pytest.fixture(params=gen_from_file(os.path.join(DATA_DIR, "s3_books_uuids.txt")))
def s3_all_books_uuids(request):
    """Yields UUIDs for all books in aws s3 bucket
    """
    yield request.param


@pytest.fixture
def s3_books_url(s3_base_url, s3_all_books_uuids):
    """Return a base URL for AWS S3 bucket"""
    s3_url = f"{s3_base_url}/baked/{s3_all_books_uuids}.json"
    return s3_url


@pytest.fixture
def s3_books_titles():
    """Returns the book titles for books in aws s3 bucket
    """
    data_file = DATA_DIR + "/s3_books_titles.txt"

    with open(data_file, "r") as infile:
        data = infile.read()
    return data.strip()
