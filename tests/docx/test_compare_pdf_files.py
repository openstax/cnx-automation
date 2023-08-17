import os

import shutil

from diff_pdf_visually import pdf_similar

import pytest

import tempfile

"""
Compares two pdf files. To run:
1. run two pdf jobs in corgi
2. download the pdf files from corgi (by default to Downloads folder on Mac)
3. make sure that base_from_dir variable is set correctly
4. base_to_dir is a temp folder and is auto-deleted after each test run
5. run 'pytest -k test_compare_pdf_files.py tests/docx'
6. to get a log file of differences, run 'pytest -k test_compare_pdf_files.py tests/docx | tee docx_diffs.txt'

Latest update on June 23rd, 2023
"""


def test_compare_pdf_files():
    # Part 1: Copies pdf files into temp folder
    with tempfile.TemporaryDirectory() as tmp_dir:
        base_to_dir = tmp_dir

        home_dir = os.path.expanduser("~")
        base_from_dir = f"{home_dir}/downloads/"

        pdf_files_paths = []

        for afile in os.listdir(base_from_dir):
            if afile.startswith("openstax-osbooks-") and afile.endswith(".pdf"):
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
