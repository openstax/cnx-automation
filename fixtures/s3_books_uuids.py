import pytest
import json

"""
Extracts book uuids from queue state bucket json
Latest update on Oct. 20th, 2020
"""


@pytest.fixture
def s3_books_uuids(s3_queue_state_bucket_books):

    # reading nested lists and getting slug names
    json_data = json.loads(s3_queue_state_bucket_books)

    json_data = json_data[::-1]

    uuid_list = []
    for key in json_data:
        if key["uuid"]:
            uuid_list.append(key["uuid"])

    return uuid_list
