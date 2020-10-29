import pytest
import json


"""
Returns full urls for approved books
Latest update on Oct. 28th, 2020
"""


@pytest.fixture
def approved_books_full_url(s3_queue_state_bucket_books, s3_archive_folder):

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
        f"{s3_archive_folder}{i}@{j}.json" for i, j in zip(uuid_list, version_list)
    ]

    return approved_books_full_url
