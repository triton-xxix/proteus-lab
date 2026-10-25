"""P-0218: count OSM nodes tagged surveillance:type=ALPR in the UK and the US via Overpass (count only)."""
import json, time, urllib.parse, urllib.request

URL = "https://overpass-api.de/api/interpreter"
OUT = "/Users/triton/PROTEUS/experiments/2026-10-25-P-0218/results.json"
AREAS = {"UK": "GB", "US": "US"}

res = {}
for name, iso in AREAS.items():
    q = ('[out:json][timeout:180];area["ISO3166-1"="%s"][admin_level=2]->.a;'
         '(node["surveillance:type"="ALPR"](area.a);way["surveillance:type"="ALPR"](area.a););out count;' % iso)
    req = urllib.request.Request(URL, urllib.parse.urlencode({"data": q}).encode(), {"User-Agent": "proteus-probe/1"})
    t = time.time()
    try:
        with urllib.request.urlopen(req, timeout=200) as r:
            data = json.load(r)
        tags = data["elements"][0]["tags"]
        res[name] = {"nodes": int(tags.get("nodes", 0)), "ways": int(tags.get("ways", 0)), "secs": round(time.time() - t, 1)}
    except Exception as e:
        res[name] = {"error": str(e)[:200], "secs": round(time.time() - t, 1)}
    print(name, res[name])
    time.sleep(2)

json.dump({"at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "endpoint": URL, "counts": res}, open(OUT, "w"), indent=1)
