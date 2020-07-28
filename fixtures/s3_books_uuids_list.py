import pytest
import json

"""
Verifies which collections are present in the aws s3 bucket
Latest update on July 21, 2020
"""


@pytest.fixture
def s3_books_uuids_list(s3_base_url, s3_queue_state_bucket_books):

    # reading nested lists and getting slug names
    json_data = json.loads(s3_queue_state_bucket_books)

    json_data = json_data[::-1]

    # json list to dict, so the latest name will override, and take care of duplicates
    json_data_new = {item["name"]: item for item in json_data}
    # convert back to list, will contain no duplicates
    non_dups = list(json_data_new.values())

    all_uuid_list = []
    for key in non_dups:
        if key["uuid"]:
            all_uuid_list.append(key["uuid"])

    return all_uuid_list
