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

Latest update on June 21st, 2023
"""


def test_compare_pdf_files():
    # Part 1: Copies pdf files into predefined folder

    base_to_dir = "./pdf_files"

    home_dir = os.path.expanduser("~")
    base_from_dir = f"{home_dir}/downloads/"

    pdf_files_paths = []

    for afile in os.listdir(base_from_dir):
        if afile.endswith(".pdf") and "-git-" in afile:
            from_dir = os.path.join(base_from_dir, afile)
            to_dir = os.path.join(base_to_dir, afile)

            shutil.copy(from_dir, to_dir)

            pdf_files_paths.append(to_dir)

    # Part 2: Compares pdf files

    if len(pdf_files_paths) == 2:
        try:
            assert pdf_similar(pdf_files_paths[0], pdf_files_paths[1])

        except AssertionError:
            pytest.exit("PDFS ARE NOT THE SAME")

        else:
            print("\n\n=========>>> PDFS APPEAR TO BE THE SAME")

    else:
        pytest.fail(f"Two pdf files required: {len(pdf_files_paths)} file(s) available")
