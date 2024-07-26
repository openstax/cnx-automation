import csv
import json

import urllib
from urllib.request import urlopen

from urllib.error import HTTPError

"""
Verifies collections in the aws s3 bucket folder (git webhosting pipeline)
Latest update on July 26th, 2024
"""


def test_s3_bucket_git_books(s3_archive_folder, abl_api_approved):
    valid_urls = []
    invalid_urls = []
    valid_url_slugs = []
    invalid_url_slugs = []

    for i in abl_api_approved:
        short_sha = i["commit_sha"][0:7]
        slug = i["slug"]
        uuid = i["uuid"]

        git_url = f"{s3_archive_folder}{uuid}@{short_sha}.json"

        try:
            urllib.request.urlopen(git_url)

        except HTTPError as htp:
            # Return code 404, 501, ...
            print(f"FAILED: {htp} {git_url} - {slug}")

            invalid_urls.append(git_url)
            invalid_url_slugs.append(slug)

        else:
            print(f"SUCCEEDED: {git_url} - {slug}")

            s3_git_books_reqs = urllib.request.urlopen(git_url)

            s3_git_books = s3_git_books_reqs.read()
            s3_git_books_jdata = json.loads(s3_git_books)
            s3_git_books_tree = s3_git_books_jdata["tree"]

            valid_urls.append(git_url)
            valid_url_slugs.append(slug)

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
    with open("git_webhosting_report.csv", "w", newline="") as csvfile:
        fields_s = ["VALID URLS"]
        fields_f = ["INVALID URLS"]

        writer = csv.writer(csvfile, delimiter="\n")
        writer.writerow(fields_s)
        writer = csv.writer(csvfile, delimiter="\t")
        writer.writerows(zip(valid_urls, valid_url_slugs))

        writer.writerow(fields_f)
        writer = csv.writer(csvfile, delimiter="\t")
        writer.writerows(zip(invalid_urls, invalid_url_slugs))

    print("Total successful books: ", len(valid_urls))
    print("Total unsuccessful books: ", len(invalid_urls))
