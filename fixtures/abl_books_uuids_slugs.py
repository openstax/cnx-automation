import pytest

"""
Creates a dictionary of book uuid:slug for all github content repos.
Latest update on April 29th, 2022
"""


@pytest.fixture
def abl_books_uuids_slugs(abl_approved):

    slugs = []
    uuids = []

    for i in abl_approved:
        book_versions = i["versions"]
        for j in book_versions:
            commit_metadata = j["commit_metadata"]["books"]
            for k in commit_metadata:
                slugs.append(k["slug"])

    for i in abl_approved:
        book_versions = i["versions"]
        for j in book_versions:
            commit_metadata = j["commit_metadata"]["books"]
            for k in commit_metadata:
                uuids.append(k["uuid"])

    uuids_slugs = {uuids[i]: slugs[i] for i in range(len(uuids))}

    return uuids_slugs
