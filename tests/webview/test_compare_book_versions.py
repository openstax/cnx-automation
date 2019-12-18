from tests import markers
from pages.webview.home import Home
from urllib.request import urlopen
import json
import urllib

"""
Gets the latest versions of all openstax collections on environment 1 and environment 2 and checks
which collection version changed
Latest update on 26/11/2019
"""


@markers.nondestructive
def test_compare_book_versions(
    webview_base_url, archive_base_url, webview_base_url2, archive_base_url2, selenium
):

    home1 = Home(selenium, webview_base_url).open()
    home2 = Home(selenium, webview_base_url2).open()

    for cnx_book1 in home1.featured_books.openstax_list:

        book_title1 = cnx_book1.title
        book_id1 = cnx_book1.cnx_id
        url1 = f"{archive_base_url}" + "/contents/" + f"{book_id1}" + ".json"
        env1 = str(webview_base_url)[8:]

        page1 = urllib.request.urlopen(url1).read()
        jdata1 = json.loads(page1)

        raw_ver1 = {v for k, v in jdata1.items() if k == "version"}
        version1 = str(raw_ver1)[2:-2]

        ver_dict1 = {book_title1: version1}

        k1 = set(ver_dict1.keys())

        for cnx_book2 in home2.featured_books.openstax_list:

            book_title2 = cnx_book2.title
            book_id2 = cnx_book2.cnx_id
            url2 = f"{archive_base_url2}" + "/contents/" + f"{book_id2}" + ".json"
            env2 = str(webview_base_url2)[8:]

            page2 = urllib.request.urlopen(url2).read()
            jdata2 = json.loads(page2)

            raw_ver2 = {v for k, v in jdata2.items() if k == "version"}
            version2 = str(raw_ver2)[2:-2]

            ver_dict2 = {book_title2: version2}

            k2 = set(ver_dict2.keys())

            same_books = set(k1).intersection(set(k2))

            for b in same_books:
                if ver_dict1[b] != ver_dict2[b]:
                    print(
                        "\n"
                        "COLLECTION VERSION CHANGED for "
                        + b
                        + "\n"
                        + env1
                        + ": "
                        + str(ver_dict1[b])
                        + " != "
                        + env2
                        + ": "
                        + str(ver_dict2[b])
                    )
                else:
                    print(
                        "\n"
                        "COLLECTION VERSION UNCHANGED for "
                        + b
                        + "\n"
                        + env1
                        + ": "
                        + str(ver_dict1[b])
                        + " == "
                        + env2
                        + ": "
                        + str(ver_dict2[b])
                    )
