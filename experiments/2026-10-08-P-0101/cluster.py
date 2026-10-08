"""P-0101: do Form 4 cluster buys beat SPY over 30 days? 2025 EDGAR filings.

Cluster: 3 or more distinct reporting owners with open-market purchases (code P) in the same issuer
within 14 days of trade date. The event is known on the filing date of the purchase that completes
the cluster. Entry at the first close strictly after that filing date (a filing can land after the
close), exit at the first close on or after entry + 30 calendar days. Excess = stock return minus
SPY over the same two dates. One event per ticker per 30 days. Prices: Yahoo chart, keyless.

Usage: python -I cluster.py DATA_DIR OUT_DIR   (DATA_DIR holds the SEC form345 zips)
"""
import csv
import io
import json
import pathlib
import statistics
import sys
import time
import urllib.error
import urllib.request
import zipfile
from datetime import date, datetime, timedelta, timezone

csv.field_size_limit(10**9)
UA = {"User-Agent": "Luke Boyd luke.boyd@neptunemarketing.co.uk"}  # contact named by Luke, 9 Oct 2026
QUARTERS = ["2025q1", "2025q2", "2025q3", "2025q4"]
SEC = "https://www.sec.gov/files/structureddata/data/insider-transactions-data-sets/%s_form345.zip"


def fetch_zips(data):
    data.mkdir(parents=True, exist_ok=True)
    for q in QUARTERS:
        p = data / ("%s_form345.zip" % q)
        if p.exists() and p.stat().st_size > 1000:
            continue
        with urllib.request.urlopen(urllib.request.Request(SEC % q, headers=UA), timeout=120) as r:
            p.write_bytes(r.read())
        time.sleep(0.5)


def d(s):
    return datetime.strptime(s.strip(), "%d-%b-%Y").date()


def tsv(z, name):
    with z.open(name) as f:
        return list(csv.DictReader(io.TextIOWrapper(f, "utf-8", errors="replace"), delimiter="\t"))


def purchases(data):
    out = []
    for q in QUARTERS:
        z = zipfile.ZipFile(data / ("%s_form345.zip" % q))
        names = {n.split("/")[-1].upper(): n for n in z.namelist()}
        sub = {r["ACCESSION_NUMBER"]: r for r in tsv(z, names["SUBMISSION.TSV"])}
        owners = {}
        for r in tsv(z, names["REPORTINGOWNER.TSV"]):
            owners.setdefault(r["ACCESSION_NUMBER"], r["RPTOWNERCIK"])
        for r in tsv(z, names["NONDERIV_TRANS.TSV"]):
            if r.get("TRANS_CODE") != "P" or r.get("TRANS_ACQUIRED_DISP_CD") != "A":
                continue
            s = sub.get(r["ACCESSION_NUMBER"])
            if not s or s.get("DOCUMENT_TYPE") not in ("4", "4/A"):
                continue
            sym = (s.get("ISSUERTRADINGSYMBOL") or "").strip().upper()
            if not sym or sym in ("NONE", "N/A") or len(sym) > 5:
                continue
            try:
                td, fd = d(r["TRANS_DATE"]), d(s["FILING_DATE"])
            except ValueError:
                continue
            out.append((sym, td, fd, owners.get(r["ACCESSION_NUMBER"], r["ACCESSION_NUMBER"])))
    return out


def clusters(rows):
    by = {}
    for sym, td, fd, own in rows:
        by.setdefault(sym, []).append((fd, td, own))
    events = []
    for sym, lst in by.items():
        lst.sort()
        last = None
        for i, (fd, td, own) in enumerate(lst):
            known = [x for x in lst[: i + 1] if abs((x[1] - td).days) <= 14]
            if len({x[2] for x in known}) >= 3:
                if last is None or (fd - last).days > 30:
                    events.append((sym, fd))
                    last = fd
    return events


def bars(sym, cache):
    if sym in cache:
        return cache[sym]
    url = "https://query1.finance.yahoo.com/v8/finance/chart/%s?period1=1727740800&period2=1767225600&interval=1d" % sym.replace(".", "-")
    out = None
    for attempt in range(3):
        try:
            r = json.load(urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=30))
            res = r["chart"]["result"][0]
            c = res["indicators"]["quote"][0]["close"]
            out = [(datetime.fromtimestamp(t, tz=timezone.utc).date(), x) for t, x in zip(res["timestamp"], c) if x]
            break
        except urllib.error.HTTPError as e:
            if e.code == 429:
                time.sleep(4 * (attempt + 1))
                continue
            break
        except Exception:
            break
    cache[sym] = out
    time.sleep(0.15)
    return out


def at_or_after(b, day, strict=False):
    for dd, c in b:
        if dd > day or (not strict and dd == day):
            return dd, c
    return None


def main():
    data, out = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
    t0 = time.time()
    fetch_zips(data)
    rows = purchases(data)
    ev = clusters(rows)
    ev = [e for e in ev if e[1] <= date(2025, 11, 25)]
    cache = {}
    spy = bars("SPY", cache)
    res = []
    for sym, fd in ev:
        if time.time() - t0 > 900:
            break
        b = bars(sym, cache)
        if not b:
            continue
        e = at_or_after(b, fd, strict=True)
        if not e:
            continue
        x = at_or_after(b, e[0] + timedelta(days=30))
        se, sx = at_or_after(spy, e[0]), at_or_after(spy, x[0]) if x else None
        if not x or not se or not sx or e[1] < 1.0:
            continue
        r = x[1] / e[1] - 1
        m = sx[1] / se[1] - 1
        res.append({"sym": sym, "filed": fd.isoformat(), "entry": e[0].isoformat(), "exit": x[0].isoformat(),
                    "ret": round(r, 4), "spy": round(m, 4), "excess": round(r - m, 4)})
    ex = [x["excess"] for x in res]
    summ = {
        "purchase_rows": len(rows), "cluster_events": len(ev), "priced": len(res),
        "mean_excess": round(statistics.mean(ex), 4) if ex else None,
        "median_excess": round(statistics.median(ex), 4) if ex else None,
        "beat_spy_share": round(sum(e > 0 for e in ex) / len(ex), 3) if ex else None,
        "t_stat": round(statistics.mean(ex) / (statistics.stdev(ex) / len(ex) ** 0.5), 2) if len(ex) > 2 else None,
        "mean_excess_trim5pct": None, "seconds": round(time.time() - t0),
    }
    if len(ex) > 20:
        s = sorted(ex)
        k = len(s) // 20
        summ["mean_excess_trim5pct"] = round(statistics.mean(s[k: len(s) - k]), 4)
    out.mkdir(parents=True, exist_ok=True)
    (out / "events.json").write_text(json.dumps(res, indent=0))
    (out / "summary.json").write_text(json.dumps(summ, indent=1))
    print(json.dumps(summ))


if __name__ == "__main__":
    main()
