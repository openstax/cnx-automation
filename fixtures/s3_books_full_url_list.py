import pytest
import json
import urllib
from urllib.request import urlopen

"""
Verifies which collections are present in the aws s3 bucket
Latest update on 07/08/2020
"""


@pytest.fixture
def s3_books_full_url_list(s3_base_url, s3_approved_books_json_url):

    s3_archive_folder = "/apps/archive/master/contents/"

    # opens the collection urls and verifies which are in s3 bucket and which are not
    read_approved_books_json = urllib.request.urlopen(s3_approved_books_json_url).read()

    # reading nested lists and getting slug names
    json_data = json.loads(read_approved_books_json)

    # removes the old version of Microbiology collection from the list
    json_data_alt = [
        i for i in json_data if not (i["name"] == "Microbiology" and i["version"] == "1.8.6")
    ]

    uuid_list = [""]
    j = 0
    for i in json_data_alt:
        if j == 0:
            uuid_list[0] = i["uuid"]
        else:
            uuid_list.append(i["uuid"])
        j += 1

    version_list = [""]
    j = 0
    for i in json_data_alt:
        if j == 0:
            version_list[0] = i["version"]
        else:
            version_list.append(i["version"])
        j += 1

    for i in range(0, len(version_list)):
        version_list[i] = version_list[i][2:]

    s3_books_full_url = [
        f"{s3_base_url}{s3_archive_folder}{i}@{j}.json" for i, j in zip(uuid_list, version_list)
    ]

    return s3_books_full_url
