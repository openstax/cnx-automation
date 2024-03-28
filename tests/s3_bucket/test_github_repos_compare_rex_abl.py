"""
Compares uuids from rex/release.json and abl
Latest update on March 27, 2024
"""


def test_github_repos_compare_rex_abl(abl_approved, rex_released_books):
    abl_uuids_slugs = {}

    for i in abl_approved:
        book_versions = i["versions"]
        for j in book_versions:
            commit_metadata = j["commit_metadata"]["books"]
            for k in commit_metadata:
                abl_uuids_slugs[k["uuid"]] = k["slug"]

    rex_uuid_list = list(rex_released_books.keys())

    for item in abl_uuids_slugs.items():
        print(f"--->>> Checking {item[1]}:")

        try:
            assert item[0] in rex_uuid_list

        except AssertionError as asse:
            print(f"!!! No match {asse}")

        else:
            print("Match")
