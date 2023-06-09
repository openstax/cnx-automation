import os

import shutil

import zipfile

from docx import Document

from deepdiff import DeepDiff

import pytest


def test_unzip_and_compare_docxs():
    # Part 0: Run two corgi docx jobs for the same collection, one for the latest version, one for a previous version
    # and download the docx zip files

    # Part 1: Copies docx zip files and unzips them into two different folders

    base_to_dir = "/Users/om9/Documents/Projects/cnx-automation/docx_old_new"
    base_from_dir = "/Users/om9/downloads/"

    all_files = os.listdir(base_from_dir)
    unwanted = (".DS_Store", "coll-book-")
    files = [x for x in all_files if not x.startswith(unwanted)]

    old_dir = []
    new_dir = []

    unzip_dirs = []

    if len(files) == 2:
        for i in range(len(files)):
            if ".zip" not in files[i]:
                pytest.exit(f"No zip file available: {files[i]}")
            else:
                file = os.path.join(base_from_dir, files[i])
                tof = os.path.join(base_from_dir, f"{base_to_dir}/%d" % i, files[i])
                shutil.copy(file, tof)

                unzip_dirs.append(tof.split("/openstax", 1)[0])
    else:
        pytest.fail(f"Two zip files required: {len(files)} file available")

    for j in unzip_dirs:
        os.chdir(j)

        # Unzips the zip files
        for file in os.listdir(j):
            if zipfile.is_zipfile(file):
                with zipfile.ZipFile(file) as item:
                    item.extractall()

        # Deletes the zip files after unzip
        for fname in os.listdir(j):
            if fname.endswith(".zip"):
                os.remove(os.path.join(j, fname))

        m = os.listdir(j)

        old_dir.append(f"{unzip_dirs[0]}/{m[0]}")
        new_dir.append(f"{unzip_dirs[1]}/{m[0]}")

    # Part 2: Compares text of all docx files

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
        print("------>>>>> NO DIFFERENCES <<<<<------")
    else:
        ddiffs = DeepDiff(dict_old, dict_new, verbose_level=2).pretty()
        print(f"FOUND DIFFERENCES:\n{ddiffs}")

    # Deletes everything in the directory 0
    dir_0 = os.listdir(f"{unzip_dirs[0]}/")
    shutil.rmtree(f"{unzip_dirs[0]}/{dir_0[0]}")

    # Deletes everything in the directory 1
    dir_1 = os.listdir(f"{unzip_dirs[1]}/")
    shutil.rmtree(f"{unzip_dirs[1]}/{dir_1[0]}")
