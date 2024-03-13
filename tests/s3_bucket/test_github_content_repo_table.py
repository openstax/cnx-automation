import re

import requests

import urllib.parse

from bs4 import BeautifulSoup


"""
Verifies the table tags of each index.cnxml file
Latest update on February 27th, 2024
"""


def test_github_content_repo_table(git_content_repos, headers_data):
    # checks all the github content repos within given index range
    sindex = int(input("Enter start index of a content repo: "))
    eindex = int(input("Enter end index a content repo: "))

    for repo in git_content_repos[sindex:eindex]:
        print("\nNow verifying: ", repo)

        contents_dir = f"https://api.github.com/repos/openstax/{repo}/contents"
        modules_dir = f"{contents_dir}/modules/"

        modules_list = requests.get(modules_dir, headers=headers_data)

        for item in modules_list.json():
            rel_path = urllib.parse.quote(item["path"])

            if item["type"] != "dir":
                print(f"Exclude file(s): {rel_path}")
                continue

            index_url = f"{contents_dir}/{rel_path}/index.cnxml"

            module_resp = requests.get(index_url, headers=headers_data)

            if module_resp.status_code in range(400, 501):
                print(
                    f"Error code {module_resp.status_code}: Incorrect/missing index file in {repo} / {rel_path}"
                )
                continue

            else:
                resp_content = module_resp.text

                soup = BeautifulSoup(resp_content, "xml")
                tablet = soup.find_all("table")

                if tablet:
                    for tbl in tablet:
                        try:
                            tgroups = tbl.find_all("tgroup")
                            assert tgroups

                        except AssertionError as assen:
                            print(f'TGROUP TAG ISSUE: {item["name"]} - {assen}')

                        else:
                            for tgroup in tgroups:
                                try:
                                    assert tgroup(re.compile(r"(entry|row)"))

                                except AssertionError as asser:
                                    print(f'TABLE TAG ISSUE: {item["name"]} - {asser}')

                                else:
                                    if len(tbl.text.strip()) == 0:
                                        try:
                                            assert tgroup("media")

                                        except AssertionError as asse:
                                            print(f'MEDIA TAG ISSUE: {item["name"]} - {asse}')

                                    else:
                                        continue
