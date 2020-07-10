import pytest
import json
import urllib
from urllib.request import urlopen

"""
Verifies which collections are present in the aws s3 bucket
Latest update on 07/02/2020
"""


@pytest.fixture
def s3_books_title_version_dict(s3_approved_books_json_url):

    # opens the collection urls and verifies which are in s3 bucket and which are not
    read_approved_books_json = urllib.request.urlopen(s3_approved_books_json_url).read()

    # reading nested lists and getting slug names
    json_data = json.loads(read_approved_books_json)

    name_list = [""]
    j = 0
    for i in json_data:
        if j == 0:
            name_list[0] = i["name"]
        else:
            name_list.append(i["name"])
        j += 1

    version_list = [""]
    j = 0
    for i in json_data:
        if j == 0:
            version_list[0] = i["version"]
        else:
            version_list.append(i["version"])
        j += 1

    res = {name_list[i]: version_list[i] for i in range(len(version_list))}

    return res
