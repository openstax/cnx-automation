import requests

from tests import markers


@markers.webview
@markers.nondestructive
@markers.parametrize("uuid, version", [("fea3130c-6e57-41b2-a00f-0267ffae273c", 5)])
def test_archive_redirect_for_google_results(archive_base_url, uuid, version):
    # end-to-end integration test for redirecting google away from archive URLs
    # see issue: https://github.com/openstax/cnx/issues/209

    # GIVEN an "archive" URL
    url = f"{archive_base_url}/contents/{uuid}@{version}"

    # WHEN a web request comes from Google
    response = requests.get(url=url, headers={"Referer": "https://google.com/"})

    # THEN we redirect to the canonical URL (which is served by webview)
    assert "archive" not in response.headers["Location"]
    assert response.headers["Location"] == response.headers["X-Varnish-Canonical-Url"]
    assert response.headers["X-Varnish-Status"] == "uncacheable - redirected google"
