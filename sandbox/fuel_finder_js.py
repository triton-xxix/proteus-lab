"""P-0018 part 4: print the script context around the public CSV download call, to see how the page's
own anonymous download button uses the token. Usage: python3 fuel_finder_js.py
"""
import re
import urllib.parse
import urllib.request

BASE = "https://www.developer.fuel-finder.service.gov.uk"
UA = {"User-Agent": "Mozilla/5.0 (proteus probe; keyless read)"}


def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
        return r.read().decode("utf-8", "replace")


page = get(BASE + "/access-latest-fuelprices")
for s in re.findall(r'src="([^"]+\.js)"', page):
    js = get(urllib.parse.urljoin(BASE, s))
    for kw in ("download-csv", "last-updated", "lastUpdated", "internal-api"):
        for m in re.finditer(re.escape(kw), js):
            print(f"--- {s} [{kw}] @{m.start()}")
            print(js[max(0, m.start() - 500): m.start() + 900])
