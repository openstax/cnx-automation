import requests
from tests import markers

cops_base_url = "https://cops-staging.openstax.org"


@markers.nondestructive
def test_cops_ui(selenium):

    # GIVEN an archive URL for a book
    url = f"{cops_base_url}"

    # WHEN making a request to Archive
    response = requests.get(url)

    # THEN we should NOT redirect to REX
    assert response.status_code == 200
