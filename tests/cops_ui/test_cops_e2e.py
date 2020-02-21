import requests
from tests import markers
from selenium.webdriver.common.keys import Keys

import json
import urllib
from urllib.request import urlopen

# from urllib.error import HTTPError

from time import sleep


cops_api_url = "http://localhost/api/jobs/"
cops_base_url = "http://localhost"

new_pdf_xp = (
    '// *[ @ id = "app"] / div[1] / main / div / div / div / div / div[1] / button / span / span'
)
create_xp = '//*[@id="app"]/div[3]/div/div/div[3]/button[2]/span'


@markers.parametrize(
    "colid, style, bserver", [("col11992", "astronomy", "qa"), ("col11496", "anatomy", "staging")]
)
def test_cops_ui(selenium, colid, style, bserver):

    # GIVEN an archive URL for a book
    url = f"{cops_base_url}"

    # WHEN making a request to Archive
    response = requests.get(url)

    selenium.get(url)
    new_pdf = selenium.find_element_by_xpath(new_pdf_xp)
    new_pdf.click()

    selenium.find_element_by_tag_name("body").send_keys(Keys.TAB, colid)
    selenium.find_element_by_tag_name("body").send_keys(Keys.TAB)
    selenium.find_element_by_tag_name("body").send_keys(Keys.TAB, style)
    selenium.find_element_by_tag_name("body").send_keys(Keys.TAB, bserver)

    create_button_xp = selenium.find_element_by_xpath(create_xp)
    create_button_xp.click()
    create_button_xp.click()

    # THEN we should NOT redirect to REX
    assert response.status_code == 200


def test_api_results(selenium):

    # GIVEN an archive URL for a book
    api_url = f"{cops_api_url}"

    while True:

        sleep(5)

        api_page = urllib.request.urlopen(api_url).read()
        api_jdata = json.loads(api_page)

        newest0 = api_jdata[0]
        newest1 = api_jdata[1]
        # newest2 = api_jdata[2]

        job_id0 = newest0["id"]
        job_id1 = newest1["id"]
        # job_id2 = newest2["id"]

        if job_id0 > job_id1:

            collection_id0 = newest0["collection_id"]
            # pdf_url0 = newest0["pdf_url"]
            job_status0 = newest0["status"]["name"]

            collection_id1 = newest1["collection_id"]
            # pdf_url1 = newest1["pdf_url"]
            job_status1 = newest1["status"]["name"]

            if job_status0 != "failed" and job_status1 != "failed":

                print("\nJOBS NOT COMPLETED YET, WAITING...")

                sleep(5)

                continue

            elif job_status0 == "failed" and job_status1 == "failed":

                print("\nJOBS COMPLETED SUCCESSFULLY")
                assert collection_id0 == "col11496"
                assert job_status0 == "failed"
                # assert collection_id0 in pdf_url0

                assert collection_id1 == "col11992"
                assert job_status1 == "failed"
                # assert collection_id1 in pdf_url1

                break

            else:

                continue
