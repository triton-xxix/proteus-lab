"""P-0018 part 3: find the public CSV behind the developer page (it loads by script), download it
with no key, and compare it with the retailer feeds. Usage: python3 fuel_finder_csv.py OUT_DIR
"""
import csv
import io
import json
import os
import re
import statistics
import sys
import time
import urllib.parse
import urllib.request

BASE = "https://www.developer.fuel-finder.service.gov.uk"
UA = {"User-Agent": "Mozilla/5.0 (proteus probe; keyless read)"}


def get(url):
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
            return r.status, r.headers.get("Content-Type"), r.read()
    except urllib.error.HTTPError as e:
        return e.code, e.headers.get("Content-Type"), e.read()[:2000]
    except Exception as e:
        return None, None, f"{type(e).__name__}: {e}".encode()


def main():
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    _, _, page = get(BASE + "/access-latest-fuelprices")
    page = page.decode("utf-8", "replace")
    refs = set(re.findall(r'(?:href|src)="([^"]+)"', page))
    cands = {r for r in refs if "csv" in r.lower()}
    scripts = [r for r in refs if r.endswith(".js")]
    print("hrefs with csv:", sorted(cands))
    print("scripts:", len(scripts))
    for s in scripts:
        _, _, js = get(urllib.parse.urljoin(BASE, s))
        js = js.decode("utf-8", "replace")
        for m in re.findall(r'["\'`]([^"\'`]{0,200}(?:csv|CSV)[^"\'`]{0,200})["\'`]', js):
            if "/" in m and len(m) < 300:
                cands.add(m)
    cands = sorted(cands)
    print("candidates:", cands[:40])

    got = None
    for c in cands:
        if c.startswith("http") or c.startswith("/"):
            url = urllib.parse.urljoin(BASE, c)
            code, ct, body = get(url)
            print(f"TRY {url} -> {code} {ct} {len(body)}B {body[:160]!r}")
            if code == 200 and body[:400].count(b",") > 5 and b"<html" not in body[:400].lower():
                got = (url, body)
                break
            if code == 200 and ct and "json" in ct:
                try:
                    j = json.loads(body)
                    print("  json keys:", list(j)[:10] if isinstance(j, dict) else type(j))
                    link = next((v for v in json.dumps(j).split('"') if v.startswith("http") and "csv" in v.lower()), None)
                    if link:
                        c2, ct2, b2 = get(link)
                        print(f"  follow {link[:120]} -> {c2} {ct2} {len(b2)}B")
                        if c2 == 200:
                            got = (link, b2)
                            break
                except ValueError:
                    pass
    if not got:
        print("NO CSV FOUND")
        return
    url, body = got
    with open(os.path.join(out, "fuel-finder-latest.csv"), "wb") as f:
        f.write(body)
    rows = list(csv.DictReader(io.StringIO(body.decode("utf-8-sig", "replace"))))
    print("CSV", url[:120], len(body), "bytes", len(rows), "rows")
    print("columns:", list(rows[0].keys()) if rows else None)
    print("sample:", rows[0] if rows else None)
    summary = {"url": url.split("?")[0], "bytes": len(body), "rows": len(rows),
               "columns": list(rows[0].keys()) if rows else []}
    with open(os.path.join(out, "csv-summary.json"), "w") as f:
        json.dump(summary, f, indent=1)


if __name__ == "__main__":
    main()
