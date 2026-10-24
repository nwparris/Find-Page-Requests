# @title: Find-Page-Requests
# @description: Finds all the page requests which a page makes
# @author: Nicholas W. Parris
# @date: Oct. 23, 2026

import re
import sys
from playwright.sync_api import sync_playwright

# Require at least one input (the URL)
if len(sys.argv) == 1:
    raise Exception("Requires at least one arguement.")
else:
    page_name = sys.argv[1]

# Check for options (only one for now is -o to set the output file)
option = None
if len(sys.argv) > 2:
    option = sys.argv[2]

output_file = "out.csv"
match option:
    case None:
        pass
    case "-o":
        if len(sys.argv) > 3:
            output_file = sys.argv[3]
        else:
            raise Exception("No output file specified")
    case _:
        raise Exception(f"Unrecogdnized option {option}")

# Function for capturing the requests
prefix = re.compile(r'^https?://')
suffix = re.compile(r'/.*$')
def capture(request):
    site = request.url
    site = re.sub(prefix, '', site)
    site = re.sub(suffix, '', site)
    if request.method != "GET":
        return
    with open(output_file, "a", encoding="utf-8") as file:
        file.write(f"{site}\n")

# Analyze the requests of the page
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    sites = set()
    page.on('request', capture) # Requests with capture cannot write to single
                                #   variable (threading maybe?)
    page.goto(page_name)
    browser.close()
# The postcondition will be a file with names of pages,
#   but these pages can be empty,
#   and there are duplicates

# So we filter the file
sites = []
with open(output_file, "r", encoding="utf-8") as file:
    sites = file.readlines()
with open(output_file, "w", encoding="utf-8") as file:
    for site in set(sites):
        site = "".join(site.split())
        if site:
            file.write(site + "\n")
