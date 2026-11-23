#!/usr/bin/env python3
"""trade_finder: plumbing and heating firms in a UK area from OpenStreetMap, keyless.

Usage:
  python3 trade_finder.py --area "Greater Manchester" --out run.json
  python3 trade_finder.py --from run.json --out run.json   # re-summarise a saved pull

Pulls every node, way and relation tagged craft=plumber|hvac|heating_engineer|gas_fitter inside
the named admin boundary (admin_level 6 by default) from the public Overpass API, keeps name,
craft, website, phone, postcode and a centre point, and writes rows plus a summary. A row with a
website is a lead. Stdlib only. It never contacts a firm.
"""
import argparse
import json
import sys
import time
import urllib.parse
import urllib.request

ENDPOINT = "https://overpass-api.de/api/interpreter"
CRAFTS = ["plumber", "hvac", "heating_engineer", "gas_fitter"]


def query(area, level):
    crafts = "|".join(CRAFTS)
    if level == "bbox":
        return f'[out:json][timeout:90];nwr["craft"~"^({crafts})$"]({area});out center tags;'
    sel = '["boundary"]' if level == "any" else f'["boundary"="administrative"]["admin_level"="{level}"]'
    return (
        '[out:json][timeout:90];'
        f'area{sel}["name"="{area}"]->.a;'
        f'nwr["craft"~"^({crafts})$"](area.a);'
        'out center tags;'
    )


def fetch(area, level, endpoint=ENDPOINT):
    body = urllib.parse.urlencode({"data": query(area, level)}).encode()
    req = urllib.request.Request(endpoint, data=body, headers={"User-Agent": "proteus-trade-finder/0.1"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.load(r)


def row(el):
    t = el.get("tags", {})
    lat = el.get("lat", el.get("center", {}).get("lat"))
    lon = el.get("lon", el.get("center", {}).get("lon"))
    pc = t.get("addr:postcode", "")
    return {
        "osm": f'{el["type"]}/{el["id"]}',
        "name": t.get("name", ""),
        "craft": t.get("craft", ""),
        "website": t.get("website") or t.get("contact:website") or "",
        "phone": t.get("phone") or t.get("contact:phone") or "",
        "postcode": pc,
        "area": "".join(c for c in pc.split(" ")[0] if c.isalpha()).upper() if pc else "",
        "lat": lat,
        "lon": lon,
    }


def summarise(rows):
    s = {"firms": len(rows)}
    s["with_website"] = sum(1 for r in rows if r["website"])
    s["with_phone"] = sum(1 for r in rows if r["phone"])
    s["with_both"] = sum(1 for r in rows if r["website"] and r["phone"])
    s["with_name"] = sum(1 for r in rows if r["name"])
    s["with_postcode"] = sum(1 for r in rows if r["postcode"])
    s["leads"] = s["with_website"]
    by = {}
    for r in rows:
        b = by.setdefault(r["craft"], {"firms": 0, "website": 0, "phone": 0})
        b["firms"] += 1
        b["website"] += bool(r["website"])
        b["phone"] += bool(r["phone"])
    s["by_craft"] = dict(sorted(by.items(), key=lambda kv: -kv[1]["firms"]))
    areas = {}
    for r in rows:
        k = r["area"] or "none"
        areas[k] = areas.get(k, 0) + 1
    s["by_postcode_area"] = dict(sorted(areas.items(), key=lambda kv: -kv[1]))
    return s


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--area", default="Greater Manchester")
    ap.add_argument("--level", default="6")
    ap.add_argument("--endpoint", default=ENDPOINT, help="another Overpass instance if the main one is busy")
    ap.add_argument("--from", dest="src")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    if a.src:
        run = json.load(open(a.src))
        rows = run["rows"]
        meta = run["meta"]
    else:
        t0 = time.time()
        data = fetch(a.area, a.level, a.endpoint)
        rows = sorted((row(e) for e in data.get("elements", [])), key=lambda r: r["osm"])
        meta = {
            "area": a.area,
            "admin_level": a.level,
            "crafts": CRAFTS,
            "endpoint": a.endpoint,
            "osm_timestamp": data.get("osm3s", {}).get("timestamp_osm_base", ""),
            "pulled_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "seconds": round(time.time() - t0, 1),
        }
    out = {"meta": meta, "summary": summarise(rows), "rows": rows}
    with open(a.out, "w") as f:
        json.dump(out, f, indent=1)
    s = out["summary"]
    print(f'{s["firms"]} firms, {s["with_website"]} with a website, {s["with_phone"]} with a phone, '
          f'{s["with_both"]} both; crafts {json.dumps({k: v["firms"] for k, v in s["by_craft"].items()})}')
    if not rows:
        sys.exit("no rows: check the area name and admin level")


if __name__ == "__main__":
    main()
