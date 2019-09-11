import urllib.request
import json

"""
Takes a json file and converts it and finds license information
"""

# FINAL VERSION: Sept. 10, 2019

url = input("Add collection/page url: ")
url2 = url.replace("content03", "archive-content03")
url3 = url2 + ".json"

print("Archive .json url: ", url3)

exp_lic = "Creative Commons Attribution-NonCommercial-ShareAlike License"
exp_lic2 = "by-nc-sa"

# Gets the webpage and reads its content
doc_page = urllib.request.urlopen(url3)
webpage_text = doc_page.read()

# Converts json file to str
doc_page.close()
jsondata = json.loads(webpage_text)

# this is a dictionary with license info
lic = jsondata["license"]

licname = lic["name"]
liccode = lic["code"]

print("LICENSE NAME:", licname)
print("LICENSE CODE:", liccode)

assert exp_lic == licname
assert exp_lic2 == liccode
