import os
from docx import Document
import re

"""
Searches through docx files for predefined strings
To run the search:
1. run a docx job in corgi
2. download the zip file and unzip it
3. copy the collection folder to the folder predefined in the 'directory' variable below
4. change the 'directory' variable accordingly
5. run 'pytest -k test_docx_search.py tests/docx'
Latest update on May 15th, 2023
"""


def test_docx_searches():
    directory = "tests/docx/docxss/física-universitaria-volumen-3"

    patt_list = ["\\\\sqrt", "{{", "\\\\pi", "\\\\frac", "\\\\text"]

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
