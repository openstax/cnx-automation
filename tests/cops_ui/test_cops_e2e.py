import requests
from tests import markers
from selenium.webdriver.common.keys import Keys

import pytest

import json
import urllib
from urllib.request import urlopen

from urllib.error import HTTPError, URLError
from requests.exceptions import ConnectionError

from time import sleep
import time


"""
End to end test of cops(-staging).openstax.org
Creates jobs for 2 collections, verifies that they were successfully executed and pdf is created
Latest update on 08/03/2020
"""


@markers.parametrize(
    "colid, ver, style, bserver",
    [("col11992", "latest", "astronomy", "qa"), ("col11496", "1.17", "anatomy", "staging")],
)
def test_cops_ui(
    selenium, cops_base_url, job_dialog_button, create_button, colid, ver, style, bserver
):

    # GIVEN a cops base URL
    # WHEN making a request to cops

    try:

        # verifying that cops URL is active
        response = requests.get(cops_base_url)

    except HTTPError:
        pytest.exit("<<<<<<<<<< HTTP Error: COPS URL IS INVALID OR UNREACHABLE >>>>>>>>>>")
    except URLError:
        pytest.exit("<<<<<<<<<< URL Error: COPS URL IS INVALID OR UNREACHABLE >>>>>>>>>>")
    except ConnectionError:
        pytest.exit("<<<<<<<<<< Connection Error: COPS URL IS INVALID OR UNREACHABLE >>>>>>>>>>")

    else:

        # opening 'CREATE A NEW PDF JOB' dialog
        selenium.get(cops_base_url)
        new_pdf = selenium.find_element_by_xpath(job_dialog_button)
        new_pdf.click()

        # tabbing through fields and inputting colID, style and server
        selenium.find_element_by_tag_name("body").send_keys(Keys.TAB, colid)
        selenium.find_element_by_tag_name("body").send_keys(Keys.TAB, ver)
        selenium.find_element_by_tag_name("body").send_keys(Keys.TAB, style)
        selenium.find_element_by_tag_name("body").send_keys(Keys.TAB, bserver)

        # clicking 'CREATE' button to start the jobs
        create_button_xp = selenium.find_element_by_xpath(create_button)
        create_button_xp.click()
        create_button_xp.click()

        # THEN we should get successful connection
        assert response.status_code == 200


def test_job_results(selenium, cops_base_url, cops_api_url):

    start_time = time.time()
    # 25 minutes wait time before process times out
    wait_time = 1500

    while True:

        api_page = urllib.request.urlopen(cops_api_url).read()

        # loading cops json file and extracting required data
        api_jdata = json.loads(api_page)

        newest0 = api_jdata[0]
        newest1 = api_jdata[1]

        job_id0 = newest0["id"]
        job_id1 = newest1["id"]

        collection_id0 = newest0["collection_id"]
        pdf_url0 = newest0["pdf_url"]
        job_status0 = newest0["status"]["name"]

        collection_id1 = newest1["collection_id"]
        pdf_url1 = newest1["pdf_url"]
        job_status1 = newest1["status"]["name"]

        if job_status0 != "completed" and job_status1 != "completed":

            if time.time() > start_time + wait_time:
                print("!!!!! SOMETHING WENT WRONG. PROCESS TIMED OUT AFTER 25 MINUTES !!!!!")
                break

            # printing messages while waiting for appropriate jobs to be completed
            print(f"JOBS {job_id0} AND {job_id1} NOT COMPLETED YET, WAITING...")

            # waiting for the cops jobs to complete
            sleep(20)
            continue

        elif job_status0 == "completed" and job_status1 == "completed":

            assert collection_id0 == "col11496"
            assert collection_id0 in pdf_url0
            assert job_status0 == "completed"

            assert collection_id1 == "col11992"
            assert collection_id1 in pdf_url1
            assert job_status1 == "completed"

            print(f"\nJOBS {job_id0} AND {job_id1} COMPLETED SUCCESSFULLY")
            break

        elif job_status0 == "failed" or job_status1 == "failed":
            if job_status0 == "failed":
                print(f"\nJOB {job_id0} FAILED")
            else:
                print(f"\nJOB {job_id1} FAILED")
            break

        else:
            continue
