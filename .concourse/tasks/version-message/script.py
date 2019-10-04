#!/usr/bin/env python
import json
import os

from string import Template

message_template = """:female-detective: An updated $host_url/history.txt has been discovered.
Tests have been started in CircleCI. Check progress here $circle_url
*version.txt output*
```
date:           $date
webview         $webview
cnx-archive     $archive
cnx-publishing  $publishing
oer.exports     $oer_exports
cnx-press       $press
cnx-deploy      $cnx_deploy
```
"""

template = Template(message_template)

current_dir = os.getcwd()
history_txt_dir = os.path.join(current_dir, "history-txt")
circleci_dir = os.path.join(current_dir, "run-circleci")

os.chdir(os.path.join(current_dir, "history-txt"))

with open("app_versions.json", "r") as infile:
    app_versions = json.load(infile)

with open("urls.json", "r") as infile:
    urls = json.load(infile)

with open(os.path.join(circleci_dir, "build_url"), "r") as infile:
    circle_url = infile.read()

webview_url = urls["webview_url"]

print(
    template.substitute(
        host_url=webview_url,
        date=app_versions["date"],
        webview=app_versions["webview"],
        archive=app_versions["cnx-archive"],
        publishing=app_versions["cnx-publishing"],
        oer_exports=app_versions["oer.exports"],
        press=app_versions["press"],
        cnx_deploy=app_versions["cnx-deploy"],
        circle_url=circle_url,
    )
)
