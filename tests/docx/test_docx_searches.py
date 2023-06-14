import os
import re

from docx import Document

import shutil

import pytest

import zipfile

"""
Searches through docx files for string(s) of interest. To run the search:
1. run a docx job(s) in corgi
2. download the zip file(s) via corgi (by default to Downloads folder on Mac)
3. make sure that base_to_dir, base_from_dir and patt_list variables are set correctly
4. run 'pytest -k test_docx_searches.py tests/docx'

Latest update on June 14th, 2023
"""


def test_docx_searches():
    base_to_dir = "/Users/om9/Documents/Projects/cnx-automation/docx_search"
    base_from_dir = "/Users/om9/downloads/"

    patt_list = ["\\\\sqrt", "{{", "\\\\pi", "\\\\frac", "\\\\text"]

    all_files = os.listdir(base_from_dir)
    unwanted = (".DS_Store", "coll-book-")
    files = [x for x in all_files if not x.startswith(unwanted)]

    unzip_dirs = []

    if len(files) > 0:
        for i in range(len(files)):
            if ".zip" not in files[i]:
                pytest.exit(f"No zip file available: {files[i]}")
            else:
                file = os.path.join(base_from_dir, files[i])
                tof = os.path.join(base_to_dir, files[i])

                shutil.copy(file, tof)

                unzip_dirs.append(tof.split("/openstax", 1)[0])

    else:
        pytest.fail(f"No zip files: {len(files)} file available")

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

    for i in os.listdir(unzip_dirs[0]):
        directory = f"{base_to_dir}/{i}"

        for filename in os.listdir(directory):
            all_text = []
            f = os.path.join(directory, filename)
            if os.path.isfile(f):
                doc = Document(f)
                for docpara in doc.paragraphs:
                    all_text.append(docpara.text)

                for patt in patt_list:
                    new_list = [x for x in all_text if re.search(patt, x)]
                    for item in new_list:
                        print(f"\nSEARCH RESULT: {item} --- in --->>> {f}")
