import os

import zipfile

import pytest


"""
Compares docx files of 2 versions of the same book - checking images
Updated: May 31, 2023
"""


def test_docx_comparess_images():
    old_dir = f"{os.getcwd()}/docxs_old/astronomy-2e"
    new_dir = f"{os.getcwd()}/docxs_new/astronomy-2e"

    old_images = []
    new_images = []

    for ofile in os.listdir(old_dir):
        f = os.path.join(old_dir, ofile)
        if os.path.isfile(f):
            z = zipfile.ZipFile(f)
            all_files = z.namelist()

            old_images.append(list(filter(lambda x: x.startswith("word/media/"), all_files)))

    for nfile in os.listdir(new_dir):
        f = os.path.join(new_dir, nfile)
        if os.path.isfile(f):
            z = zipfile.ZipFile(f)

            all_files = z.namelist()

            new_images.append(list(filter(lambda x: x.startswith("word/media/"), all_files)))

    flat_old_images = [item for sublist in old_images for item in sublist]
    flat_new_images = [item for sublist in new_images for item in sublist]

    try:
        assert flat_old_images == flat_new_images
    except AssertionError as asserr:
        pytest.fail(f"DIFFS FOUND IN IMAGES: {asserr}")
    else:
        print(">>> NO DIFFERENCES <<<")
