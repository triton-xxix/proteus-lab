"""Which pages ended walks in an error, and what does the API say when asked again?"""
import json
import sys
import urllib.error
from collections import Counter

sys.path.insert(0, "/Users/triton/PROTEUS/experiments/2026-11-05-P-0332")
from ringdate import revid_at, html_of

r = json.load(open("/Users/triton/PROTEUS/experiments/2026-11-05-P-0332/results.json"))
for d, v in r["dates"].items():
    rows = v.get("rows") or []
    ends = Counter(x["path"][-1] for x in rows if x["outcome"] == "error")
    print(d, "errors", sum(ends.values()), ends.most_common(5))
    for title, n in ends.most_common(2):
        try:
            rev = revid_at(title, d)
            print("   ", title, "rev", rev, "bytes", len(html_of(title, rev)))
        except urllib.error.HTTPError as e:
            print("   ", title, "rev", rev, "HTTP", e.code, e.read()[:160])
        except Exception as e:
            print("   ", title, type(e).__name__, str(e)[:160])
