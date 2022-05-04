import pytest

"""
Creates a dictionary of book uuid:slug for all github content repos.
Latest update on May 4th, 2022
"""


@pytest.fixture
def abl_books_uuids_slugs(abl_approved):

    """Returns dictionary of uuid:slug values of all collection entries in ABL json"""

    uuids_slugs = {}

    for i in abl_approved:
        book_versions = i["versions"]
        for j in book_versions:
            commit_metadata = j["commit_metadata"]["books"]
            for k in commit_metadata:
                uuids_slugs[k["uuid"]] = k["slug"]

    return uuids_slugs
