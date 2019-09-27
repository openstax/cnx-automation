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


@pytest.fixture
def webview_instance(webview_base_url):
    url = tldextract.extract(webview_base_url)
    if url.subdomain:
        return url.subdomain
    else:
        return "prod"
