import pytest
import json

import urllib
from urllib.request import urlopen

from urllib.error import HTTPError

"""
Returns the content tree of each collection in aws s3 bucket
Latest update on Oct. 14th, 2020
"""


@pytest.fixture
def bucket_books_tree(s3_base_url, code_tag, s3_queue_state_bucket_books):

    s3_archive_folder = f"/apps/archive/{code_tag}/contents/"

    # reading nested lists and getting slug names
    json_data = json.loads(s3_queue_state_bucket_books)
    json_data = json_data[::-1]

    uuid_list = []
    version_list = []
    for key in json_data:
        if key["uuid"]:
            uuid_list.append(key["uuid"])
        if key["version"]:
            version_list.append(key["version"])

    for i in range(0, len(version_list)):
        version_list[i] = version_list[i][2:]

    approved_books_full_url = [
        f"{s3_base_url}{s3_archive_folder}{i}@{j}.json" for i, j in zip(uuid_list, version_list)
    ]

    # list of approved book urls without http errors
    book_tree = []

    for books in approved_books_full_url:

        try:
            urllib.request.urlopen(books)
        except HTTPError as h_e:
            # Return code 404, 501, ...
            print("HTTPError (check concourse jobs): {}".format(h_e.code) + ", " + books)
        else:
            # Return code 200
            s3_books = urllib.request.urlopen(books).read()
            s3_jdata = json.loads(s3_books)
            book_tree.append(s3_jdata["tree"])
            continue

    return book_tree
