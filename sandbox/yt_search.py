#!/usr/bin/env python3
"""Keyless YouTube search: scrape video IDs from the results HTML, write one URL per line.

    python3 yt_search.py "query words" OUT_PATH [N]
"""
import re
import sys
import urllib.parse
import urllib.request

q, out = sys.argv[1], sys.argv[2]
n = int(sys.argv[3]) if len(sys.argv) > 3 else 8
url = "https://www.youtube.com/results?search_query=" + urllib.parse.quote_plus(q)
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0", "Accept-Language": "en-GB"})
html = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "replace")
ids = []
for m in re.finditer(r'"videoId":"([a-zA-Z0-9_-]{11})"', html):
    if m.group(1) not in ids:
        ids.append(m.group(1))
ids = ids[:n]
with open(out, "w") as fh:
    for i in ids:
        fh.write("https://www.youtube.com/watch?v=%s\n" % i)
print(len(ids), "ids")
for i in ids:
    print(i)
