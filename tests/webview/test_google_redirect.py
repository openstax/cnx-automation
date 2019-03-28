from requests import get

from tests import markers


@markers.webview
@markers.nondestructive
@markers.parametrize("uuid, version", [("fea3130c-6e57-41b2-a00f-0267ffae273c", 5)])
def test_google_redirect_archive_results(archive_base_url, uuid, version):
    # end-to-end integration test for redirecting google away from archive URLs
    # see: https://github.com/openstax/cnx/issues/209

    # GIVEN an "archive" URL
    url = "{}/contents/{}@{}".format(archive_base_url, uuid, version)

    # WHEN a web request comes from Google
    res = get(url=url, headers={"Referer": "https://google.com/"})

    # THEN we (via Varnish) redirect to the canonical URL (served by webview)
    assert "archive" not in res.headers["Location"]
    assert res.headers["Location"] == res.headers["X-Varnish-Canonical-Url"]
    assert res.headers["X-Varnish-Status"] == "uncacheable - redirected google"
