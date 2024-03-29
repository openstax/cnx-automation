import csv
import json

import urllib
from urllib.request import urlopen

from urllib.error import HTTPError

import requests
from lxml import etree

import os
import boto3

"""
Verifies pages of collections in the aws s3 bucket folder
Latest update on May 20th, 2021
"""


def test_create_queue_state_books_list(
    code_tag, queue_state_bucket, queue_filename,
):

    # Ripal's code: creates a json file of approved books from queue-state list containing these details:
    # collection_id, style, version, server, uuid

    # First, set aws tokens via set_aws_creds every time you run these tests,
    # assuming that 'aws configure' was already run to set your credentials for openstax-users
    # (follow steps in https://github.com/openstax/aws-access#assuming-a-role)

    client = boto3.client("s3")

    # queue state bucket containing approved books list with their corresponding states. Can be applied by
    # --state_bucket bucket-name
    # staging/sandbox environment "openstax-sandbox-web-hosting-content-queue-state"
    # production environment "openstax-web-hosting-content-queue-state"
    s3_queue_state_bucket = queue_state_bucket

    # code tag of each new deployment in s3 bucket. Can be applied by --code_tag code.number
    code_tag = code_tag

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
        # Note: We reverse the books when writing them so they end up in the
        # build order since list_object_versions will return items from
        # most recent to latest
        json.dump(list(reversed(s3_bucket_books)), json_output_file)


def test_s3_bucket_books(s3_queue_state_bucket_books, s3_archive_folder, concourse_prefix):

    successful_books = []
    tested_books = []
    tested_book_hashes = set()

    json_data = json.loads(s3_queue_state_bucket_books)

    # We start with one to account for the fact that job ID 1 is the "burn job"
    # in the pipeline and the first "real" job has ID 2
    job_id = 1

    for book in json_data:
        job_id += 1
        # FIXME: This version logic to remove the "1." prefix won't work for git pipelines
        book_hash = f"{book['uuid']}@{book['version'][2:]}"
        if book_hash in tested_book_hashes:
            continue
        else:
            tested_book_hashes.add(book_hash)

        url = f"{s3_archive_folder}{book_hash}.json"

        try:
            req_url = urllib.request.urlopen(url)

        except HTTPError as h_e:
            # Return code 404, 501, ...
            book.update(
                {
                    "status": "FAILURE",
                    # If a book failed, we include the job URL for the first failure
                    "job_url": f"{concourse_prefix}{job_id}",
                    "url": url,
                }
            )
            tested_books.append(book)
            print(">>> HTTPError: {}".format(h_e.code) + ", " + url)

        else:
            # Return code 200, ...
            successful_books.append(url)

            book_jsons = req_url.read()
            jsons = json.loads(book_jsons)
            book_title = jsons.get("title")

            print(f"Verifying collection {book_title} : {url}")

            xhtml_data = requests.get(url.replace(".json", ".xhtml")).content
            doc = etree.fromstring(xhtml_data)

            links = []

            for node in doc.xpath(
                '//x:a[@href and starts-with(@href, "./")]',
                namespaces={"x": "http://www.w3.org/1999/xhtml"},
            ):
                links.append(node.attrib["href"])

            # verifies every 5th page url of each book
            for link in links[::5]:
                links_replaced = link.replace("./", f"{s3_archive_folder}").replace(
                    ".xhtml", ".json"
                )

                s3_pages_request = urllib.request.urlopen(links_replaced)

                s3_pages = s3_pages_request.read()
                s3_pages_jdata = json.loads(s3_pages)

                assert s3_pages_jdata["title"]
                assert s3_pages_jdata["content"]
                assert "<body>" and "</body>" in s3_pages_jdata["content"]

                assert s3_pages_request.getcode() == 200

            book.update(
                {
                    "status": "SUCCESS",
                    # We'll assume this was the successful job URL, but it may be
                    # the book failed in this job and succeeded in a subsequent
                    # retry job. This is just for simplicity since we probably
                    # don't care much about successful job details but can be
                    # better addressed in the future if needed.
                    "job_url": f"{concourse_prefix}{job_id}",
                    "url": url,
                }
            )
            tested_books.append(book)

    # Write the report CSV (into the root folder of the repo)
    with open("report.csv", "w") as csvfile:
        fieldnames = tested_books[0].keys()

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(tested_books)
