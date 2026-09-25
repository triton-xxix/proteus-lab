"""P-0018 part 5: do exactly what the public "Download the CSV file" button does, anonymously:
GET /fuel-finder/internal-api/download-csv (sets a cookie), then GET the presigned-url endpoint with
that cookie, then fetch the redirectUrl. Only the CSV path; nothing else is called with the token.
Then compare the CSV with the retailer feeds. Usage: python3 fuel_finder_download.py OUT_DIR
"""
import csv
import http.cookiejar
import io
import json
import os
import statistics
import sys
import time
import urllib.request

DEV = "https://www.developer.fuel-finder.service.gov.uk"
PATH = "/internal/v1.0.2/csv/generate-presigned-url"
BASES = [DEV, "https://www.fuel-finder.service.gov.uk", DEV + "/fuel-finder"]

jar = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))
UA = {"User-Agent": "Mozilla/5.0 (proteus probe; keyless read)", "Accept": "application/json",
      "Referer": DEV + "/access-latest-fuelprices"}


def get(url, extra=None):
    try:
        with opener.open(urllib.request.Request(url, headers={**UA, **(extra or {})}), timeout=90) as r:
            return r.status, r.headers.get("Content-Type"), r.read()
    except urllib.error.HTTPError as e:
        return e.code, e.headers.get("Content-Type"), e.read()[:1500]
    except Exception as e:
        return None, None, f"{type(e).__name__}: {e}".encode()


def num(v):
    try:
        v = float(v)
    except (TypeError, ValueError):
        return None
    if v < 10:
        v *= 100
    if v > 1000:
        v /= 10
    return v if 100 <= v <= 250 else None


def main():
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    code, ct, body = get(DEV + "/fuel-finder/internal-api/download-csv")
    print("cookie step", code, [c.name for c in jar])
    token = json.loads(body).get("token") if code == 200 else None
    meta = None
    for base in BASES:
        for extra in ({}, {"x-access-token": token} if token else None):
            if extra is None:
                continue
            c, t, b = get(base + PATH, extra)
            print(f"TRY {base}{PATH} hdr={'token' if extra else 'cookie'} -> {c} {t} {b[:220]!r}")
            if c == 200 and t and "json" in t:
                meta = json.loads(b)
                break
        if meta:
            break
    if not meta:
        print("NO PRESIGNED URL")
        return
    data = meta.get("data", meta)
    print("generated_at", data.get("generated_at"))
    link = data.get("redirectUrl")
    t0 = time.time()
    c, t, csvb = get(link, {"Accept": "*/*"})
    print("csv", c, t, len(csvb), "bytes", round(time.time() - t0, 1), "s")
    if c != 200:
        return
    with open(os.path.join(out, "fuel-finder-latest.csv"), "wb") as f:
        f.write(csvb)
    rows = list(csv.DictReader(io.StringIO(csvb.decode("utf-8-sig", "replace"))))
    cols = list(rows[0].keys()) if rows else []
    print("rows", len(rows))
    print("columns", cols)
    print("sample", json.dumps(rows[0])[:900] if rows else None)
    summary = {"generated_at": data.get("generated_at"), "bytes": len(csvb), "rows": len(rows), "columns": cols}
    for fuel in ("E10", "B7"):
        pc = next((k for k in cols if fuel.lower() in k.lower() and "price" in k.lower() and "time" not in k.lower()
                   and "date" not in k.lower() and "update" not in k.lower()), None)
        if not pc:
            continue
        vals = [v for v in (num(r.get(pc)) for r in rows) if v]
        summary[fuel] = {"column": pc, "n": len(vals), "median": round(statistics.median(vals), 1),
                         "p10": round(statistics.quantiles(vals, n=10)[0], 1),
                         "p90": round(statistics.quantiles(vals, n=10)[-1], 1)}
    bc = next((k for k in cols if "brand" in k.lower()), None)
    if bc:
        brands = {}
        for r in rows:
            brands[r.get(bc)] = brands.get(r.get(bc), 0) + 1
        summary["top_brands"] = sorted(brands.items(), key=lambda kv: -kv[1])[:15]
    print(json.dumps(summary, indent=1))
    with open(os.path.join(out, "csv-summary.json"), "w") as f:
        json.dump(summary, f, indent=1)


if __name__ == "__main__":
    main()
