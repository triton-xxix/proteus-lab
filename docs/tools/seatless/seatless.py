"""seatless.py: how many of a UK Parliament petition's UK signatures sit in no constituency?

Every petition on petition.parliament.uk publishes two counts that should agree: the UK row of
signatures_by_country, and the sum of signatures_by_constituency. They do not. This tool fetches
petitions (open or archived, keyless), takes the UK row minus the constituency sum, and reports the
gap, the share, and the share by the month each petition opened. From probes P-0516 and P-0517.

    python3 seatless.py --ids 300412 241584           # named petitions, open or archived
    python3 seatless.py --parliament 4 --top 400      # the 400 most-signed of the 2019-24 Parliament
    python3 seatless.py --parliament 4 --top 400 --out run.json --csv rows.csv
    python3 seatless.py --from run.json               # re-score a saved run, no fetching

Standard library only. Spaces requests (--sleep, default 0.15 s). The archived list is served largest
first; the tool checks that and says so.
"""
import argparse
import csv
import json
import sys
import time
import urllib.error
import urllib.request
from collections import defaultdict

BASE = "https://petition.parliament.uk/"
UA = {"User-Agent": "seatless/1.0 (petition constituency gap check)"}


def get(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def petition(pid):
    """Open petitions live at /petitions/ID.json, archived ones at /archived/petitions/ID.json."""
    for path, kind in (("archived/petitions/%s.json", "archived"), ("petitions/%s.json", "open")):
        try:
            return get(BASE + path % pid)["data"]["attributes"], kind
        except urllib.error.HTTPError as e:
            if e.code != 404:
                raise
    raise LookupError("petition %s not found open or archived" % pid)


def row(pid, a, kind):
    by_country = a.get("signatures_by_country") or []
    by_const = a.get("signatures_by_constituency") or []
    uk = next((c["signature_count"] for c in by_country if c.get("code") == "GB"), None)
    placed = sum(c["signature_count"] for c in by_const)
    r = {"id": int(pid), "kind": kind, "title": (a.get("action") or "")[:120],
         "opened": (a.get("opened_at") or "")[:10], "signatures": a.get("signature_count"),
         "uk": uk, "placed": placed, "seats": len(by_const)}
    if uk:
        r["gap"] = uk - placed
        r["share"] = round(r["gap"] / uk, 5)
    return r


def list_archived(parl, top, sleep, floor):
    listed, page, sorted_desc, last = [], 1, True, None
    while len(listed) < top:
        d = get(BASE + "archived/petitions.json?parliament=%d&state=published&page=%d" % (parl, page))
        data = d.get("data", [])
        if not data:
            break
        for p in data:
            c = p["attributes"].get("signature_count") or 0
            if last is not None and c > last:
                sorted_desc = False
            last = c
            if c >= floor:
                listed.append(p["id"])
        if last is not None and last < floor:
            break
        page += 1
        time.sleep(sleep)
    return listed[:top], sorted_desc


def summarise(rows):
    ok = [r for r in rows if "gap" in r]
    uk, gap = sum(r["uk"] for r in ok), sum(r["gap"] for r in ok)
    months = defaultdict(lambda: [0, 0, 0])
    for r in ok:
        m = months[r["opened"][:7] or "unknown"]
        m[0] += 1
        m[1] += r["uk"]
        m[2] += r["gap"]
    return {"petitions": len(rows), "read": len(ok), "errors": sum(1 for r in rows if "error" in r),
            "no_uk_row": sum(1 for r in rows if "error" not in r and "gap" not in r),
            "uk": uk, "gap": gap, "share": round(gap / uk, 5) if uk else None,
            "negative": sum(1 for r in ok if r["gap"] < 0),
            "by_month": {k: {"n": v[0], "uk": v[1], "gap": v[2], "share": round(v[2] / v[1], 5)}
                         for k, v in sorted(months.items())}}


def report(out):
    s = out["summary"]
    print("%d petitions, %d read, %d errors | UK %s, in no seat %s, share %s%% | negative gaps %d"
          % (s["petitions"], s["read"], s["errors"], format(s["uk"], ","), format(s["gap"], ","),
             "%.2f" % (100 * s["share"]) if s["share"] is not None else "-", s["negative"]))
    for k, v in s["by_month"].items():
        print("  %s  %3d petitions  %6.2f%%  %s" % (k, v["n"], 100 * v["share"], "#" * int(round(v["share"] * 1000))))


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--ids", nargs="*", default=[])
    ap.add_argument("--parliament", type=int, help="archived Parliament number (4 is 2019-24, 3 is 2017-19)")
    ap.add_argument("--top", type=int, default=100)
    ap.add_argument("--floor", type=int, default=0, help="stop the list below this many signatures")
    ap.add_argument("--sleep", type=float, default=0.15)
    ap.add_argument("--out")
    ap.add_argument("--csv")
    ap.add_argument("--from", dest="src")
    a = ap.parse_args()
    if a.src:
        out = json.load(open(a.src))
        out["summary"] = summarise(out["rows"])
    else:
        ids, meta = list(a.ids), {}
        if a.parliament:
            got, sorted_desc = list_archived(a.parliament, a.top, a.sleep, a.floor)
            ids += [str(i) for i in got]
            meta = {"parliament": a.parliament, "top": a.top, "listed": len(got), "sorted_desc": sorted_desc}
        if not ids:
            ap.error("give --ids, --parliament or --from")
        rows = []
        for pid in ids:
            try:
                rows.append(row(pid, *petition(pid)))
            except Exception as e:  # noqa: BLE001 - one bad petition never stops the run
                rows.append({"id": int(pid), "error": str(e)[:120]})
            time.sleep(a.sleep)
        out = {"at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "query": meta, "rows": rows}
        out["summary"] = summarise(rows)
    if a.out:
        with open(a.out, "w") as f:
            json.dump(out, f, indent=1)
    if a.csv:
        with open(a.csv, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["id", "opened", "uk", "placed", "gap", "share", "title"])
            for r in out["rows"]:
                if "gap" in r:
                    w.writerow([r["id"], r["opened"], r["uk"], r["placed"], r["gap"], r["share"], r["title"]])
    report(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
