import json

import urllib
from urllib.request import urlopen

from urllib.error import HTTPError

from lxml import etree
import requests

import os
import boto3

"""
Verifies pages of collections in the aws s3 bucket folder
Latest update on Oct. 28th, 2020
"""


def test_gitstor_books():

    repo = "osbook-university-physics"
    collection = "university-physics-volume-1.collection.xml"

    token = "mytoken"

    # os.environ["AWS_ACCESS_KEY_ID"] = github_token

    headers = {"Authorization": "token " + token}
    endpoint = (
        f"https://raw.githubusercontent.com/openstax/{repo}/tree/main/collections/{collection}"
    )
    resp = requests.get(endpoint, headers=headers)

    assert resp
