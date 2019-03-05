#!/usr/bin/env python
import json
import os
import subprocess


def run(cmd):
    # https://stackoverflow.com/questions/4417546
    process = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, shell=True
    )

    for line in process.stdout:
        print(line, end="")

    output = process.communicate()[0]
    exit_code = process.returncode

    return exit_code, output


with open("./history/urls.json", "r") as infile:
    urls = json.load(infile)

# Change to cnx-automation resource directory
os.chdir("./cnx-automation")

os.environ["PYTHONUNBUFFERED"] = "1"
os.environ["WEBVIEW_BASE_URL"] = urls["webview_url"]
os.environ["LEGACY_BASE_URL"] = urls["legacy_url"]
os.environ["ARCHIVE_BASE_URL"] = urls["archive_url"]

code, output = run("make test-webview")

exit(code)
