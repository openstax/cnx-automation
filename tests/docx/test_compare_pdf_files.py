import os

import shutil

from diff_pdf_visually import pdf_similar

import pytest

"""
Compares two pdf files. To run:
1. run two pdf jobs in corgi
2. download the pdf files from corgi (by default to Downloads folder on Mac)
3. make sure that base_to_dir and base_from_dir variables are set correctly
4. run 'pytest -k test_compare_pdf_files.py tests/docx'

Latest update on June 15th, 2023
"""


def test_compare_pdf_files():
    # Part 1: Copies pdf files into a folder

    base_to_dir = "./pdf_files"

    home_dir = os.path.expanduser("~")
    base_from_dir = f"{home_dir}/downloads/"

    shutil.copytree(base_from_dir, base_to_dir, dirs_exist_ok=True)

    all_files = os.listdir(base_to_dir)
    pdfs_only = [x for x in all_files if x.endswith(".pdf")]

    pdf_files_paths = []

    if len(pdfs_only) == 2:
        for i in range(len(pdfs_only)):
            file = os.path.join(base_from_dir, pdfs_only[i])
            tof = os.path.join(base_to_dir, pdfs_only[i])
            shutil.copy(file, tof)

            pdf_files_paths.append(tof)

    else:
        pytest.fail(f"Two pdf files required: {len(pdfs_only)} file(s) available")

    # Part 2: Compares pdf files

    try:
        assert pdf_similar(pdf_files_paths[0], pdf_files_paths[1])

    except AssertionError:
        pytest.exit("PDFS ARE NOT THE SAME")

    else:
        print("\n\n=========>>> PDFS APPEAR TO BE THE SAME")
