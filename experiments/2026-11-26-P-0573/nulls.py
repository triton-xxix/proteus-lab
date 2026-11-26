import json, sys, os, datetime as dt
d = sys.argv[1]
sets = {}
for f in sorted(os.listdir(d)):
    if f == "summary.json" or not f.endswith(".json"):
        continue
    r = json.load(open(os.path.join(d, f)))["chart"]["result"][0]
    sets[f[:-5]] = {t for t, c in zip(r["timestamp"], r["indicators"]["quote"][0]["close"]) if c is None}
common = set.intersection(*sets.values())
print("common null timestamps:", len(common), "of", {k: len(v) for k, v in sets.items()})
for t in sorted(common):
    print(dt.datetime.fromtimestamp(t, dt.timezone.utc).isoformat())
