import requests

from tests import markers


@markers.archive
@markers.nondestructive
@markers.parametrize("uuid", ["36004586-651c-4ded-af87-203aca22d946"])
def test_location_header_applied_to_redirect(archive_base_url, uuid):
    # GIVEN an "archive" URL and Host Header
    url = f"{archive_base_url}/contents/{uuid}"
    headers = {"Host": "openstax.org"}

    # WHEN a web request has a host
    response = requests.get(url=url, headers=headers, allow_redirects=False)

    # THEN the host value is used in the Location header of the redirect
    assert headers["Host"] in response.headers["Location"]


@markers.archive
@markers.nondestructive
@markers.parametrize("uuid, version", [("36004586-651c-4ded-af87-203aca22d946", 5)])
def test_redirect_headers_for_google_results(archive_base_url, uuid, version):
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


@markers.test_case("C553086")
@markers.rex
@markers.archive
@markers.nondestructive
def test_archive_is_still_reachable(archive_base_url, rex_base_url):
    """REX still needs a way to fetch the content from Archive without being redirected
    """
    # GIVEN an archive URL for a book
    url = f"{archive_base_url}/contents/f8zJz5tx@11.3:Pw-p-yeP@10/10-3-Phase-Transitions"

    # WHEN making a request to Archive
    response = requests.get(url)

    # THEN we should NOT redirect to REX
    for hist in response.history:
        assert rex_base_url not in hist.headers["location"]
