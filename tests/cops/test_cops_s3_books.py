from tests import markers
from urllib.request import urlopen
import json
import urllib
import requests


"""
Verifies collections in s3 bucket
Latest update on 01/02/2020
"""

s3_base_url = "https://d27639afyuqlps.cloudfront.net"

# @markers.ottoa
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

    url = f"{s3_base_url}" + "/baked/" + f"{uuids}" + ".json"

    page = urllib.request.urlopen(url).read()
    jdata = json.loads(page)

    raw_title = {v for k, v in jdata.items() if k == "title"}
    title = str(raw_title)[2:-2]

    response = requests.get(url)

    assert 200 == response.status_code
    assert (
        title == "American Government 2e"
        or title == "Astronomy"
        or title == "College Physics with Courseware"
        or title == "Introductory Statistics"
    )
