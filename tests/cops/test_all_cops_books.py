from tests import markers
import pytest
import requests

import json
import urllib
from urllib.request import urlopen

from urllib.error import HTTPError


"""
Verifies which collections are present in the aws s3 bucket
Latest update on 07/08/2020
"""


@pytest.mark.xfail(raises=(AssertionError, HTTPError))
@markers.awss3
@markers.nondestructive
def test_verify_collections_in_s3_bucket(selenium, s3_books_title_list, s3_books_full_url_list):

    for books in range(len(s3_books_full_url_list)):

        try:
            # opens the collection urls and verifies which are in s3 bucket and which are not
            s3_books = urllib.request.urlopen(s3_books_full_url_list[books]).read()

        except HTTPError as err:
            # skipping collection not in s3 bucket yet

            # and getting the title(s) of missing book(s)
            missing_book = s3_books_full_url_list[books].replace(
                "sandbox.openstax.org/apps/archive/master", "cnx.org"
            )
            missing_split = missing_book.split("@", 1)[0]
            missing_format = "{0}.json".format(missing_split)
            missing_data = urllib.request.urlopen(missing_format).read()
            s3_exception = json.loads(missing_data)
            missing_title = s3_exception.get("title")

            if err.code:
                print(f"\n!!!!!!! COLLECTION NOT IN THE AWS S3 BUCKET YET: {missing_title} \n", err)
                pass
            else:
                raise

        else:

            try:
                # reading nested lists and getting slug names
                s3_jdata = json.loads(s3_books)
                s3_nest = s3_jdata["tree"]["contents"]
                s3_title = s3_jdata.get("title")

                slug_pref = s3_nest[0]["slug"]
                last_chap = s3_nest[-1]
                slug_index = last_chap["slug"]

                response = requests.get(s3_books_full_url_list[books])

                if slug_pref == "preface" and slug_index == "index":
                    # verifies all collections with preface and index sections
                    assert slug_pref == "preface"
                    assert slug_index == "index"
                    assert 200 == response.status_code
                    assert s3_title in s3_books_title_list

                elif slug_pref == "preface" and slug_index == "references":
                    # verifies all collections with preface and references sections
                    assert slug_pref == "preface"
                    assert slug_index == "references"
                    assert 200 == response.status_code
                    assert s3_title in s3_books_title_list

            except AssertionError as err2:
                if err2:
                    print(f"\n!!!!!!! ASSERTION ERROR EXCEPTION: {s3_title}\n", err2)
                    continue
                else:
                    raise
