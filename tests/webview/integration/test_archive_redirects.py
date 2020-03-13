import requests

from tests import markers

@markers.nondestructive
@markers.parametrize("uuid", [("fea3130c-6e57-41b2-a00f-0267ffae273c")])
def test_archive_redirect(archive_base_url, uuid):
    # GIVEN an "archive" URL
    url = f"{archive_base_url}/contents/{uuid}"

    # WHEN a web request has a host
    response = requests.get(url=url, headers={"Host": "openstax.org"}, allow_redirects=False)

    # THEN the host is used in the redirect 
    assert "openstax.org" in response.headers["Location"]
