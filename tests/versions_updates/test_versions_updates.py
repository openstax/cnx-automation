import urllib
from urllib.request import urlopen

import deepdiff
import json

import pytest


"""
Compares version.txt and python-version.txt files on qa or staging against production env
Updated: 17/12/2020
"""


@pytest.mark.xfail(reason=" >>>>> Attention! No versions changed in current deploy <<<<< ")
def test_versions_updates(webview_base_url):

    # Extracts versions from python-version.txt

    url_versions_staging_qa = f"{webview_base_url}/python-version.txt"
    url_versions_production = "https://cnx.org/python-version.txt"

    staging_qa_vers = urllib.request.urlopen(url_versions_staging_qa)

    # Removes comment lines and splits elements in qa(staging).cnx.org/python-version.txt
    verlist = []
    for line in staging_qa_vers:
        if not line.startswith(b"#" or b"##"):
            verlist.append(line.strip().decode("utf-8").split("=="))

    # Removes empty elements and flattens the list
    vlc_mod = [ele for ele in verlist if ele != [""]]
    vlc_flat_list = [item for sublist in vlc_mod for item in sublist]

    # Creates dictionary from the list above
    vlc_dict = {vlc_flat_list[i]: vlc_flat_list[i + 1] for i in range(0, len(vlc_flat_list), 2)}

    production_vers = urllib.request.urlopen(url_versions_production)

    # Removes comment lines and splits elements in cnx.org/python-version.txt
    prod_verlist = []
    for line in production_vers:
        if not line.startswith(b"#" or b"##"):
            prod_verlist.append(line.strip().decode("utf-8").split("=="))

    # Removes empty elements and flattens the list
    pvlc_mod = [ele for ele in prod_verlist if ele != [""]]
    pvlc_flat_list = [item for sublist in pvlc_mod for item in sublist]

    # Creates dictionary from the list above
    pvlc_dict = {pvlc_flat_list[i]: pvlc_flat_list[i + 1] for i in range(0, len(pvlc_flat_list), 2)}

    # Compares both dictionaries and prints the changed values
    vers_diff = deepdiff.DeepDiff(pvlc_dict, vlc_dict)

    # Creates a more readable output containing modules with changed versions only
    vers_diff_flat = {}

    for key, val in vers_diff.items():
        if type(val) == dict:
            vers_diff_flat[key] = len(vers_diff.keys())
            vers_diff_flat.update(val)
        else:
            vers_diff_flat[key] = val

    v_items = [(k, v) for k, v in vers_diff_flat.items()]
    print("\n", *v_items[1:], sep="\n")

    assert not vers_diff


@pytest.mark.xfail(reason=" >>>>> Attention! No versions changed in current deploy <<<<< ")
def test_webview_versions_updates(webview_base_url):

    # Extracts versions from version.txt

    url_history_staging_qa = f"{webview_base_url}/version.txt"
    url_history_production = "https://cnx.org/version.txt"

    # Loads dictionary from version.txt of qa(staging).cnx.org
    staging_qa_vers = urllib.request.urlopen(url_history_staging_qa).read()
    staging_qa_jsons = json.loads(staging_qa_vers)

    # Loads dictionary from version.txt of cnx.org
    prod_vers = urllib.request.urlopen(url_history_production).read()
    prod_jsons = json.loads(prod_vers)

    # Compares both dictionaries and prints the changed values
    vers_diff = deepdiff.DeepDiff(prod_jsons, staging_qa_jsons)

    # Creates a more readable output containing modules with changed versions only
    vers_diff_flat = {}

    for key, val in vers_diff.items():
        if type(val) == dict:
            vers_diff_flat[key] = len(vers_diff.keys())
            vers_diff_flat.update(val)
        else:
            vers_diff_flat[key] = val

    v_items = [(k, v) for k, v in vers_diff_flat.items()]
    print("\n", *v_items[1:], sep="\n")

    assert not vers_diff
