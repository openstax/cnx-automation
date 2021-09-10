import backoff
import requests

from tests import markers

import csv
import pytest


@backoff.on_exception(backoff.expo, requests.exceptions.ConnectionError)
def get_url(url):
    return requests.get(url)


def log_failures_to_csv(status_code, cnx_url):
    dict_urls_errors = {"ERROR": status_code, "PAGE URL": cnx_url}

    with open("url_failures_report.csv", "a") as urlerr:
        writer = csv.DictWriter(urlerr, dict_urls_errors.keys())
        if urlerr.tell() == 0:
            writer.writeheader()
        writer.writerow(dict_urls_errors)


@markers.slow
@markers.nondestructive
def test_calculus2_uri_redirect_to_rex(webview_base_url, rex_base_url, calculus_vol_2_uri):
    # GIVEN a webview_base_url, rex_base_url and a calculus_vol_2_uri

    # WHEN we go to a page based on the webview_base_url and uri
    cnx_page_slug = calculus_vol_2_uri.split("/")[-1]
    cnx_url = f"{webview_base_url}{calculus_vol_2_uri}"
    response = get_url(cnx_url)

    # THEN we are redirected to rex
    if response.status_code != 200:
        log_failures_to_csv(response.status_code, cnx_url)

        pytest.fail(f"{response.status_code} in {cnx_page_slug}")

    else:
        assert response.url.startswith(rex_base_url)
