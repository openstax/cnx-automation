from tests import markers
from urllib.request import urlopen
import json
import urllib
import pytest
import requests

"""
Verifies collections in s3 bucket
Latest update on 01/02/2020
"""

s3_base_url = "https://d27639afyuqlps.cloudfront.net"


@markers.nondestructive
@markers.parametrize(
    "uuids",
    [
        "9d8df601-4f12-4ac1-8224-b450bf739e5f",
        "2e737be8-ea65-48c3-aa0a-9f35b4c6a966",
        "405335a3-7cff-4df2-a9ad-29062a4af261",
        "30189442-6998-4686-ac05-ed152b91b9de",
    ],
)
def test_cops_s3_books(selenium, uuids):

    s3_url = f"{s3_base_url}" + "/baked/" + f"{uuids}" + ".json"

    s3_page = urllib.request.urlopen(s3_url).read()
    s3_jdata = json.loads(s3_page)

    s3_title = s3_jdata.get("title")

    s3_nest = s3_jdata["tree"]["contents"]
    slug_name = s3_nest[0]["slug"]
    response = requests.get(s3_url)

    if slug_name == "preface":
        assert slug_name == "preface"
        assert 200 == response.status_code
        assert (
            s3_title == "American Government 2e"
            or s3_title == "Astronomy"
            or s3_title == "College Physics with Courseware"
            or s3_title == "Introductory Statistics"
        )

    elif slug_name != "preface":
        assert 200 == response.status_code
        assert (
            s3_title == "American Government 2e"
            or s3_title == "Astronomy"
            or s3_title == "College Physics with Courseware"
            or s3_title == "Introductory Statistics"
        )

        pytest.skip(msg="Skipping slug[0] verification as it is NOT preface")
