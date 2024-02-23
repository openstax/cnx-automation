import re

import requests

import urllib.parse

from bs4 import BeautifulSoup


"""
Verifies math and m:math tags to make sure they are not empty
Latest update on February 23rd, 2024
"""


def test_github_content_repo_equation(git_content_repos, headers_data):
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
                equation = soup.find_all("equation")

                for equ in equation:
                    try:
                        assert equ.find_all(re.compile(r"(m:math|math)"))

                    except AssertionError:
                        continue

                    else:
                        for matek in equ.find_all(re.compile(r"(m:math|math)")):
                            try:
                                assert len(matek.text.strip()) > 0

                            except AssertionError as asse:
                                print(f"{item['name']} - {asse}")
