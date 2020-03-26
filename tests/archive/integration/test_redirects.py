import requests

from tests import markers


@markers.archive
@markers.nondestructive
@markers.parametrize("uuid", [("fea3130c-6e57-41b2-a00f-0267ffae273c")])
def test_location_header_applied_to_redirect(archive_base_url, uuid):
    # GIVEN an "archive" URL and Host Header
    url = f"{archive_base_url}/contents/{uuid}"
    headers = {"Host": "openstax.org"}

    # WHEN a web request has a host
    response = requests.get(url=url, headers=headers, allow_redirects=False)

    # THEN the host value is used in the Location header of the redirect
    assert headers["Host"] in response.headers["Location"]


@markers.archive
@markers.webview
@markers.nondestructive
@markers.parametrize("uuid, version", [("fea3130c-6e57-41b2-a00f-0267ffae273c", 5)])
def test_headers_for_google_results(archive_base_url, uuid, version):
    # end-to-end integration test for redirecting google away from archive URLs
    # see: https://github.com/openstax/cnx/issues/209

    # GIVEN an "archive" URL
    url = f"{archive_base_url}/contents/{uuid}@{version}"

    # WHEN a web request comes from Google
    response = requests.get(url=url, headers={"Referer": "https://google.com/"})

    # THEN we redirect to the canonical URL (which is served by webview)
    assert "archive" not in response.headers["Location"]
    assert response.headers["Location"] == response.headers["X-Varnish-Canonical-Url"]
    assert response.headers["X-Varnish-Status"] == "uncacheable - redirected google"
