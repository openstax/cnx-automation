#!/bin/bash
import json
import os

from string import Template

message_template = """:female-detective: An updated $host_url has been discovered. Browser tests will start in a moment ...
```
$version_data
```
"""

template = Template(message_template)

current_dir = os.getcwd()
history_txt_dir = os.path.join(current_dir, "history-txt")

os.chdir(os.path.join(current_dir, "history-txt"))

with open("app_versions.json", "r") as infile:
    app_versions = json.load(infile)

with open("urls.json", "r") as infile:
    urls = json.load(infile)

webview_url = urls["webview_url"]

print(template.substitute(host_url=webview_url, version_data=app_versions))
