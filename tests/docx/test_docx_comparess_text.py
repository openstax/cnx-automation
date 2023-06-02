import os
from docx import Document

from deepdiff import DeepDiff

import pytest


"""
Compares docx files of 2 versions of the same book - checking text
Updated: May 31, 2023
"""


def test_docx_comparess_text():
    old_dir = f"{os.getcwd()}/docxs_old/astronomy-2e"
    new_dir = f"{os.getcwd()}/docxs_new/astronomy-2e"

    dict_old = {}
    dict_new = {}

    for ofile in os.listdir(old_dir):
        f = os.path.join(old_dir, ofile)
        if os.path.isfile(f):
            doc = Document(f)
            for docpara in doc.paragraphs:
                dict_old.setdefault(docpara.text, ofile)

    for nfile in os.listdir(new_dir):
        f = os.path.join(new_dir, nfile)
        if os.path.isfile(f):
            doc = Document(f)
            for docpara in doc.paragraphs:
                dict_new.setdefault(docpara.text, nfile)

    if not DeepDiff(dict_old, dict_new):
        print(">>> NO DIFFERENCES <<<")
    else:
        print(f"FOUND DIFFERENCES:\n{DeepDiff(dict_old, dict_new).pretty()} ----->>>>")
        pytest.fail(f"DIFFS: {DeepDiff(dict_old, dict_new).pretty()}")
