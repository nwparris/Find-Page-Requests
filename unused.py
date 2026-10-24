import re
import sys
import tk
from playwright.sync_api import sync_playwright

tk_title = "URL Dependency Tracker"
tk_minsize = 200
tk_geometry = "300x300+50+50"
tk_input_text = "Please input the URL you would lke to find the API
                 dependencies for."
tk_notURL_text = "Entry not a URL."

option = False
is_headed = len(sys.argv) == 1
if is_headed:
    print("Opening head...")
    root = tk.Tk()
    root.title(tk_title)
    root.minsize(tk_minsize, tk_minsize)
    root.geometry(tk_geometry)
    tk.Label(root, text=tk_input_text)

    tk_URL = tk.StringVar()
    not_URL = True
    submitted = False
    def submit():
        
    while not_URL:
        if submitted:
            tk.Label(root, text=tk_notURL_text)

    root.mainloop()
else:
    page_name = sys.argv[1]

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

prefix = re.compile(r'^https?://')
suffix = re.compile(r'/.*$')
def capture(request, sites):
    site = request.url
    site = re.sub(prefix, '', site)
    site = re.sub(suffix, '', site)
    if request.method != "GET":
        return
    with open(output_file, "a", encoding="utf-8") as file:
        file.write(f"{site}\n")

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    sites = set()
    page.on('request', lambda request: capture(request, sites))
    page.goto(page_name)
    browser.close()

sites = []
with open(output_file, "r", encoding="utf-8") as file:
    sites = file.readlines()

with open(output_file, "w", encoding="utf-8") as file:
    for site in set(sites):
        file.write(site)
