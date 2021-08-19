import requests

import urllib.parse
from urllib.error import HTTPError

import pytest

"""
Searches for a string in all index.cnxml of a particular content repo or all existing osbooks- content repos
Latest update on August 12th, 2021
"""


def test_search_github_content_repos(git_content_repos, headers_data):

    string_to_search = input("\nEnter string to search for: ")

    repo_to_search = input(
        "\nEnter content repo name (or press ENTER to search through all osbooks- repos): "
    )

    for repo in git_content_repos:

        if repo_to_search not in repo:

            continue

        else:

            print(f'\nSearching for "{string_to_search}" in modules of: ', repo)

            modules_dir = f"https://api.github.com/repos/openstax/{repo}/contents/modules/"

            try:

                modules_list = requests.get(modules_dir, headers=headers_data)

            except HTTPError as h_e:
                # Return code 404, 501, ... for incorrect modules url
                pytest.fail(f"HTTP Error {h_e.code}: incorrect modules url {modules_dir}")

            else:

                for item in modules_list.json():

                    if item["type"] != "dir":

                        # Ignore anything that may not be a directory
                        continue

                    rel_path = urllib.parse.quote(item["path"])
                    modules_url = f"https://api.github.com/repos/openstax/{repo}/contents/{rel_path}/index.cnxml"

                    try:
                        module_resp = requests.get(modules_url, headers=headers_data)

                    except HTTPError as h_e:
                        # Return code 404, 501, ... for incorrect/missing index.cnxml
                        pytest.fail(
                            f"HTTP Error {h_e.code}: incorrect/missing index.cnxml {modules_url}"
                        )

                    else:
                        xhtml_data = module_resp.text
                        found_data = xhtml_data.find(string_to_search)

                        if found_data >= 1:

                            print(
                                f'String "{string_to_search}" found in {modules_url}: ', found_data
                            )

                        else:

                            continue
