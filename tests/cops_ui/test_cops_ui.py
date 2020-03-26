import requests

import pytest

from urllib.error import HTTPError, URLError
from requests.exceptions import ConnectionError

from time import sleep
from tkinter import Tk, Button

from selenium.webdriver.common.keys import Keys

"""
Testing the pdf link after cops job is completed to see that pdf has pages and content
Latest update on 16/03/2020
"""


def test_cops_errors(selenium, cops_base_url, cops_api_url, create_button):

    cancel_button = "#app > div.v-dialog__content.v-dialog__content--active > div > div > div.v-card__actions > button:nth-child(2) > span"

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

        assert response.status_code == 200

        # opening 'CREATE A NEW PDF JOB' dialog

        root = Tk()

        selenium.get(cops_base_url)

        btn = Button(root, text="cops page", command=test_cops_errors)
        btn.pack()

        elem = selenium.find_element_by_class_name("v-btn__content")
        elem.click()

        sleep(2)

        selenium.find_element_by_tag_name("body").send_keys(Keys.TAB, "colid")
        selenium.find_element_by_tag_name("body").send_keys(Keys.TAB, "vers")
        selenium.find_element_by_tag_name("body").send_keys(Keys.TAB)
        selenium.find_element_by_tag_name("body").send_keys(Keys.TAB)

        sleep(2)

        create_button_xp = selenium.find_element_by_xpath(create_button)
        create_button_xp.click()
        create_button_xp.click()

        sleep(2)

        box_cancel_button = selenium.find_element_by_css_selector(cancel_button)
        box_cancel_button.click()

        sleep(2)

        elem = selenium.find_element_by_class_name("v-btn__content")
        elem.click()

        sleep(2)

        root.destroy()
        root.mainloop()
