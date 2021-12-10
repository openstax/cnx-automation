import os


def test_wipe_files():
    s3_bucket_books = f"{os.getcwd()}/fixtures/data/webview/s3_bucket_books.json"

    with open("url_failures_report.csv", "w") as ef, open("report.csv", "w") as rt, open(
        s3_bucket_books, "w"
    ) as s3, open("url_others_report.csv", "w") as rs:
        ef.truncate()
        rt.truncate()
        s3.truncate()
        rs.truncate()
