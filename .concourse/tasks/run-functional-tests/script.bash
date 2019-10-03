#!/bin/bash
set -euo pipefail

base_dir=$(pwd)

cd history-txt

# Map urls to variables generated from the concourse resource
WEBVIEW_BASE_URL=$(jq -r .webview_url < urls.json)
ARCHIVE_BASE_URL=$(jq -r .archive_url < urls.json)
LEGACY_BASE_URL=$(jq -r .legacy_url < urls.json)

# Send a POST request to circleci with the approriate values
RESULT=$(curl --header "Content-Type: application/json" \
         -d '{"build_parameters": {"CIRCLE_JOB": "test-webview",
                                   "LEGACY_BASE_URL": "'"$LEGACY_BASE_URL"'",
                                   "WEBVIEW_BASE_URL": "'"$WEBVIEW_BASE_URL"'",
                                   "ARCHIVE_BASE_URL": "'"$ARCHIVE_BASE_URL"'"}
             }' https://circleci.com/api/v1.1/project/github/openstax/cnx-automation/tree/master\?circle-token\=$CIRCLE_API_TOKEN)

BUILD_PARAMS=$(echo "$RESULT" | jq -r .build_parameters)

echo "Build Parameters=$BUILD_PARAMS"

BUILD_URL=$(echo "$RESULT" | jq -r .build_url | tee $base_dir/build_url)

echo "Circle CI Build URL=$BUILD_URL"
