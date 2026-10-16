"""P-0163: count 3+ insider open-market buy clusters in a recent 30-day window, keyless, from SEC data.

Source: SEC Insider Transactions Data Sets (quarterly Form 3/4/5 extracts). A cluster is three or more
distinct reporting owners with open-market purchases (transaction code P) in the same issuer
within the window. Writes clusters.csv and summary.json next to this file.
"""
import csv
import io
import json
import sys
import urllib.request
import zipfile
from collections import defaultdict
from datetime import date, datetime, timedelta
from pathlib import Path

OUT = Path(__file__).resolve().parent
UA = {"User-Agent": "proteus-lab research https://github.com/triton-xxix/proteus-lab"}


def get(url):
    req = urllib.request.Request(url, headers=UA)
    return urllib.request.urlopen(req, timeout=120).read()


def load(q):
    url = f"https://www.sec.gov/files/structureddata/data/insider-transactions-data-sets/{q}_form345.zip"
    raw = get(url)
    (OUT / f"{q}.size").write_text(str(len(raw)))
    z = zipfile.ZipFile(io.BytesIO(raw))
    def tsv(name):
        return list(csv.DictReader(io.TextIOWrapper(z.open(name), encoding="utf-8", errors="replace"), delimiter="\t"))
    return tsv("SUBMISSION.tsv"), tsv("REPORTINGOWNER.tsv"), tsv("NONDERIV_TRANS.tsv")


def parse(d):
    for fmt in ("%d-%b-%Y", "%Y-%m-%d"):
        try:
            return datetime.strptime(d.strip(), fmt).date()
        except ValueError:
            pass
    return None


def main():
    q = sys.argv[1] if len(sys.argv) > 1 else "2026q3"
    sub, own, trans = load(q)
    issuer = {r["ACCESSION_NUMBER"]: (r.get("ISSUERCIK"), r.get("ISSUERTRADINGSYMBOL") or r.get("ISSUERNAME")) for r in sub}
    owners = defaultdict(set)
    for r in own:
        owners[r["ACCESSION_NUMBER"]].add(r["RPTOWNERCIK"])
    buys = []
    for r in trans:
        if r.get("TRANS_CODE") != "P":
            continue
        d = parse(r.get("TRANS_DATE", ""))
        if d:
            buys.append((d, r["ACCESSION_NUMBER"]))
    end = max(d for d, _ in buys)
    start = end - timedelta(days=29)
    by_issuer = defaultdict(set)
    for d, acc in buys:
        if start <= d <= end and acc in issuer:
            by_issuer[issuer[acc]] |= owners[acc]
    clusters = sorted(((k, len(v)) for k, v in by_issuer.items() if len(v) >= 3), key=lambda x: -x[1])
    with open(OUT / "clusters.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["issuer_cik", "symbol", "distinct_buyers"])
        for (cik, sym), n in clusters:
            w.writerow([cik, sym, n])
    summary = {"quarter": q, "window": [start.isoformat(), end.isoformat()], "p_rows_in_window":
               sum(1 for d, _ in buys if start <= d <= end), "issuers_with_buys": len(by_issuer),
               "clusters_3plus": len(clusters), "clusters_5plus": sum(1 for _, n in clusters if n >= 5),
               "top": [[s, n] for (_, s), n in clusters[:10]]}
    (OUT / "summary.json").write_text(json.dumps(summary, indent=1))
    print(json.dumps(summary))


if __name__ == "__main__":
    main()
