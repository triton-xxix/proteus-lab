#!/usr/bin/env python3
"""Same-day Munich settle check (P-0333, 6 Nov 2026). Keyless, stdlib, reads and prints only.

Prints the Munich-Stadt high so far (DWD station 03379, WMO 10865) from DWD's 10-minute files beside
each open Munich row of exchange/BOOK.csv, a day before the daily file with TXK lands.

  python3 exchange/settlecheck.py            the check
  python3 exchange/settlecheck.py --measure OUT.json
                                             also score the 10-minute maxima against TXK

The book is never written. The high so far is a floor on the day's high, not a settlement.
"""
import csv
import datetime as dt
import io
import json
import pathlib
import statistics
import sys
import urllib.request
import zipfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
SID = "03379"
BASE = "https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/"
URLS = {
    "tt_now": BASE + "10_minutes/air_temperature/now/10minutenwerte_TU_%s_now.zip" % SID,
    "tt_recent": BASE + "10_minutes/air_temperature/recent/10minutenwerte_TU_%s_akt.zip" % SID,
    "tx_now": BASE + "10_minutes/extreme_temperature/now/10minutenwerte_extrema_temp_%s_now.zip" % SID,
    "tx_recent": BASE + "10_minutes/extreme_temperature/recent/10minutenwerte_extrema_temp_%s_akt.zip" % SID,
    "daily": BASE + "daily/kl/recent/tageswerte_KL_%s_akt.zip" % SID,
}


def rows(url, prefix=None):
    """The data rows of a DWD zip as dicts, keys stripped."""
    req = urllib.request.Request(url, headers={"User-Agent": "proteus-settlecheck"})
    blob = urllib.request.urlopen(req, timeout=60).read()
    with zipfile.ZipFile(io.BytesIO(blob)) as z:
        names = [n for n in z.namelist() if n.startswith(prefix or "produkt")]
        text = z.read(names[0]).decode("latin-1")
    lines = text.splitlines()
    head = [h.strip() for h in lines[0].split(";")]
    for line in lines[1:]:
        parts = [p.strip() for p in line.split(";")]
        if len(parts) >= len(head):
            yield dict(zip(head, parts))


def series(key, field):
    """{datetime in UTC: value} for one 10-minute file, -999 dropped."""
    out = {}
    for r in rows(URLS[key]):
        v = r.get(field)
        if v in (None, "", "-999", "-999.0"):
            continue
        out[dt.datetime.strptime(r["MESS_DATUM"], "%Y%m%d%H%M")] = float(v)
    return out


def day_max(s, shift_hours=0):
    """Highest value per day, day boundary moved by shift_hours from UTC."""
    out = {}
    for t, v in s.items():
        d = (t + dt.timedelta(hours=shift_hours)).date().isoformat()
        out[d] = max(out.get(d, -99.0), v)
    return out


def deg(x):
    return int(x + 0.5) if x >= 0 else -int(-x + 0.5)


def score(name, mx, txk, days):
    use = [d for d in days if d in mx]
    gaps = [txk[d] - mx[d] for d in use]
    if not gaps:
        return {"name": name, "days": 0}
    return {
        "name": name, "days": len(use),
        "mean_txk_minus": round(statistics.mean(gaps), 3), "sd": round(statistics.pstdev(gaps), 3),
        "min_gap": round(min(gaps), 2), "max_gap": round(max(gaps), 2),
        "exact_days": sum(abs(g) < 0.05 for g in gaps),
        "same_whole_degree": sum(deg(mx[d]) == deg(txk[d]) for d in use),
    }


def open_munich():
    out = []
    with open(ROOT / "exchange/BOOK.csv", newline="") as f:
        for r in csv.DictReader(f):
            if not r["outcome"] and r["market"] == "Highest Temperature" and "unich" in r["reason"]:
                out.append(r)
    return out


def contract_hit(contract, high):
    """Would this contract win at this high? Bins are '7°C', '18°C or higher', '3°C or lower'."""
    n = int(contract.split("°")[0])
    if "higher" in contract:
        return deg(high) >= n
    if "lower" in contract:
        return deg(high) <= n
    return deg(high) == n


