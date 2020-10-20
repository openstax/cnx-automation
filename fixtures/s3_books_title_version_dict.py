import pytest
import json

"""
Creates a dictionary of book titles and their corresponding versions from queue state bucket json
Latest update on Oct. 19th, 2020
"""


@pytest.fixture
def s3_books_title_version_dict(s3_queue_state_bucket_books):

    # reading nested lists and getting slug names
    json_data = json.loads(s3_queue_state_bucket_books)

    json_data = json_data[::-1]

    name_list = []
    version_list = []
    for key in json_data:
        if key["name"]:
            name_list.append(key["name"])
        if key["version"]:
            version_list.append(key["version"])

    res = {name_list[i]: version_list[i] for i in range(len(version_list))}

    return res
