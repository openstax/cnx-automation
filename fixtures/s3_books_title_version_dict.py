import pytest
import json

"""
Verifies which collections are present in the aws s3 bucket
Latest update on July 21, 2020
"""


@pytest.fixture
def s3_books_title_version_dict(s3_queue_state_bucket_books):

    # reading nested lists and getting slug names
    json_data = json.loads(s3_queue_state_bucket_books)

    name_list = []
    version_list = []
    for key in json_data:
        if key["name"]:
            name_list.append(key["name"])
        if key["version"]:
            version_list.append(key["version"])

    res = {name_list[i]: version_list[i] for i in range(len(version_list))}

    return res
