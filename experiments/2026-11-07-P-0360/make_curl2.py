"""P-0360, pass 2: the 20-title calls came back with `continue` on 31 of 32 batches and views for only about a
third of the pages. So fetch only the pages on two or more walks (where any ring lives) plus the target and its
last step, five titles a call, paced at 6 a minute.
Usage: python3 -I make_curl2.py WALKS.json OUTDIR HOST EXTRA_TITLE...
"""
import json
import os
import sys
import urllib.parse
from collections import Counter

walks_file, outdir, host, extra = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4:]
os.makedirs(outdir, exist_ok=True)
through = Counter()
for r in json.load(open(walks_file))["rows"]:
    for p in set((r.get("path") or [])[1:]):
        through[p] += 1
titles = [p for p, n in through.most_common() if n >= 2 and "action=edit" not in p]
for t in extra:
    if t not in titles:
        titles.append(t)
lines = ['user-agent = "ProteusLab-pageviews-check/1.1"', "silent", "fail-with-body", 'rate = "6/m"']
n = -1
for n, i in enumerate(range(0, len(titles), 5)):
    q = {"action": "query", "prop": "pageviews", "pvipdays": "60", "format": "json", "formatversion": "2",
         "titles": "|".join(titles[i:i + 5])}
    lines.append('url = "https://%s/w/api.php?%s"' % (host, urllib.parse.urlencode(q)))
    lines.append('output = "%s/small%02d.json"' % (outdir, n))
open(os.path.join(outdir, "curl2.cfg"), "w").write("\n".join(lines) + "\n")
print(len(titles), "titles,", n + 1, "requests")
