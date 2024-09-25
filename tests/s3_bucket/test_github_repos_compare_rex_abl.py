"""
Compares uuids from rex/release.json and abl api
Run: pytest -k test_github_repos_compare_rex_abl.py tests/s3_bucket --rex_base_url https://openstax.org
Latest update on July 30th, 2024
"""


def test_github_repos_compare_rex_abl(rex_released_books, abl_books_uuids_slugs):
    match = []
    nomatch = []

    rex_uuid_list = list(rex_released_books.keys())

    for item in abl_books_uuids_slugs.items():
        print(f"--->>> Checking {item[1]}:")

        try:
            assert item[0] in rex_uuid_list

        except AssertionError as asse:
            nomatch.append(f"!!! No match {asse}")

        else:
            match.append("MATCH")

    if len(nomatch) > 0:
        print(f"NO MATCH: {nomatch}")
    else:
        print(f"NO MATCH: {len(nomatch)}")
        print(f"MATCH   : {len(match)}")
