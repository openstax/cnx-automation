import os

import shutil

import zipfile

from deepdiff import DeepDiff

import pytest

from collections import OrderedDict

import docx2txt

"""
Compares docx files. To run:
1. run two docx jobs in corgi
2. download the docx zip files from corgi (by default to Downloads folder on Mac)
3. make sure that base_to_dir and base_from_dir variables are set correctly
- required folder structure is: root folder docx_old_new and its two subfolders 0 and 1
4. run 'pytest -k test_unzip_and_compare_docxs.py tests/docx > diffs_report.txt'

Latest update on July 21st, 2023
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

    subs = []

    for j in unzip_dirs:
        os.chdir(j)

        # Unzips the files
        for file in os.listdir(j):
            if zipfile.is_zipfile(file):
                with zipfile.ZipFile(file) as item:
                    item.extractall()

        subs.append(os.listdir(j))

    for sub in subs[0]:
        old_dir.append(f"{unzip_dirs[0]}/{sub}")

    old_dir_am = [val for val in old_dir if not val.endswith(".zip")]

    for sub in subs[1]:
        new_dir.append(f"{unzip_dirs[1]}/{sub}")

    new_dir_am = [val for val in new_dir if not val.endswith(".zip")]

    # Part 2: Compares text of all docx files

    dict_old = {}
    dict_new = {}

    for old in list(OrderedDict.fromkeys(old_dir_am)):
        old_books = old.split("/0")[1].lstrip().split(" ")[0]
        dict_old[old_books] = {}
        for ofile in os.listdir(old):
            f = os.path.join(old, ofile)
            if os.path.isfile(f):
                odoc = docx2txt.process(f)
                dict_old[old_books][ofile] = odoc

    for new in list(OrderedDict.fromkeys(new_dir_am)):
        new_books = new.split("/1")[1].lstrip().split(" ")[0]
        dict_new[new_books] = {}
        for nfile in os.listdir(new):
            f = os.path.join(new, nfile)
            if os.path.isfile(f):
                ndoc = docx2txt.process(f)
                dict_new[new_books][nfile] = ndoc

    if not DeepDiff(dict_new.values(), dict_old.values()):
        print("------>>>>> NO DIFFERENCES <<<<<------")
    else:
        ddiffs = DeepDiff(dict_new, dict_old, verbose_level=2).pretty()

        print(f"FOUND DIFFERENCES:\n{ddiffs}")
