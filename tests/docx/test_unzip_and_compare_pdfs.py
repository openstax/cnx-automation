import os

import shutil

from diff_pdf_visually import pdf_similar

import pytest

"""
Compares two pdf files. To run:
1. run two pdf jobs in corgi
2. download the pdf files from corgi (by default to Downloads folder on Mac)
3. make sure that base_to_dir and base_from_dir variables are set correctly
4. run 'pytest -k test_unzip_and_compare_pdfs.py tests/docx'

Latest update on June 14th, 2023
"""


def test_unzip_and_compare_pdfs():
    # Part 1: Copies pdf files into two different folders

    base_to_dir = "/Users/om9/Documents/Projects/cnx-automation/pdf_old_new"
    base_from_dir = "/Users/om9/downloads/"

    all_files = os.listdir(base_from_dir)
    unwanted = (".DS_Store", "coll-book-")
    files = [x for x in all_files if not x.startswith(unwanted)]

    paths = []

    if len(files) == 2:
        for i in range(len(files)):
            if ".pdf" not in files[i]:
                pytest.exit(f"No pdf file available: {files[i]}")
            else:
                file = os.path.join(base_from_dir, files[i])
                tof = os.path.join(f"{base_to_dir}/%d" % i, files[i])
                shutil.copy(file, tof)

                paths.append(tof)

    else:
        pytest.fail(f"Two pdf files required: {len(files)} file available")

    # Part 2: Compares pdf files

    try:
        assert pdf_similar(paths[0], paths[1])

    except AssertionError:
        pytest.exit("PDFS ARE NOT THE SAME")

    else:
        print("\n\n=========>>> PDFS APPEAR TO BE THE SAME")
