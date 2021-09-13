def test_wipe_files():

    with open("url_error_list.csv", "w") as ef, open("report.csv", "w") as rt:
        ef.truncate()
        rt.truncate()
