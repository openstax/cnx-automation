import os

import shutil

import zipfile

from docx import Document

from deepdiff import DeepDiff

import pytest

from collections import OrderedDict

"""
Compares docx files. To run:
1. run two docx jobs in corgi
2. download the docx zip files from corgi (by default to Downloads folder on Mac)
3. make sure that base_to_dir and base_from_dir variables are set correctly
4. run 'pytest -k test_unzip_and_compare_docxs.py tests/docx'

Latest update on June 23rd, 2023
"""


def test_unzip_and_compare_docxs():
    # Part 1: Copies docx zip files and unzips them into two different folders
    home_dir = os.path.expanduser("~")

    base_to_dir = f"{os.getcwd()}/docx_old_new"
    base_from_dir = f"{home_dir}/downloads/"

    all_files = os.listdir(base_from_dir)
    docx_zips_only = [x for x in all_files if "zip" and "docx" in x]

    old_dir = []
    new_dir = []

    unzip_dirs = []

    for i in range(len(docx_zips_only)):
        if len(docx_zips_only) == 2:
            file = os.path.join(base_from_dir, docx_zips_only[i])
            tof = os.path.join(f"{base_to_dir}/%d" % i, docx_zips_only[i])
            shutil.copy(file, tof)

            unzip_dirs.append(f"{base_to_dir}/%d" % i)

        else:
            pytest.fail(f"Two zip files required: {len(docx_zips_only)} file(s) available")

    for j in unzip_dirs:
        os.chdir(j)

        # Unzips the files
        for file in os.listdir(j):
            if zipfile.is_zipfile(file):
                with zipfile.ZipFile(file) as item:
                    item.extractall()

        subs_dirs = os.listdir(j)

        for sub in subs_dirs:
            old_dir.append(f"{unzip_dirs[0]}/{sub}")
            new_dir.append(f"{unzip_dirs[1]}/{sub}")

    old_dir_am = [val for val in old_dir if not val.endswith(".zip")]
    new_dir_am = [val for val in new_dir if not val.endswith(".zip")]

    # Part 2: Compares text of all docx files

    dict_old = {}
    dict_new = {}

    for old in list(OrderedDict.fromkeys(old_dir_am)):
        for ofile in os.listdir(old):
            f = os.path.join(old_dir_am[1], ofile)
            if os.path.isfile(f):
                doc = Document(f)
                for docpara in doc.paragraphs:
                    dict_old.setdefault(docpara.text, ofile)

    for new in list(OrderedDict.fromkeys(new_dir_am)):
        for nfile in os.listdir(new):
            f = os.path.join(new_dir_am[1], nfile)
            if os.path.isfile(f):
                doc = Document(f)
                for docpara in doc.paragraphs:
                    dict_new.setdefault(docpara.text, nfile)

    if not DeepDiff(dict_old, dict_new):
        print("------>>>>> NO DIFFERENCES <<<<<------")
    else:
        ddiffs = DeepDiff(dict_old, dict_new, verbose_level=2).pretty()
        print(f"FOUND DIFFERENCES:\n{ddiffs}")
