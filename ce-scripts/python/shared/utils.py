import csv
import os
from datetime import datetime

import requests


def make_destination_folder(folder):
    if not os.path.isdir(folder):
        os.makedirs(folder)


def to_csv(fieldnames, collection, filename, mode="w", datestamp=True):
    if datestamp:
        filename = f"{filename}-{datetime.now().strftime('%Y%m%d')}.csv"
    else:
        filename = f"{filename}.csv"

    print(f"Saving csv file to {filename}")

    with open(filename, mode=mode) as outfile:
        w = csv.DictWriter(outfile, fieldnames, dialect="excel")

        if mode == "a":
            if not os.path.exists(filename):
                w.writeheader()
        else:
            w.writeheader()

        for row in collection:
            w.writerow(row)


def save_csv_results(output_dir, filename, results, mode="w", datestamp=True):
    make_destination_folder(output_dir)
    result_path = os.path.join(output_dir, filename)

    fieldnames = results[0].keys()

    to_csv(fieldnames, results, result_path, mode=mode, datestamp=datestamp)


def get_rows_from_csv(filename):
    with open(filename, "r", encoding="ISO-8859-1") as csvfile:
        datareader = csv.DictReader(csvfile)
        for row in datareader:
            yield {key: value for key, value in row.items()}


def get_json_reponse(url, **kwargs):
    params = kwargs

    r = requests.get(url, params=params)
    r.raise_for_status()
    return r.json()
