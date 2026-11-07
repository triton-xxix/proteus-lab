"""P-0360: P-0339's curl config writer with the host as an argument.
Usage: python3 -I make_curl.py WALKS.json OUTDIR HOST   then   curl -K OUTDIR/curl.cfg
"""
import json
import os
import sys
import urllib.parse

walks_file, outdir, host = sys.argv[1], sys.argv[2], sys.argv[3]
os.makedirs(outdir, exist_ok=True)
titles = []
for r in json.load(open(walks_file))["rows"]:
    for p in (r.get("path") or [])[1:]:
        if p not in titles:
            titles.append(p)
first = int(sys.argv[4]) if len(sys.argv) > 4 else 0  # skip batches already fetched
# 10 quick calls drew "too many requests" on 7 Nov, so pace them
lines = ['user-agent = "ProteusLab-pageviews-check/1.1"', "silent", "fail-with-body", 'rate = "6/m"']
n = -1
for n, i in enumerate(range(0, len(titles), 20)):
    if n < first:
        continue
    q = {"action": "query", "prop": "pageviews", "pvipdays": "60", "format": "json", "formatversion": "2",
         "titles": "|".join(titles[i:i + 20])}
    lines.append('url = "https://%s/w/api.php?%s"' % (host, urllib.parse.urlencode(q)))
    lines.append('output = "%s/batch%02d.json"' % (outdir, n))
open(os.path.join(outdir, "curl.cfg"), "w").write("\n".join(lines) + "\n")
print(len(titles), "titles,", n + 1, "requests")
