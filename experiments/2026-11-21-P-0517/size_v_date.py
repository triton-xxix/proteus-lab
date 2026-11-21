"""P-0517: does the unplaced-signature hole on archived 2019-24 petitions track size or calendar?

Keyless. Walks archived/petitions.json?parliament=4&state=published pages (the list is sorted by
signature count, largest first) until counts fall under 10,000 or MAXP petitions are listed, fetches
each petition's archived JSON, and records the UK row minus the constituency sum. Then splits by
size band and opening year.

    python3 size_v_date.py
"""
import json, sys, time, urllib.request
from collections import defaultdict
from pathlib import Path

ROOT = "/Users/triton/PROTEUS/"
HERE = Path(__file__).resolve().parent
UA = {"User-Agent": "proteus-lab-check/1.0"}
FLOOR = 10000
MAXP = 400
DEADLINE = time.time() + 9 * 60


def get(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def main():
    if Path(ROOT + "HALT").exists():
        print("HALT")
        return 1
    listed, page, sorted_ok, last = [], 1, True, None
    while len(listed) < MAXP:
        d = get("https://petition.parliament.uk/archived/petitions.json?parliament=4&state=published&page=%d" % page)
        data = d.get("data", [])
        if not data:
            break
        for p in data:
            c = p["attributes"].get("signature_count") or 0
            if last is not None and c > last:
                sorted_ok = False
            last = c
            if c >= FLOOR:
                listed.append(p)
        if last < FLOOR:
            break
        page += 1
        time.sleep(0.2)
    print("listed", len(listed), "pages", page, "sorted", sorted_ok, flush=True)
    rows = []
    for p in listed[:MAXP]:
        if time.time() > DEADLINE:
            print("deadline hit", flush=True)
            break
        try:
            a = get("https://petition.parliament.uk/archived/petitions/%s.json" % p["id"])["data"]["attributes"]
        except Exception as e:  # noqa: BLE001
            rows.append({"id": p["id"], "error": str(e)[:100]})
            continue
        uk = next((c["signature_count"] for c in a.get("signatures_by_country") or [] if c.get("code") == "GB"), None)
        scon = sum(c["signature_count"] for c in a.get("signatures_by_constituency") or [])
        if uk:
            rows.append({"id": p["id"], "opened": (a.get("opened_at") or "")[:7], "uk": uk, "gap": uk - scon})
        time.sleep(0.15)
    ok = [r for r in rows if "gap" in r]
    bands = [(10000, 50000), (50000, 150000), (150000, 10 ** 8)]
    eras = {"2019-20H1": lambda m: m < "2020-03", "lockdown 2020-03..2021-06": lambda m: "2020-03" <= m <= "2021-06",
            "2021-07..2022": lambda m: "2021-07" <= m <= "2022-12", "2023-24": lambda m: m >= "2023-01"}
    table = {}
    for lo, hi in bands:
        for name, f in eras.items():
            sel = [r for r in ok if lo <= r["uk"] < hi and r["opened"] and f(r["opened"])]
            u = sum(r["uk"] for r in sel)
            table["%d-%d | %s" % (lo, hi, name)] = {"n": len(sel), "share": round(sum(r["gap"] for r in sel) / u, 4) if u else None}
    by_month = defaultdict(lambda: [0, 0, 0])
    for r in ok:
        m = by_month[r["opened"]]
        m[0] += 1; m[1] += r["uk"]; m[2] += r["gap"]
    months = {k: {"n": v[0], "share": round(v[2] / v[1], 4)} for k, v in sorted(by_month.items())}
    out = {"at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "listed": len(listed), "sorted_desc": sorted_ok,
           "read": len(ok), "errors": len(rows) - len(ok), "band_by_era": table, "by_month": months, "rows": rows}
    (HERE / "results.json").write_text(json.dumps(out, indent=1))
    print(json.dumps({k: v for k, v in out.items() if k not in ("rows", "by_month")}, indent=1))
    print(json.dumps(months))
    return 0


if __name__ == "__main__":
    sys.exit(main())
