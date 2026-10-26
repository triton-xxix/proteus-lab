"""P-0228: insider buying clusters from SEC's Form 3/4/5 structured data set, keyless.

Called shot: about 15 issuers in one week with 3+ distinct insiders making open-market buys (code P).
Week: the last full Mon-Fri filing week in the quarter file. Data downloaded to sandbox/p0228/.
"""
import collections
import csv
import datetime as dt
import io
import json
import os
import sys
import urllib.request
import zipfile

Q = sys.argv[1] if len(sys.argv) > 1 else "2026q3"
URL = "https://www.sec.gov/files/structureddata/data/form-345-data-sets/%s_form345.zip" % Q
DL = "/Users/triton/PROTEUS/sandbox/p0228"
OUT = "/Users/triton/PROTEUS/experiments/2026-10-26-P-0228"
UA = {"User-Agent": "Proteus research probe proteus-lab@users.noreply.github.com"}

os.makedirs(DL, exist_ok=True)
zpath = os.path.join(DL, Q + ".zip")
if not os.path.exists(zpath):
    data = urllib.request.urlopen(urllib.request.Request(URL, headers=UA), timeout=120).read()
    open(zpath, "wb").write(data)
print("zip bytes", os.path.getsize(zpath))
z = zipfile.ZipFile(zpath)
print("members", z.namelist())


def rows(name):
    with z.open(name) as f:
        yield from csv.DictReader(io.TextIOWrapper(f, "utf-8", errors="replace"), delimiter="\t")


sub = {}
for r in rows("SUBMISSION.tsv"):
    if r["DOCUMENT_TYPE"] in ("4", "4/A"):
        sub[r["ACCESSION_NUMBER"]] = r
owners = collections.defaultdict(set)
for r in rows("REPORTINGOWNER.tsv"):
    if r["ACCESSION_NUMBER"] in sub:
        owners[r["ACCESSION_NUMBER"]].add(r["RPTOWNERCIK"])
buys = []
for r in rows("NONDERIV_TRANS.tsv"):
    a = r["ACCESSION_NUMBER"]
    if a in sub and r["TRANS_CODE"] == "P" and r.get("TRANS_ACQUIRED_DISP_CD", "A") == "A":
        buys.append(r)
print("form 4 filings", len(sub), "open-market buy rows", len(buys))


def fdate(s):
    return dt.datetime.strptime(s, "%d-%b-%Y").date()


filed = [fdate(s["FILING_DATE"]) for s in sub.values()]
last = max(filed)
monday = last - dt.timedelta(days=last.weekday())
if last.weekday() < 4:
    monday -= dt.timedelta(days=7)
friday = monday + dt.timedelta(days=4)
print("week", monday, "to", friday)

by_issuer = collections.defaultdict(lambda: {"owners": set(), "value": 0.0, "name": "", "ticker": ""})
for r in buys:
    s = sub[r["ACCESSION_NUMBER"]]
    if not (monday <= fdate(s["FILING_DATE"]) <= friday):
        continue
    k = s["ISSUERCIK"]
    by_issuer[k]["name"], by_issuer[k]["ticker"] = s["ISSUERNAME"], s["ISSUERTRADINGSYMBOL"]
    by_issuer[k]["owners"] |= owners[r["ACCESSION_NUMBER"]]
    try:
        by_issuer[k]["value"] += float(r["TRANS_SHARES"] or 0) * float(r["TRANS_PRICEPERSHARE"] or 0)
    except ValueError:
        pass

any_buy = len(by_issuer)
clusters = sorted(((v["ticker"], v["name"], len(v["owners"]), round(v["value"])) for v in by_issuer.values()
                   if len(v["owners"]) >= 3), key=lambda t: -t[2])
print("issuers with any open-market buy that week", any_buy)
print("issuers with 3+ distinct insider buyers", len(clusters))
for c in clusters:
    print("  %-6s %-40s owners %d  value $%s" % (c[0], c[1][:40], c[2], format(c[3], ",")))
json.dump({"quarter": Q, "week": [str(monday), str(friday)], "issuers_any_buy": any_buy,
           "clusters": clusters}, open(os.path.join(OUT, "clusters-%s.json" % Q), "w"), indent=1)
