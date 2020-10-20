import urllib
import json
from urllib.request import urlopen

from itertools import cycle

from urllib.error import HTTPError

import requests
import os

import boto3

"""
Verifies collections in the aws s3 bucket against queue-state list of approved books
Latest update on Oct. 20th, 2020
"""


def test_create_queue_state_books_list(
    aws_access_key_id_value, aws_secret_access_key_value, code_tag, queue_state_bucket
):

    # Ripal's code: creates a json file of approved books from queue-state list containing these details:
    # collection_id, style, version, server, uuid

    # apply aws credentials to access s3 buckets
    os.environ["AWS_ACCESS_KEY_ID"] = aws_access_key_id_value
    os.environ["AWS_SECRET_ACCESS_KEY"] = aws_secret_access_key_value

    client = boto3.client("s3")

    # queue state bucket containing approved books list with their corresponding states. Can be applied by
    # --state_bucket bucket-name
    # staging/sandbox environment "openstax-sandbox-web-hosting-content-queue-state"
    # production environment "openstax-web-hosting-content-queue-state"
    s3_queue_state_bucket = queue_state_bucket

    # code tag of each new deployment in s3 bucket. Can be applied by --code_tag code.number
    code_tag = code_tag

    # queue filename set in the bakery environment, same for both staging and production
    queue_filename = "distribution-queue.json"

    json_output_filename = f"{os.getcwd()}/fixtures/data/webview/s3_bucket_books.json"

    s3_bucket_books = []

    queue_state_key = f"{code_tag}.{queue_filename}"

    resp = client.list_object_versions(Bucket=s3_queue_state_bucket, Prefix=queue_state_key)

    versions = resp["Versions"]

    for version in versions:
        resp = client.get_object(
            Bucket=s3_queue_state_bucket, Key=queue_state_key, VersionId=version["VersionId"]
        )
        s3_bucket_books.append(json.loads(resp["Body"].read()))

    # writes the json file with required book details (see the top message)
    with open(json_output_filename, "w") as json_output_file:
        json.dump(s3_bucket_books, json_output_file)


def test_page_content(
    bucket_books_tree, s3_books_title_version_dict, s3_books_uuids, code_tag, s3_base_url
):

    # path to the aws s3 bucket folder
    s3_archive_folder = f"/apps/archive/{code_tag}/contents/"

    book_id = []
    book_title = []

    # creates list of book uuids and titles from the books in the aws s3 bucket
    for elem in range(len(bucket_books_tree)):

        book_id.clear()
        uuids_vers = bucket_books_tree[elem]["id"]
        book_id.append(uuids_vers[0 : uuids_vers.index("@")])

        book_title.clear()
        book_title.append(bucket_books_tree[elem]["title"])

        title_results = list(s3_books_title_version_dict.keys())

        try:

            # compares book uuids in the queue-state list against actual books in aws s3 bucket
            assert [j for j in book_id if j in s3_books_uuids]

        except AssertionError as as_error:

            print(f"{as_error}: book id {book_id} : {book_title} not found, next item")

        try:

            # compares book titles in the queue-state list against actual books in aws s3 bucket
            assert [i for i in book_title if i in title_results]

        except AssertionError as as_error:

            print(f"{as_error}: book title {book_title} : {book_id} not found, next item")

        else:

            book_tree_contents = bucket_books_tree[elem]["contents"]

            for content in range(len(book_tree_contents)):

                try:
                    page_id = book_tree_contents[content]["contents"]

                    page_id_noversion = []

                # checking for exceptions when iteration runs out of "contents" item
                except (KeyError, IndexError):
                    continue

                else:

                    # extracts the page ids from books in aws s3 bucket and removes their versions
                    for pid in range(0, len(page_id), 6):

                        page_ids = page_id[pid]["id"]
                        page_id_noversion.append(page_ids[0 : page_ids.index("@")])

                        uuid_dict = dict(zip(page_id_noversion, cycle(book_id)))

                        # reconstructs the complete book:page url
                        s3_pages_full_url = [
                            f"{s3_base_url}{s3_archive_folder}{i}:{j}.json"
                            for i, j in zip(uuid_dict.values(), uuid_dict.keys())
                        ]

                        # iterates through pages in books and asserts that content exists
                        for pages in range(len(s3_pages_full_url)):

                            response = requests.get(s3_pages_full_url[pages])

                            try:

                                s3_pages = urllib.request.urlopen(s3_pages_full_url[pages]).read()
                                s3_pages_jdata = json.loads(s3_pages)

                                s3_page_title = s3_pages_jdata.get("title")
                                s3_page_content = s3_pages_jdata.get("content")

                                assert s3_page_title != ""
                                assert s3_page_content != ""

                                assert 200 == response.status_code

                            # checking for exceptions as some page urls are non-clickable
                            except HTTPError:
                                continue

                            except AssertionError as aa_errors:
                                print(
                                    f"{aa_errors}, page title or content is empty in {book_title} / {s3_page_title}, "
                                    f"next item "
                                )
                            else:
                                page_id_noversion.clear()
                                continue