def settled_agreement(utc_days, local_days):
    """Do the settled Munich rows of the book agree with a rule read from the station?"""
    rows_out, n, utc_ok, local_ok = [], 0, 0, 0
    with open(ROOT / "exchange/BOOK.csv", newline="") as f:
        for r in csv.DictReader(f):
            if r["market"] != "Highest Temperature" or "unich" not in r["reason"]:
                continue
            d = r["event_start"][:10]
            if r["outcome"] not in ("winner", "loser") or d not in utc_days or d not in local_days:
                continue
            won = r["outcome"] == "winner"
            u, l = contract_hit(r["contract"], utc_days[d]) == won, contract_hit(r["contract"], local_days[d]) == won
            n, utc_ok, local_ok = n + 1, utc_ok + u, local_ok + l
            if not (u and l):
                rows_out.append({"id": r["id"], "day": d, "contract": r["contract"], "outcome": r["outcome"],
                                 "utc_high": utc_days[d], "local_high": local_days[d]})
    return {"rows": n, "utc_day_agrees": utc_ok, "local_day_agrees": local_ok, "disagreements": rows_out}


def main():
    now = dt.datetime.now(dt.timezone.utc).replace(tzinfo=None)
    tt = series("tt_now", "TT_10")
    tx = series("tx_now", "TX_10")
    latest = max(tt) if tt else None
    if latest is None:
        print("no 10-minute rows in the now file")
        return 1
    age = (now - latest).total_seconds() / 60
    print("now file: %d rows, %s to %s UTC, newest %.0f min old" % (len(tt), min(tt), latest, age))
    print("newest reading %.1f C; extrema file has %d rows, newest %s" % (
        tt[latest], len(tx), max(tx) if tx else "none"))
    tt_days, tx_days = day_max(tt), day_max(tx)
    tx_r = series("tx_recent", "TX_10")  # the now file holds today only; this one holds past days
    past = day_max(tx_r)
    for d in sorted(set(tt_days) | set(tx_days)):
        print("  %s  high so far: TT_10 %s, TX_10 %s" % (d, tt_days.get(d), tx_days.get(d)))
    print("open Munich rows:")
    for r in open_munich():
        d = r["event_start"][:10]
        today = d == now.date().isoformat()
        hi = tx_days.get(d) if today else past.get(d)
        if hi is None:
            print("  %s %s %s p %s: no readings for that day yet" % (r["id"], d, r["contract"], r["p"]))
        else:
            print("  %s %s %s p %s: %s %.1f, rounds to %d" % (
                r["id"], d, r["contract"], r["p"], "high so far" if today else "day's high", hi, deg(hi)))
    if "--measure" not in sys.argv:
        return 0

    out = sys.argv[sys.argv.index("--measure") + 1]
    txk = {}
    for r in rows(URLS["daily"], "produkt_klima_tag"):
        if r.get("TXK") not in (None, "", "-999", "-999.0"):
            d = r["MESS_DATUM"]
            txk["%s-%s-%s" % (d[:4], d[4:6], d[6:8])] = float(r["TXK"])
    tt_r = series("tt_recent", "TT_10")
    days = sorted(d for d in txk if d >= "2026-05-01")
    settled = settled_agreement(day_max(tx_r), day_max(tx_r, 1))
    res = {
        "generated_utc": now.isoformat() + "Z",
        "now_file": {"rows": len(tt), "first": str(min(tt)), "last": str(latest), "age_min": round(age)},
        "txk_days": len(days), "first": days[0], "last": days[-1],
        "recent_tt_last": str(max(tt_r)), "recent_tx_last": str(max(tx_r)),
        "settled_rows": settled,
        "scores": [
            score("TT_10 spot, UTC day", day_max(tt_r), txk, days),
            score("TX_10 extreme, UTC day", day_max(tx_r), txk, days),
            score("TT_10 spot, UTC+1 day", day_max(tt_r, 1), txk, days),
            score("TX_10 extreme, UTC+1 day", day_max(tx_r, 1), txk, days),
        ],
    }
    json.dump(res, open(out, "w"), indent=1)
    print(json.dumps(res, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
