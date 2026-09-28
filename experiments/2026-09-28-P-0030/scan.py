"""P-0030 scan: which front-page and page-2 stories have no explainer yet (scrimba title
'Explain anything') and would pass the hn.watch gate (article ok, or 10+ comments).
Copy of sandbox/hnwatch/scan.py; writes scan.json next to itself when run from the sandbox."""
import json
import re
import time
import urllib.request
from urllib.parse import urlencode

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0 Safari/537.36 proteus-p0030"


def get(url, accept="text/html"):
    t = time.time()
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": accept})
    r = urllib.request.urlopen(req, timeout=60)
    return r.read().decode("utf-8", "replace"), round(time.time() - t, 2)


ids = []
for p in ("https://hn.watch/", "https://hn.watch/?p=2"):
    text, _ = get(p)
    ids += re.findall(r'data-id="(\d+)"', text)
print("rows", len(ids))
out = []
for i, sid in enumerate(ids):
    hn = "https://news.ycombinator.com/item?id=" + sid
    text, secs = get("https://scrimba.com/explain?" + urlencode({"link": hn, "embed": "1,fullwindow", "play": "1", "via": "hn_watch"}))
    title = (re.search(r"<title>(.*?)</title>", text, re.S) or [None, ""])[1]
    generated = title != "Explain anything"
    row = {"rank": i + 1, "id": sid, "generated": generated, "title": title[:70], "secs": secs}
    if not generated:
        g, gs = get("https://hn.watch/api/story/" + sid, "application/json")
        try:
            b = json.loads(g)
            row["article"] = (b.get("article") or {}).get("status")
            row["comments"] = (b.get("comments") or {}).get("count")
            row["hn_title"] = (b.get("title") or "")[:60]
            row["gate_play"] = (not b.get("url")) or row["article"] == "ok" or (row["comments"] or 0) >= 10
        except Exception as e:
            row["gate_err"] = str(e)[:60]
    out.append(row)
    print(json.dumps(row))
print("generated", sum(1 for r in out if r["generated"]), "of", len(out))
print("candidates", [r["id"] for r in out if not r["generated"] and r.get("gate_play")])
