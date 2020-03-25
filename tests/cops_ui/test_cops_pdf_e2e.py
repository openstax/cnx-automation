import requests
from tests import markers
from selenium.webdriver.common.keys import Keys

import pytest

import json
import urllib
from urllib.request import urlopen

from urllib.error import HTTPError, URLError
from requests.exceptions import ConnectionError

import time

from time import sleep
from tkinter import Tk, Button

import PyPDF2
import os

"""
End to end test of cops(-staging).openstax.org
Creates jobs for 2 collections, verifies that they were successfully executed and pdf is created with content
Latest update on 25/03/2020
"""


@markers.parametrize(
    "colid, ver, style, bserver",
    [("col11992", "latest", "astronomy", "qa"), ("col11496", "1.17", "anatomy", "staging")],
)
def test_create_cops_jobs(
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


def test_verify_cops_jobs(selenium, cops_api_url):

    # 20 minutes wait time before process times out
    start_time = time.time()
    wait_time = 1200

    while True:

        if time.time() > start_time + wait_time:
            pytest.exit(
                "!!!!! ONE OF THE TWO JOBS FAILED. PROCESS TIMED OUT AFTER 20 MINUTES !!!!!"
            )

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

        for i, j in [(job_status0, job_status1)]:

            if i == "completed" and j == "completed":
                assert collection_id0 == "col11496"
                assert collection_id0 in pdf_url0
                assert job_status0 == "completed"

                assert collection_id1 == "col11992"
                assert collection_id1 in pdf_url1
                assert job_status1 == "completed"

                print(f"\nCOPS JOBS '{job_id0}' {job_status0} AND '{job_id1}' {job_status1}")
                break

            elif (i == "failed" and j == "completed") or (i == "completed" and j == "failed"):
                pytest.exit(f"\nJOB '{job_id0}' {job_status0} AND '{job_id1}' {job_status1}")

            elif i == "failed" and j == "failed":
                pytest.exit(f"\nJOB '{job_id0}' {job_status0} AND '{job_id1}' {job_status1}")

        else:
            continue

        pytest.exit(
            f"\nSOMETHING WENT WRONG: '{job_id0}' {job_status0} AND '{job_id1}' {job_status1}"
        )


def test_verify_cops_pdf(selenium, cops_base_url, cops_api_url):

    api_page = urllib.request.urlopen(cops_api_url).read()
    api_jdata = json.loads(api_page)
    newest0 = api_jdata[0]
    pdf_url0 = newest0["pdf_url"]

    if pdf_url0 is None:
        pytest.exit(">>>> PDF LINK IS MISSING <<<<")

    else:
        root = Tk()

        selenium.get(cops_base_url)

        btn = Button(root, text="cops page", command=test_verify_cops_pdf)
        btn.pack()

        elem = selenium.find_element_by_tag_name("a")
        elem.click()

        selenium.switch_to.window(selenium.window_handles[1])

        current_url = selenium.current_url
        url_pdf = current_url

        urllib.request.urlretrieve(url_pdf, r"collection_pdf_document.pdf")

        sleep(2)

        pdf_file = open("collection_pdf_document.pdf", "rb")
        read_pdf = PyPDF2.PdfFileReader(pdf_file)
        number_of_pages = read_pdf.getNumPages()

        pdf_page = read_pdf.getPage(0)
        pdf_page_content = pdf_page.extractText()

        if os.path.exists("collection_pdf_document.pdf"):
            os.remove("collection_pdf_document.pdf")

        assert number_of_pages > 0
        assert "CHAPTER" in pdf_page_content

        root.destroy()
        root.mainloop()
