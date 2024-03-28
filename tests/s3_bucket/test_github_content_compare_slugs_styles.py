import requests

import urllib.parse
from urllib.error import HTTPError

import pytest

from bs4 import BeautifulSoup


"""
Compares slugs/styles between books.xml and ABL file of every collection in github content repo.
Latest update on June 7th, 2022
"""


def test_github_content_compare_slugs_styles(
    git_content_repos, headers_data, abl_books_slugs_styles
):
    for repo in git_content_repos:
        print("\nNow verifying: ", repo)

        meta_inf_dir = f"https://api.github.com/repos/openstax/{repo}/contents/META-INF/"

        meta_inf_list = requests.get(meta_inf_dir, headers=headers_data)

        if meta_inf_list.status_code != 200:
            # Return code 404, 501, ... for incorrect meta-inf url
            print(f">>>>> FAILED {meta_inf_list.status_code}: no meta-inf folder in {repo}")

        else:
            for item in meta_inf_list.json():
                if item["type"] != "file":
                    # Ignore anything that may not be a file
                    continue

                else:
                    rel_path = urllib.parse.quote(item["path"])
                    meta_inf_url = (
                        f"https://api.github.com/repos/openstax/{repo}/contents/{rel_path}"
                    )

                    if "books.xml" not in meta_inf_url:
                        print(f"!!! boosk.xml is missing in {repo}")

                    else:
                        try:
                            meta_inf_resp = requests.get(meta_inf_url, headers=headers_data)
                            meta_inf_resp.raise_for_status()

                        except HTTPError as h_e:
                            # Return code 404, 501, ... for incorrect/missing books.xml
                            pytest.fail(
                                f"HTTP Error {h_e.code}: incorrect/missing books.xml {meta_inf_url}"
                            )

                        else:
                            meta_inf_resp = requests.get(meta_inf_url, headers=headers_data)

                            resp_content = meta_inf_resp.text

                            soup = BeautifulSoup(resp_content, "xml")
                            book_tags = soup.find_all("book")

                            for btag in book_tags:
                                try:
                                    btag["slug"]

                                except (KeyError, AttributeError):
                                    print("---> Key error - slug tag is missing")

                                else:
                                    slug_text = btag["slug"]

                                    try:
                                        # Compare slugs in books.xml against slugs in ABL
                                        assert slug_text in abl_books_slugs_styles.keys()

                                    except (AssertionError, AttributeError):
                                        print(f"slug mismatch: {slug_text}")

                                    else:
                                        continue
