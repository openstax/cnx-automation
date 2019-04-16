from dotenv import load_dotenv
import os
import pytest
import urllib.request
from ast import literal_eval
load_dotenv(verbose = True)
url_addr_version = os.environ['URL_ADDR_VERSION']

# adding cnx-deploy version number to applitools screenshot results
@pytest.fixture(scope="session")
def deploy_version_tag(request):
    """Returns cnx version numbers"""

    version_page = urllib.request.urlopen(url_addr_version)
    web_content = version_page.read()

    # convert bytes into strings
    web_ver_dec = web_content.decode('UTF-8')
    # convert strings into dictionary
    cnx_version_dict = literal_eval(web_ver_dec)
    # extracting cnx deploy version number
    cnx_deploy = "-> cnx-deploy: " + cnx_version_dict['cnx-deploy']

    if not cnx_deploy:
        raise Exception("cnx deploy version is missing")
    else:
        yield cnx_deploy

# adding webview version number to applitools screenshot results
@pytest.fixture(scope="session")
def webview_version_tag(request):
    """Returns cnx version numbers"""

    version_page = urllib.request.urlopen(url_addr_version)
    web_content = version_page.read()

    # convert bytes into strings
    web_ver_dec = web_content.decode('UTF-8')
    # convert strings into dictionary
    cnx_version_dict = literal_eval(web_ver_dec)
    # extracting webview version number
    w_webview, w_versions = cnx_version_dict['webview'].split()
    cnx_w_web = w_versions

    if not cnx_w_web:
        raise Exception("cnx webview version is missing")
    else:
        yield cnx_w_web
