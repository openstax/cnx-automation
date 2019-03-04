#!/usr/bin/env python
import json
import os
import subprocess

with open("history/urls.json", "r") as infile:
    urls = json.loads(infile)

print(urls)

os.environ["PYTHONUNBUFFERED"] = "1"
os.environ["WEBVIEW_BASE_URL"] = urls["webview_url"]
os.environ["LEGACY_BASE_URL"] = urls["legacy_url"]
os.environ["ARCHIVE_BASE_URL"] = urls["archive_url"]


def run(cmd):
    proc = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True
    )
    stdout = []
    stderr = []
    mix = []

    while proc.poll() is None:
        line = proc.stdout.readline()
        if line != "":
            stdout.append(line)
            mix.append(line)
            print(line, end="")

        line = proc.stderr.readline()
        if line != "":
            stderr.append(line)
            mix.append(line)
            print(line, end="")

    return proc.returncode, stdout, stderr, mix


code, out, err, mix = run("make test-webview")

exit(code)
