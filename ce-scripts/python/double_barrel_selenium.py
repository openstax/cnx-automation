import os
import random
import sys

from selenium import webdriver
import chromedriver_binary  # Adds chromedriver binary to path

from python.shared.utils import save_csv_results, get_rows_from_csv

HERE = os.path.abspath(os.path.dirname(__file__))


def get_user_response(prompt=">>> "):
    response = input(
        f"--------------------------\n"
        f"Do the pages look correct?\n\n"
        f"Press 1 for Pass\n"
        f"Press 2 for Fail\n"
        f"Press 3 for Quit\n\n{prompt}"
    )

    return response


if __name__ == "__main__":

    output_dir = os.path.join(HERE, "output")
    result_output_path = os.path.join(output_dir, "test-results.csv")
    input_file = "output/production-search-results_before_fix-20190717.csv"

    # Settings for 1 or 2 browser windows.
    driver_mode = 2  # Set to 1 for one browser, set to 2 for two browsers
    primary_column = "prod_webview_url"
    secondary_column = "staging_webview_url"

    # Do not edit
    driver_dos_set = False
    result_uuids = []

    if os.path.exists(result_output_path):
        result_uuids = [row["uuid"] for row in get_rows_from_csv(result_output_path)]

    test_data = [row for row in get_rows_from_csv(input_file)]

    random_test_data = random.sample(test_data, 10)

    counter = 0
    result_data = []

    while counter <= len(random_test_data):

        for row in random_test_data:

            if row["uuid"] in result_uuids:
                continue

            with webdriver.Chrome() as driver_uno:
                driver_uno.set_window_position(0, 0)

                driver_uno.maximize_window()

                height = driver_uno.get_window_size()["height"]
                width = driver_uno.get_window_size()["width"]

                driver_uno.set_window_size(height, width / 2)

                driver_uno.get(row[primary_column])

                if driver_mode == 2 and secondary_column:

                    driver_dos = webdriver.Chrome()
                    driver_dos_set = True
                    driver_dos.set_window_position(width / 2, 0)
                    driver_dos.set_window_size(height, width / 2)

                    driver_dos.get(row[secondary_column])

                while True:
                    response = get_user_response()

                    if response == "1":
                        if driver_dos_set:
                            driver_dos.close()
                        row["result"] = "PASS"
                        result_data.append(row)
                        counter += 1
                        break
                    elif response == "2":
                        if driver_dos_set:
                            driver_dos.close()
                        row["result"] = "FAIL"
                        result_data.append(row)
                        counter += 1
                        break
                    elif response == "3":
                        if driver_dos_set:
                            driver_dos.close()
                        if result_data:
                            save_csv_results(
                                output_dir, "test-results", result_data, datestamp=False
                            )
                        sys.exit()
                    else:
                        continue

    if result_data:
        save_csv_results(
            output_dir, "test-results", result_data, mode="a", datestamp=False
        )

    print("No more test items to test =)")
