# Content Engineering Scripts

A central location to store content engineering scripts used for ad-hoc purposes and for posterity.


## Scripts contained herein

### Bash
| script                       | description                                                                                                                 |
|------------------------------|-----------------------------------------------------------------------------------------------------------------------------|
| w3c_rex.sh                   | Used to run w3c html validator locally along w/ rex to validate html pages                                                  |

### Python

| script                       | description                                                                                                                 |
|------------------------------|-----------------------------------------------------------------------------------------------------------------------------|
| `self_close_xpath_search.py` | Used to do xpath searches (self closing tags) on html content via archive. Exports results to a csv in `./output`           |
| `double_barrel_selenium.py`  | Uses the results from the previous script to open 1 or 2 browser windows for visual comparison. Exports results with PASS/FAIL in `./output` |
| `gen_book_uris.py`           | Run the script with archive_host and book uuid to generate all the rex urls for a book                                      |
