"""P-0018: find the statutory Fuel Finder scheme from GOV.UK's own keyless search API, then try the
endpoints it points at without a key. Prints what answered and how.
Usage: python3 fuel_finder_probe.py OUT_DIR
"""
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request

UA = {"User-Agent": "Mozilla/5.0 (proteus probe; keyless read)"}


def get(url, accept="*/*"):
    t = time.time()
    try:
        req = urllib.request.Request(url, headers={**UA, "Accept": accept})
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.status, r.headers.get("Content-Type"), r.read(), round(time.time() - t, 2), None
    except urllib.error.HTTPError as e:
        return e.code, e.headers.get("Content-Type"), e.read()[:2000], round(time.time() - t, 2), str(e)
    except Exception as e:
        return None, None, b"", round(time.time() - t, 2), f"{type(e).__name__}: {str(e)[:100]}"


def main():
    out_dir = sys.argv[1]
    os.makedirs(out_dir, exist_ok=True)
    log = {"pulled_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "search": [], "probes": []}

    links = set()
    for q in ["fuel finder", "fuel finder api", "fuel price transparency", "road fuel prices open data"]:
        url = "https://www.gov.uk/api/search.json?" + urllib.parse.urlencode({"q": q, "count": 8})
        code, ctype, body, secs, err = get(url, "application/json")
        hits = []
        if code == 200:
            for r in json.loads(body).get("results", []):
                hits.append({"title": r.get("title"), "link": r.get("link"),
                             "updated": r.get("public_timestamp"), "desc": (r.get("description") or "")[:200]})
                links.add(r.get("link"))
        log["search"].append({"q": q, "status": code, "hits": hits, "error": err})
        print(f"search {q!r}: {code} {len(hits)} hits")
        for h in hits:
            print(f"   {h['updated'][:10] if h['updated'] else '?'}  {h['title']}  {h['link']}")

    # Read the GOV.UK pages that mention fuel finder and harvest any non-gov.uk URLs they cite.
    ext = set()
    for link in sorted(l for l in links if l and "fuel" in l.lower()):
        url = link if link.startswith("http") else "https://www.gov.uk/api/content" + link
        code, ctype, body, secs, err = get(url, "application/json")
        text = body.decode("utf-8", "replace")
        found = set(re.findall(r"https?://[A-Za-z0-9.\-]*(?:fuel|finder)[A-Za-z0-9.\-]*\.[a-z.]+[^\s\"'<>)]*", text))
        ext |= found
        mentions_api = len(re.findall(r"\bAPI\b", text))
        log["probes"].append({"url": url, "status": code, "bytes": len(body), "api_mentions": mentions_api,
                              "fuel_urls": sorted(found)[:20], "error": err})
        print(f"page {url}: {code} {len(body)}B API x{mentions_api} urls={sorted(found)[:6]}")

    # Try each cited fuel/finder host bare, with no key.
    for u in sorted(ext)[:15]:
        code, ctype, body, secs, err = get(u)
        snippet = body[:300].decode("utf-8", "replace").replace("\n", " ")
        log["probes"].append({"url": u, "status": code, "content_type": ctype, "bytes": len(body),
                              "seconds": secs, "snippet": snippet, "error": err})
        print(f"try {u}: {code} {ctype} {len(body)}B {secs}s {err or ''} | {snippet[:140]}")

    with open(os.path.join(out_dir, "probe.json"), "w") as f:
        json.dump(log, f, indent=1)


if __name__ == "__main__":
    main()
