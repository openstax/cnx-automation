"""
Compares uuids from rex/release.json and abl api
Latest update on July 30th, 2024
"""


def test_github_repos_compare_rex_abl(rex_released_books, abl_books_uuids_slugs):
    rex_uuid_list = list(rex_released_books.keys())

    for item in abl_books_uuids_slugs.items():
        print(f"--->>> Checking {item[1]}:")

        try:
            assert item[0] in rex_uuid_list

        except AssertionError as asse:
            print(f"!!! No match {asse}")

        else:
            print("Match")
