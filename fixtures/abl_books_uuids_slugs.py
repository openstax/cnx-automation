import pytest

"""
Creates a dictionary of book uuid:slug for all github content repos.
Latest update on July 30th, 2024
"""


@pytest.fixture
def abl_books_uuids_slugs(abl_api_approved):
    """Returns dictionary of uuid:slug values of all collection entries in ABL api"""

    uuids_slugs = {}

    for i in abl_api_approved:
        uuids_slugs[i["uuid"]] = i["slug"]

    return uuids_slugs
