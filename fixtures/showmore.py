from dotenv import load_dotenv
import os
import pytest
import urllib.request
from ast import literal_eval

load_dotenv(verbose = True)

mpath_more = os.environ['MPATH_MORE']

@pytest.fixture(scope="session")
def shmore_xpath_ids(request):
    """Returns Show More xpath elements"""

    with open(mpath_more, "r") as mofile:
        moreIDs = mofile.readlines()

    if not moreIDs:
        raise Exception("show more xpath element IDs are missing")
    else:
        yield moreIDs

