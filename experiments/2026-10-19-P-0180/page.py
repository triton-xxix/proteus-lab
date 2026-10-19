"""Build docs/probes/P-0180/data.json from the committed probe files. Numbers on the page come from here."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "docs", "probes", "P-0180", "data.json")


def load(name):
    with open(os.path.join(HERE, name)) as f:
        return json.load(f)


summary = load("summary.json")
launches = load("launches.json")
rows = load("rows-v2.json")
heard_at = {k["sig"]: k["heard"] for k in launches["kept"]}
t0 = min(heard_at.values())

out_rows = []
for r in rows:
    if r.get("status") != "ok":
        continue
    bundled = (r.get("creator_buy_tokens") or 0) > 0
    out_rows.append({
        "creator": r["creator"][:4],
        "bundled": bundled,
        "heard_s": round(heard_at.get(r["sig"], t0) - t0, 1),
        "age_s": r["age_s"],
        "buyers": r["buyers_total"],
        "sellers": r["sellers_total"],
        "first_block_buyers": r["first_block_buyers"],
        "shots": r["shots"],
    })

data = {
    "heard": len(launches["kept"]) + launches["creates_with_buy"],
    "heard_seconds": launches["seconds"],
    "no_buy_in_create": len(launches["kept"]),
    "summary": summary,
    "rows": out_rows,
}
os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w") as f:
    json.dump(data, f, indent=1)
print("wrote", os.path.normpath(OUT), len(out_rows), "rows")
