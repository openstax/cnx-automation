import csv
import json

import urllib
from urllib.request import urlopen

from urllib.error import HTTPError

"""
Verifies collections in the aws s3 bucket folder (for git pipeline)
Latest update on December 17th, 2021
"""


def test_s3_bucket_git_books(s3_archive_folder, abl_approved):

    repository_name = [i["repository_name"] for i in abl_approved if "repository_name" in i]
    versions = [i["versions"] for i in abl_approved if "versions" in i]

    valid_urls = []
    invalid_urls = []

    if repository_name:
        for ver in versions:
            for i in ver:
                short_sha = i["commit_sha"][0:7]
                commit_metadata = i["commit_metadata"]
                books = commit_metadata["books"]
                for book in books:
                    slug = book["slug"]
                    uuid = book["uuid"]

                    git_url = f"{s3_archive_folder}{book['uuid']}@{short_sha}.json"

                    try:
                        urllib.request.urlopen(git_url)

                    except HTTPError as htp:
                        # Return code 404, 501, ...
                        print(f"FAILED: {htp} {git_url} - {slug}")

                        invalid_urls.append(git_url)

                    else:
                        print(f"SUCCEEDED: {git_url} - {slug}")

                        s3_git_books_reqs = urllib.request.urlopen(git_url)

                        s3_git_books = s3_git_books_reqs.read()
                        s3_git_books_jdata = json.loads(s3_git_books)
                        s3_git_books_tree = s3_git_books_jdata["tree"]

                        valid_urls.append(git_url)

                        try:

                            assert s3_git_books_jdata["title"] != " "
                            assert s3_git_books_jdata["slug"] in slug
                            assert s3_git_books_jdata["id"] in uuid
                            assert "<body>" and "</span>" in s3_git_books_jdata["content"]

                            assert len(s3_git_books_tree["id"]) > 1
                            assert s3_git_books_tree["contents"] != " "

                            assert s3_git_books_reqs.getcode() == 200

                        except AssertionError:
                            print(f"Assertion error in {uuid} - {slug}")

                        else:
                            continue

                # Write the report CSV (into the root folder of the repo)
                with open("git_report.csv", "w", newline="") as csvfile:
                    fields_s = ["VALID URLS"]
                    fields_f = ["INVALID URLS"]

                    writer = csv.writer(csvfile, delimiter="\n")
                    writer.writerow(fields_s)
                    writer.writerow(valid_urls)

                    writer.writerow(fields_f)
                    writer.writerow(invalid_urls)
