# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os
import pytest
import requests

from tests.utils import gen_from_file, skip_if_destructive_and_sensitive

DATA_DIR = os.path.join(os.path.realpath(os.path.dirname(__file__)), "data", "webview")


@pytest.fixture
def rex_base_url(request):
    """Return a base URL for REX used for integration testing"""
    config = request.config
    base_url = config.getoption("rex_base_url") or config.getini("rex_base_url")
    if base_url is not None:
        skip_if_destructive_and_sensitive(request, base_url)
        return base_url


@pytest.fixture
def rex_released_books(rex_base_url):
    release_json_url = rex_base_url + "/rex/release.json"
    response = requests.get(release_json_url)
    response.raise_for_status()

    return response.json()["books"]


@pytest.fixture(params=gen_from_file(os.path.join(DATA_DIR, "openstax_books_uuids.txt")))
def openstax_all_books_uuids(request):
    """Yields UUIDs for all openstax books"""
    yield request.param


@pytest.fixture
def s3_base_url(request):
    """Return a base URL for AWS S3 bucket"""
    config = request.config
    base_url = config.getoption("s3_base_url") or config.getini("s3_base_url")
    if base_url is not None:
        skip_if_destructive_and_sensitive(request, base_url)
        return base_url


@pytest.fixture(params=gen_from_file(os.path.join(DATA_DIR, "s3_bucket_books.json")))
def s3_queue_state_bucket_books(request):
    """Yields location of the json file"""
    yield request.param


@pytest.fixture(scope="session")
def aws_access_key_id_value(request):
    """Return value of the aws access key id"""
    config = request.config
    awskeyvalue = config.getoption("aws_access_key_id_value") or config.getini(
        "aws_access_key_id_value"
    )
    if awskeyvalue is not None:
        return awskeyvalue


@pytest.fixture(scope="session")
def aws_secret_access_key_value(request):
    """Return value of the aws secret access key value"""
    config = request.config
    awssecretvalue = config.getoption("aws_secret_access_key_value") or config.getini(
        "aws_secret_access_key_value"
    )
    if awssecretvalue is not None:
        return awssecretvalue


@pytest.fixture
def concourse_base_url(request):
    """Return a concourse base url"""
    config = request.config
    concourse_base_url = config.getoption("concourse_base_url") or config.getini(
        "concourse_base_url"
    )
    if concourse_base_url is not None:
        skip_if_destructive_and_sensitive(request, concourse_base_url)
        return concourse_base_url


@pytest.fixture
def code_tag(request):
    """Return a deployment code tag"""
    config = request.config
    code_tag = config.getoption("code_tag") or config.getini("code_tag")
    if code_tag is not None:
        skip_if_destructive_and_sensitive(request, code_tag)
        return code_tag


@pytest.fixture
def web_hosting_env(request):
    """Return a web hosting environment name (prod or staging)"""
    config = request.config
    web_hosting_env = config.getoption("web_hosting_env") or config.getini("web_hosting_env")
    if web_hosting_env is not None:
        skip_if_destructive_and_sensitive(request, web_hosting_env)
        return web_hosting_env


@pytest.fixture
def jobs_folder(request):
    """Return a section of jobs folder (jobs/bakery or jobs/archive-bakery)"""
    config = request.config
    jobs_folder = config.getoption("jobs_folder") or config.getini("jobs_folder")
    if jobs_folder is not None:
        skip_if_destructive_and_sensitive(request, jobs_folder)
        return jobs_folder


@pytest.fixture
def concourse_prefix(code_tag, jobs_folder, web_hosting_env, concourse_base_url):
    """Return a concourse build url including code tag"""
    concourse_prefix = f"{concourse_base_url}/{web_hosting_env}/{jobs_folder}/builds/"
    return concourse_prefix


@pytest.fixture
def s3_archive_folder(code_tag, s3_base_url):
    """Return complete archive folder in aws s3 bucket"""
    s3_archive_folder = f"{s3_base_url}/apps/archive/{code_tag}/contents/"
    return s3_archive_folder


@pytest.fixture
def queue_state_bucket(request):
    """Return queue state bucket name"""
    config = request.config
    queue_state_bucket = config.getoption("queue_state_bucket") or config.getini(
        "queue_state_bucket"
    )
    if queue_state_bucket is not None:
        skip_if_destructive_and_sensitive(request, queue_state_bucket)
        return queue_state_bucket


@pytest.fixture
def queue_filename(request):
    """Return the queue filename json"""
    config = request.config
    queue_filename = config.getoption("queue_filename") or config.getini("queue_filename")
    if queue_filename is not None:
        return queue_filename


@pytest.fixture
def abl_url(request):
    """Return ABL json url"""
    config = request.config
    base_url = config.getoption("abl_url") or config.getini("abl_url")
    if base_url is not None:
        skip_if_destructive_and_sensitive(request, base_url)
        return base_url


@pytest.fixture
def abl_api_approved(abl_url):
    """Return list of dictionaries of approved books in ABL json"""
    abl_dict = requests.get(abl_url).json()
    return abl_dict
