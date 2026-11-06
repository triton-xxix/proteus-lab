"""P-0333 second leg: which station and rounding rule explains the settled Munich rows of the book?

Reads exchange/BOOK.csv and DWD's daily TXK for candidate stations. For each station and rule, counts
how many settled rows the rule gets right, and whether each settled day has exactly one winning bin.
Usage: python3 which_station.py OUT.json
"""
import csv
import io
import json
import math
import sys
import urllib.request
import zipfile

BOOK = "/Users/triton/PROTEUS/exchange/BOOK.csv"
STATIONS = {"03379 Munich-Stadt": "03379", "01262 Munich airport": "01262"}
BASE = ("https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/daily/kl/recent/"
        "tageswerte_KL_%s_akt.zip")


def txk(sid):
    req = urllib.request.Request(BASE % sid, headers={"User-Agent": "proteus-settlecheck"})
    blob = urllib.request.urlopen(req, timeout=60).read()
    with zipfile.ZipFile(io.BytesIO(blob)) as z:
        name = [n for n in z.namelist() if n.startswith("produkt_klima_tag")][0]
        text = z.read(name).decode("latin-1")
    lines = text.splitlines()
    head = [h.strip() for h in lines[0].split(";")]
    out = {}
    for line in lines[1:]:
        r = dict(zip(head, [p.strip() for p in line.split(";")]))
        if r.get("TXK") not in (None, "", "-999", "-999.0"):
            d = r["MESS_DATUM"]
            out["%s-%s-%s" % (d[:4], d[4:6], d[6:8])] = float(r["TXK"])
    return out


RULES = {
    "round": lambda x: math.floor(x + 0.5),
    "floor": math.floor,
    "ceil": math.ceil,
}


def hit(contract, value):
    n = int(contract.split("°")[0])
    if "higher" in contract:
        return value >= n
    if "lower" in contract:
        return value <= n
    return value == n


rows = [r for r in csv.DictReader(open(BOOK, newline=""))
        if r["market"] == "Highest Temperature" and "unich" in r["reason"]
        and r["outcome"] in ("winner", "loser")]
res = {"settled_rows": len(rows), "combos": [], "rows": []}
data = {name: txk(sid) for name, sid in STATIONS.items()}
for name, obs in data.items():
    for rule, f in RULES.items():
        use = [r for r in rows if r["event_start"][:10] in obs]
        ok = sum(hit(r["contract"], f(obs[r["event_start"][:10]])) == (r["outcome"] == "winner") for r in use)
        res["combos"].append({"station": name, "rule": rule, "rows": len(use), "agree": ok})
for r in rows:
    d = r["event_start"][:10]
    res["rows"].append({
        "id": r["id"], "day": d, "contract": r["contract"], "outcome": r["outcome"],
        **{name.split()[0]: data[name].get(d) for name in data},
    })
winners = {}
for r in rows:
    if r["outcome"] == "winner":
        winners.setdefault(r["event_start"][:10], set()).add(r["contract"])
res["winning_days"] = len(winners)
json.dump(res, open(sys.argv[1], "w"), indent=1)
for c in res["combos"]:
    print(c)
for r in res["rows"]:
    print(r["id"], r["day"], r["contract"], r["outcome"], r["03379"], r["01262"])
