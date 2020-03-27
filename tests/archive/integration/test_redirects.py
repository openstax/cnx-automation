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
