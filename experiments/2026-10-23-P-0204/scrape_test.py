#!/usr/bin/env python3
"""P-0204: does Octocrawl's keyless hosted scrape return Markdown holding at least 90 percent of the words a
plain fetch of the same page holds, on three public pages?

Discovery first: GET the API root and /openapi.json to learn the scrape route and request shape. Then for
each page: a plain fetch (urllib, tags stripped, script and style dropped) and a hosted scrape, trying the
documented route first and two Firecrawl-style shapes as fallbacks. Recall is distinct words (lower case,
letters and digits, 3+ chars) of the plain text found in the Markdown. Keyless, 20 pages a day; this uses 3.
Run: /Users/triton/PROTEUS/.venv/bin/python3 /Users/triton/PROTEUS/experiments/2026-10-23-P-0204/scrape_test.py
"""
import json
import os
import re
import time
import urllib.error
import urllib.request
from html.parser import HTMLParser

HERE = os.path.dirname(os.path.abspath(__file__))
API = "https://api.octocrawl.dev"
UA = "proteus-probe/P-0204 (+https://triton-xxix.github.io/proteus-lab/)"
PAGES = [
    "https://en.wikipedia.org/wiki/HTTP_402",
    "https://docs.python.org/3/library/json.html",
    "https://www.gov.uk/bank-holidays",
]


class Text(HTMLParser):
    def __init__(self):
        super().__init__()
        self.skip = 0
        self.parts = []

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style", "noscript", "svg"):
            self.skip += 1

    def handle_endtag(self, tag):
        if tag in ("script", "style", "noscript", "svg") and self.skip:
            self.skip -= 1

    def handle_data(self, data):
        if not self.skip:
            self.parts.append(data)


def words(s):
    return set(w for w in re.findall(r"[a-z0-9]+", s.lower()) if len(w) >= 3)


def http(url, method="GET", payload=None, headers=None):
    h = {"User-Agent": UA, "Accept": "application/json, text/html;q=0.9, */*;q=0.5"}
    if headers:
        h.update(headers)
    data = None
    if payload is not None:
        data = json.dumps(payload).encode()
        h["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, method=method, headers=h)
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            body = r.read().decode("utf-8", "replace")
            status = r.status
            ctype = r.headers.get("Content-Type", "")
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "replace")
        status = e.code
        ctype = e.headers.get("Content-Type", "")
    return status, body, ctype, round((time.time() - t0) * 1000)


def find_markdown(obj):
    """Depth-first search for a string field called markdown."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k.lower() == "markdown" and isinstance(v, str):
                return v
        for v in obj.values():
            r = find_markdown(v)
            if r:
                return r
    if isinstance(obj, list):
        for v in obj:
            r = find_markdown(v)
            if r:
                return r
    return None


def main():
    out = {"discovery": {}, "pages": []}
    for path in ("/", "/openapi.json", "/v1", "/docs"):
        st, body, ct, ms = http(API + path)
        out["discovery"][path] = {"status": st, "ctype": ct, "ms": ms, "head": body[:1500]}
        print("discovery", path, st, ct, ms, "ms")
        print("  ", body[:600].replace("\n", " "))

    routes = [
        ("POST", "/v1/scrape", lambda u: {"url": u, "formats": ["markdown"]}),
        ("POST", "/scrape", lambda u: {"url": u, "formats": ["markdown"]}),
        ("POST", "/v1/scrape", lambda u: {"url": u}),
        ("GET", "/v1/scrape?url=", None),
    ]
    for url in PAGES:
        rec = {"url": url}
        st, body, ct, ms = http(url)
        p = Text()
        p.feed(body)
        plain = " ".join(p.parts)
        pw = words(plain)
        rec["plain"] = {"status": st, "ms": ms, "bytes": len(body), "distinct_words": len(pw)}
        rec["attempts"] = []
        md = None
        for method, route, shape in routes:
            if method == "GET":
                sst, sbody, sct, sms = http(API + route + urllib.request.quote(url, safe=""))
            else:
                sst, sbody, sct, sms = http(API + route, "POST", shape(url))
            try:
                parsed = json.loads(sbody)
            except Exception:
                parsed = None
            att = {"method": method, "route": route, "status": sst, "ms": sms, "head": sbody[:700]}
            rec["attempts"].append(att)
            print(url, method, route, "->", sst, sms, "ms")
            if sst == 200 and parsed is not None:
                md = find_markdown(parsed)
                att["keys"] = list(parsed.keys()) if isinstance(parsed, dict) else None
                att["state"] = parsed.get("status") if isinstance(parsed, dict) else None
                if md:
                    break
            else:
                print("  ", sbody[:300].replace("\n", " "))
        if md:
            mw = words(md)
            inter = pw & mw
            rec["markdown"] = {
                "chars": len(md),
                "distinct_words": len(mw),
                "plain_words_kept": len(inter),
                "recall_pct": round(100 * len(inter) / max(1, len(pw)), 1),
                "md_words_not_in_plain": len(mw - pw),
                "sample_missing": sorted(pw - mw)[:40],
            }
            with open(os.path.join(HERE, "md_" + re.sub(r"[^a-z0-9]+", "_", url.lower())[:60] + ".md"), "w") as fh:
                fh.write(md)
            print("  recall", rec["markdown"]["recall_pct"], "pct of", len(pw), "plain words; md chars", len(md))
        else:
            rec["markdown"] = None
            print("  no markdown obtained")
        out["pages"].append(rec)
    with open(os.path.join(HERE, "results.json"), "w") as fh:
        json.dump(out, fh, indent=1)


if __name__ == "__main__":
    main()
