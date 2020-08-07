import pytest
import json

import urllib
from urllib.request import urlopen

"""
Verifies which collections are present in the aws s3 bucket
Latest update on Aug. 6th, 2020
"""


@pytest.fixture
def bucket_books_tree(s3_base_url, s3_queue_state_bucket_books):

    s3_archive_folder = "/apps/archive/master/contents/"

    # reading nested lists and getting slug names
    json_data = json.loads(s3_queue_state_bucket_books)
    json_data = json_data[::-1]

    # json list to dict, so the latest name will override, and take care of duplicates
    json_data_new = {item["name"]: item for item in json_data}
    # convert back to list, will contain no duplicates
    non_duplicates = list(json_data_new.values())

    uuid_list = []
    version_list = []
    for key in non_duplicates:
        if key["uuid"]:
            uuid_list.append(key["uuid"])
        if key["version"]:
            version_list.append(key["version"])

    for i in range(0, len(version_list)):
        version_list[i] = version_list[i][2:]

    approved_books_full_url = [
        f"{s3_base_url}{s3_archive_folder}{i}@{j}.json" for i, j in zip(uuid_list, version_list)
    ]

    book_tree = []

    for books in range(len(approved_books_full_url)):

        s3_books = urllib.request.urlopen(approved_books_full_url[books]).read()

        s3_jdata = json.loads(s3_books)
        book_tree.append(s3_jdata["tree"])

    return book_tree
