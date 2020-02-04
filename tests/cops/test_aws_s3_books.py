from tests import markers
import requests

"""
Verifies presents of collections in aws s3 bucket
Latest update on 03/02/2020
"""


@markers.awss3
@markers.nondestructive
def test_aws_s3_books(selenium, s3_books_url, s3_json_data, s3_books_titles, s3_books_uuids):

    # GIVEN s3 bucket url converted json file
    # WHEN we get slugs from embedded dictionary/list of the json file

    s3_title = s3_json_data.get("title")

    s3_nest = s3_json_data["tree"]["contents"]
    slug_pref = s3_nest[0]["slug"]

    last_chap = s3_nest[-1]
    slug_index = last_chap["slug"]

    response = requests.get(s3_books_url)

    # THEN we verify and assert

    if slug_pref == "preface":
        assert slug_pref == "preface"
        assert slug_index == "index"
        assert 200 == response.status_code
        assert s3_title in s3_books_titles

    else:
        assert slug_index == "index"
        assert 200 == response.status_code
        assert s3_title in s3_books_titles
