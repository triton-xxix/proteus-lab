"""P-0339: write a curl config that fetches the 395 walk pages' pageviews, 20 titles per request.
Usage: python3 -I make_curl.py WALKS.json OUTDIR   then   curl -K OUTDIR/curl.cfg
"""
import json
import os
import sys
import urllib.parse

walks_file, outdir = sys.argv[1], sys.argv[2]
os.makedirs(outdir, exist_ok=True)
titles = []
for r in json.load(open(walks_file))["rows"]:
    for p in (r.get("path") or [])[1:]:
        if p not in titles:
            titles.append(p)
lines = ['user-agent = "ProteusLab-pageviews-check/1.1"', "silent", "fail-with-body"]
first = int(sys.argv[3]) if len(sys.argv) > 3 else 0  # skip batches already fetched
for n, i in enumerate(range(0, len(titles), 20)):
    if n < first or (len(sys.argv) > 4 and n > int(sys.argv[4])):
        continue
    q = {"action": "query", "prop": "pageviews", "pvipdays": "60", "format": "json", "formatversion": "2",
         "titles": "|".join(titles[i:i + 20])}
    lines.append('url = "https://en.wikipedia.org/w/api.php?%s"' % urllib.parse.urlencode(q))
    lines.append('output = "%s/batch%02d.json"' % (outdir, n))
open(os.path.join(outdir, "curl.cfg"), "w").write("\n".join(lines) + "\n")
print(len(titles), "titles,", n + 1, "requests")
