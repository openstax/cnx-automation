import json
import urllib
from urllib.request import urlopen

# from urllib.error import HTTPError

from time import sleep

cops_api_url = "http://localhost/api/jobs/"


def test_api_results(selenium):

    # GIVEN an archive URL for a book
    api_url = f"{cops_api_url}"

    while True:

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

                print("JOBS NOT COMPLETED YET, WAITING...")

                sleep(5)

                continue

            elif job_status0 == "failed" and job_status1 == "failed":

                print("JOBS COMPLETED SUCCESSFULLY")
                assert collection_id0 == "col11496"
                assert job_status0 == "failed"
                # assert collection_id0 in pdf_url0

                assert collection_id1 == "col11992"
                assert job_status1 == "failed"
                # assert collection_id1 in pdf_url1

                break

            else:
                print("UNEXPECTED ERROR")
