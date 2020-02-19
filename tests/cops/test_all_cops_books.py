from tests import markers
import pytest
import requests

import json
import urllib
from urllib.request import urlopen

from urllib.error import HTTPError

"""
Verifies which collections are present in the aws s3 bucket
Latest update on 05/02/2020
"""


@markers.awss3
@markers.nondestructive
def test_all_cops_books(selenium, s3_base_url, s3_books_titles, s3_books_url):

    try:
        # opens the collection urls and verifies which are in s3 bucket and which are not
        s3_page = urllib.request.urlopen(s3_books_url).read()

    except HTTPError as err:
        # skipping collection not it s3 bucket yet
        if err.code:
            pytest.skip(msg="Collection NOT in aws s3 bucket yet")
        else:
            raise
    else:
        # reading nested lists and getting slug names
        s3_jdata = json.loads(s3_page)
        s3_nest = s3_jdata["tree"]["contents"]
        s3_title = s3_jdata.get("title")

        slug_pref = s3_nest[0]["slug"]
        last_chap = s3_nest[-1]
        slug_index = last_chap["slug"]

        response = requests.get(s3_books_url)

        if slug_pref == "preface":
            # verifies all collections with preface and index sections
            assert slug_pref == "preface"
            assert slug_index == "index"
            assert 200 == response.status_code
            assert s3_title in s3_books_titles

        else:
            # verifies collections without preface, like College Physics with Courseware
            assert slug_index == "index"
            assert 200 == response.status_code
            assert s3_title in s3_books_titles
