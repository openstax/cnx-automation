import pytest

"""
Creates a dictionary of styles:slugs for all github content repos.
Latest update on June 3rd, 2022
"""


@pytest.fixture
def abl_books_slugs_styles(abl_approved):

    """Returns dictionary of slug:style of all collection entries in ABL json"""

    slugs_styles = {}

    for i in abl_approved:
        book_versions = i["versions"]
        for j in book_versions:
            commit_metadata = j["commit_metadata"]["books"]
            for k in commit_metadata:
                slugs_styles[k["slug"]] = k["style"]

    return slugs_styles
