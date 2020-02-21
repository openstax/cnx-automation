import json
import urllib
from urllib.request import urlopen
from urllib.error import HTTPError

from time import sleep

cops_api_url = "http://localhost/api/jobs/"


def test_api_results(selenium):

    # GIVEN an archive URL for a book
    api_url = f"{cops_api_url}"

    try:

        api_page = urllib.request.urlopen(api_url).read()
        api_jdata = json.loads(api_page)

        newest0 = api_jdata[0]
        newest1 = api_jdata[1]

        job_status0 = newest0["status"]["name"]
        job_status1 = newest1["status"]["name"]

    except HTTPError as err:
        if err.code:
            print("Cannot reach url")
        else:
            raise

    else:
        sleep(2)

        assert job_status0 == "queued" or job_status0 == "assigned" or job_status0 == "processing"
        assert job_status1 == "queued" or job_status1 == "assigned" or job_status0 == "processing"
