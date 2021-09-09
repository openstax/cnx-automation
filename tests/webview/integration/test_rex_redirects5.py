import backoff
import requests

from tests import markers

import csv
import pytest


@backoff.on_exception(backoff.expo, requests.exceptions.ConnectionError)
def get_url(url):
    return requests.get(url)


@markers.slow
@markers.nondestructive
def test_calculus2_uri_redirect_to_rex(webview_base_url, rex_base_url, calculus_vol_2_uri):
    # GIVEN a webview_base_url, rex_base_url and a calculus_vol_2_uri

    # WHEN we go to a page based on the webview_base_url and uri
    cnx_page_slug = calculus_vol_2_uri.split("/")[-1]
    cnx_url = f"{webview_base_url}{calculus_vol_2_uri}"
    response = get_url(cnx_url)

    status_codes = []
    error_urls = []

    # THEN we are redirected to rex
    if response.status_code != 200:

        status_codes.append(str(response.status_code))
        error_urls.append(cnx_url)

        dict_urls = {"PAGE URL": error_urls[i] for i in range(len(status_codes))}
        dict_errors = {"ERROR": status_codes[i] for i in range(len(status_codes))}
        dict_urls_errors = {**dict_urls, **dict_errors}

        with open("url_error_list.csv", "a") as urlerr:
            writer = csv.DictWriter(urlerr, dict_urls_errors.keys())

            if urlerr.tell() == 0:
                writer.writeheader()

            writer.writerow(dict_urls_errors)

        pytest.fail(f"{response.status_code} in {cnx_page_slug}")

    else:
        assert 200 == response.status_code
        assert response.url.startswith(rex_base_url)
