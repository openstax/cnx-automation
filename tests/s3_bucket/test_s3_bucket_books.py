import json

import urllib
from urllib.request import urlopen

from urllib.error import HTTPError

from lxml import etree
import requests

import os
import boto3

"""
Verifies collections in the s3 bucket folder
Latest update on Oct. 26th, 2020
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


def test_s3_bucket_books(s3_base_url, code_tag, s3_queue_state_bucket_books):

    # path to the aws s3 bucket folder
    s3_archive_folder = f"/apps/archive/{code_tag}/contents/"

    # reading nested lists and getting slug names
    json_data = json.loads(s3_queue_state_bucket_books)
    json_data = json_data[::-1]

    uuid_list = []
    version_list = []
    for key in json_data:
        if key["uuid"]:
            uuid_list.append(key["uuid"])
        if key["version"]:
            version_list.append(key["version"])

    for i in range(0, len(version_list)):
        version_list[i] = version_list[i][2:]

    approved_books_full_url = [
        f"{s3_base_url}{s3_archive_folder}{i}@{j}.json" for i, j in zip(uuid_list, version_list)
    ]

    successful_books = []
    unsuccessful_books = []

    for url in approved_books_full_url:
        try:
            urllib.request.urlopen(url)
        except HTTPError as h_e:
            # Return code 404, 501, ...
            print("HTTPError (check concourse jobs): {}".format(h_e.code) + ", " + url)
            unsuccessful_books.append(url)

        else:
            successful_books.append(url.replace(".json", ".xhtml"))

    # list of approved book urls without http errors (unsuccessful concourse jobs)
    for book in successful_books:

        print("Verifying pages of collection ", book)

        xhtml_data = requests.get(book).content
        doc = etree.fromstring(xhtml_data)

        links = []
        for node in doc.xpath(
            '//x:a[@href and starts-with(@href, "./")]',
            namespaces={"x": "http://www.w3.org/1999/xhtml"},
        ):
            links.append(node.attrib["href"])

        # verifies every 10th page url in each book
        for link in links[::10]:

            links_replaced = link.replace("./", f"{s3_base_url}{s3_archive_folder}").replace(
                ".xhtml", ".json"
            )

            res = requests.get(links_replaced)

            s3_pages = urllib.request.urlopen(links_replaced).read()
            s3_pages_jdata = json.loads(s3_pages)
            s3_page_title = s3_pages_jdata.get("title")
            s3_page_content = s3_pages_jdata.get("content")

            assert s3_page_title != ""
            assert s3_page_content != ""

            assert res.status_code == 200
