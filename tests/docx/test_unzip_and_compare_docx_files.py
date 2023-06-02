import os

import shutil

import zipfile

from docx import Document

from deepdiff import DeepDiff

import pytest


def test_unzip_and_compare_docx_files():
    # Part 1: below code copies the docx zip files and unzips them into two different folders

    base_to_dir = "/Users/om9/Documents/Projects/cnx-automation/docx_old_new"
    base_from_dir = "/Users/om9/downloads/"

    all_files = os.listdir(base_from_dir)
    unwanted = (".DS_Store", "coll-book-")
    files = [x for x in all_files if not x.startswith(unwanted)]

    old_dir = []
    new_dir = []

    for i in range(len(files)):
        file = os.path.join(base_from_dir, files[i])

        tof = os.path.join(base_from_dir, f"{base_to_dir}/%d" % i, files[i])
        shutil.copy(file, tof)

    working_directory = [f"{base_to_dir}/0", f"{base_to_dir}/1"]

    for j in working_directory:
        os.chdir(j)

        for file in os.listdir(j):
            if zipfile.is_zipfile(file):
                with zipfile.ZipFile(file) as item:
                    item.extractall()

        for fname in os.listdir(j):
            if fname.endswith(".zip"):
                os.remove(os.path.join(j, fname))

        m = os.listdir(j)
        old_dir.append(f"{base_to_dir}/0/{m[0]}")
        new_dir.append(f"{base_to_dir}/1/{m[0]}")

    # Part 2: below code compares text of all docx files

    dict_old = {}
    dict_new = {}

    for ofile in os.listdir(old_dir[0]):
        f = os.path.join(old_dir[0], ofile)
        if os.path.isfile(f):
            doc = Document(f)
            for docpara in doc.paragraphs:
                dict_old.setdefault(docpara.text, ofile)

    for nfile in os.listdir(new_dir[0]):
        f = os.path.join(new_dir[0], nfile)
        if os.path.isfile(f):
            doc = Document(f)
            for docpara in doc.paragraphs:
                dict_new.setdefault(docpara.text, nfile)

    if not DeepDiff(dict_old, dict_new):
        print(">>> NO DIFFERENCES <<<")
    else:
        print(f"FOUND DIFFERENCES:\n{DeepDiff(dict_old, dict_new).pretty()} ----->>>>")
        pytest.fail(f"DIFFS: {DeepDiff(dict_old, dict_new).pretty()}")
