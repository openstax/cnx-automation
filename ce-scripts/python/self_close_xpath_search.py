import os
import re
import urllib
from collections import Counter

from python.shared.utils import make_destination_folder, to_csv, get_json_reponse

HERE = os.path.abspath(os.path.dirname(__file__))

# Match books in REX: https://github.com/openstax/rex-web/blob/master/src/config.js
BOOKS = [
    {"title": "Prealgebra", "cnx_id": "caa57dab-41c7-455e-bd6f-f443cda5519c"},
    #    {'title': 'Elementary Algebra', 'cnx_id': '0889907c-f0ef-496a-bcb8-2a5bb121717f'},
    {"title": "Intermediate Algebra", "cnx_id": "02776133-d49d-49cb-bfaa-67c7f61b25a1"},
    #    {'title': 'College Algebra', 'cnx_id': '9b08c294-057f-4201-9f48-5d6ad992740d'},
    #    {'title': 'Algebra and Trigonometry', 'cnx_id': '13ac107a-f15f-49d2-97e8-60ab2e3b519c'},
    {"title": "Precalculus", "cnx_id": "fd53eae1-fa23-47c7-bb1b-972349835c3c"},
    {"title": "Calculus Volume 1", "cnx_id": "8b89d172-2927-466f-8661-01abc7ccdba4"},
    {"title": "Calculus Volume 2", "cnx_id": "1d39a348-071f-4537-85b6-c98912458c3c"},
    {"title": "Calculus Volume 3", "cnx_id": "a31cd793-2162-4e9e-acb5-6e6bbd76a5fa"},
    {
        "title": "Introductory Statistics",
        "cnx_id": "30189442-6998-4686-ac05-ed152b91b9de",
    },
    #    {'title': 'Introductory Business Statistics',
    #     'cnx_id': 'b56bb9e9-5eb8-48ef-9939-88b1b12ce22f'},
    {
        "title": "Anatomy and Physiology",
        "cnx_id": "14fb4ad7-39a1-4eee-ab6e-3ef2482e3e22",
    },
    {"title": "Astronomy", "cnx_id": "2e737be8-ea65-48c3-aa0a-9f35b4c6a966"},
    #    {'title': 'Biology', 'cnx_id': '185cbf87-c72e-48f5-b51e-f14f21b5eabd'},
    {"title": "Biology 2e", "cnx_id": "8d50a0af-948b-4204-a71d-4826cba765b8"},
    #    {'title': 'Concepts of Biology', 'cnx_id': 'b3c1e1d2-839c-42b0-a314-e119a8aafbdd'},
    {"title": "Microbiology", "cnx_id": "e42bd376-624b-4c0f-972f-e0c57998e765"},
    {"title": "Chemistry 2e", "cnx_id": "7fccc9cf-9b71-44f6-800b-f9457fd64335"},
    #    {'title': 'Chemistry: Atoms First', 'cnx_id': '4539ae23-1ccc-421e-9b25-843acbb6c4b0'},
    {
        "title": "Chemistry: Atoms First 2e",
        "cnx_id": "d9b85ee6-c57f-4861-8208-5ddf261e9c5f",
    },
    {"title": "College Physics", "cnx_id": "031da8d3-b525-429c-80cf-6c8ed997733a"},
    #    {'title': 'University Physics Volume 1', 'cnx_id': 'd50f6e32-0fda-46ef-a362-9bd36ca7c97d'},
    #    {'title': 'University Physics Volume 2', 'cnx_id': '7a0f9770-1c44-4acd-9920-1cd9a99f2a1e'},
    #    {'title': 'University Physics Volume 3', 'cnx_id': 'af275420-6050-4707-995c-57b9cc13c358'},
    #    {'title': 'Biology for AP® Courses', 'cnx_id': '6c322e32-9fb0-4c4d-a1d7-20c95c5c7af2'},
    #    {'title': 'The AP Physics Collection', 'cnx_id': '8d04a686-d5e8-4798-a27d-c608e4d0e187'},
    #    {'title': 'Fizyka dla szkół wyższych. Tom 1', 'cnx_id': '4eaa8f03-88a8-485a-a777-dd3602f6c13e'},
    #    {'title': 'Fizyka dla szkół wyższych. Tom 2', 'cnx_id': '16ab5b96-4598-45f9-993c-b8d78d82b0c6'},
    #    {'title': 'Fizyka dla szkół wyższych. Tom 3', 'cnx_id': 'bb62933e-f20a-4ffc-90aa-97b36c296c3e'},
    #    {'title': 'American Government', 'cnx_id': '5bcc0e59-7345-421d-8507-a1e4608685e8'},
    {
        "title": "American Government 2e",
        "cnx_id": "9d8df601-4f12-4ac1-8224-b450bf739e5f",
    },
    {
        "title": "Principles of Economics 2e",
        "cnx_id": "bc498e1f-efe9-43a0-8dea-d3569ad09a82",
    },
    #    {'title': 'Principles of Macroeconomics 2e','cnx_id': '27f59064-990e-48f1-b604-5188b9086c29'},
    #    {'title': 'Principles of Microeconomics 2e', 'cnx_id': '5c09762c-b540-47d3-9541-dda1f44f16e5'},
    {"title": "Psychology", "cnx_id": "4abf04bf-93a0-45c3-9cbc-2cefd46e68cc"},
    {
        "title": "Introduction to Sociology 2e",
        "cnx_id": "02040312-72c8-441e-a685-20e9333f3e1d",
    },
    #    {'title': 'Principles of Macroeconomics for AP® Courses 2e',
    #     'cnx_id': '9117cf8c-a8a3-4875-8361-9cb0f1fc9362'},
    #    {'title': 'Principles of Microeconomics for AP® Courses 2e',
    #     'cnx_id': '636cbfd9-4e37-4575-83ab-9dec9029ca4e'},
    {"title": "U.S. History", "cnx_id": "a7ba2fb8-8925-4987-b182-5f4429d48daa"},
    {
        "title": "Introduction to Business",
        "cnx_id": "4e09771f-a8aa-40ce-9063-aa58cc24e77f",
    },
    {"title": "Business Ethics", "cnx_id": "914ac66e-e1ec-486d-8a9c-97b0f7a99774"},
    {
        "title": "Principles of Accounting, Volume 2: Managerial Accounting",
        "cnx_id": "920d1c8a-606c-4888-bfd4-d1ee27ce1795",
    },
    {
        "title": "Principles of Accounting, Volume 1: Financial Accounting",
        "cnx_id": "9ab4ba6d-1e48-486d-a2de-38ae1617ca84",
    },
]


def extract_tag_from_match(match):
    """Uses a regex to extract the tag name from a match

    Example:
        '<span xmlns="http://www.w3.org/1999/xhtml" data-type="title"/>'

    returns "span"

    """
    tag_regex = re.compile(r"<(\w+)")
    tag = re.search(tag_regex, match)
    if tag:
        return tag.group(1)
    return None


def build_webview_url(webview_host, book_uuid, page_uuid):
    return f"{webview_host}/contents/{book_uuid}:{page_uuid}"


def save_results(output_dir, filename, results, datestamp=True):
    make_destination_folder(output_dir)
    result_path = os.path.join(output_dir, filename)

    fieldnames = results[0].keys()
    to_csv(fieldnames, results, result_path, datestamp=datestamp)


def add_additional_metadata(
    book_title,
    book_uuid,
    archive_host,
    webview_staging_host,
    webview_prod_host,
    results,
):
    """Adds extra data to the result that we might need. Mostly about the xpath matches

    """
    for result in results:
        matches = result["matches"]
        num_matches = len(matches)

        # Extract the tag from the match and create a counter. Return top 3 counts
        match_tags = [extract_tag_from_match(match=match) for match in matches]
        match_tags_unique = list(set(match_tags))
        match_counts = Counter(match_tags)
        top_three_matches = match_counts.most_common(3)

        result["book_title"] = book_title
        result["archive_host"] = archive_host
        result["archive_html_url"] = urllib.parse.urljoin(archive_host, result["uri"])
        result["total_matches"] = num_matches
        result["match_counts"] = [f"{k}: {v}" for k, v in match_counts.items()]
        result["match_tags"] = match_tags_unique
        result["match_top_three"] = [f"{i[0]}: {i[1]}" for i in top_three_matches]
        result["staging_webview_url"] = build_webview_url(
            webview_host=webview_staging_host,
            book_uuid=book_uuid,
            page_uuid=result["uuid"],
        )
        result["prod_webview_url"] = build_webview_url(
            webview_host=webview_prod_host,
            book_uuid=book_uuid,
            page_uuid=result["uuid"],
        )

    return results


def do_xpath_search(archive_url, cnx_id, xpath_query, type="baked-html"):
    """Does an xpath search against an archive instance and returns json

    """
    params = dict(id=cnx_id, q=xpath_query, type=type)

    return get_json_reponse(url=archive_url, **params)


if __name__ == "__main__":
    archive_host = "https://archive.cnx.org"
    webview_staging_host = "https://staging.cnx.org"
    webview_prod_host = "https://cnx.org"
    xpath_search_url = f"{archive_host}/xpath.json"
    output_dir = os.path.join(HERE, "output")
    output_filename = os.path.join(output_dir, "production-search-results_before_fix")

    xitems = [
        "//h:em[not(node())]",
        "//h:strong[not(node())]",
        "//h:sub[not(node())]",
        "//h:sup[not(node())]",
        "//h:iframe[not(node())]",
        "//h:span[not(node())]",
        "//h:h3[not(node())]",
        "//h:section[not(node())]",
        "//h:figure[not(node())]",
        "//h:u[not(node())]",
        "//h:a[not(node())]",
        "//h:figcaption[not(node())]",
    ]

    q = "|".join([i for i in xitems])

    results_data = []

    # Change the range here to target different books.
    # Example BOOKS[9:10] will target Intro. to Statistics
    for book in BOOKS:
        print(f"Searching [{book['title']}] uuid: {book['cnx_id']}")
        results = do_xpath_search(
            archive_url=xpath_search_url, cnx_id=book["cnx_id"], xpath_query=q
        )
        if results:
            print(f"{len(results)} results found.")

            results = add_additional_metadata(
                book_title=book["title"],
                book_uuid=book["cnx_id"],
                archive_host=archive_host,
                webview_staging_host=webview_staging_host,
                webview_prod_host=webview_prod_host,
                results=results,
            )

            results_data.extend(results)

        else:
            print(
                f"No results found for [title: {book['title']}] [uuid: {book['cnx_id']} "
            )

    if results_data:
        print("Saving all result data")
        print(f"{len(results_data)} total result data found")
        save_results(output_dir, output_filename, results_data)
