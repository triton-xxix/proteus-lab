"""P-0424: my exchange book's Brier ratio to the market, beside the two papers' own figures.
Reads exchange/BOOK.csv (read only) and tables.json from pull.py. Prints the paper table rows that
name a model next to Brier numbers so the best and worst can be read off."""
import csv
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
rows = [r for r in csv.DictReader(open("/Users/triton/PROTEUS/exchange/BOOK.csv")) if r["brier"] and r["market_brier"]]


def ratio(rs):
    me = sum(float(r["brier"]) for r in rs) / len(rs)
    mk = sum(float(r["market_brier"]) for r in rs) / len(rs)
    return {"n": len(rs), "my_brier": round(me, 4), "market_brier": round(mk, 4), "gap": round(me - mk, 4),
            "ratio": round(me / mk, 2)}


out = {"book_all": ratio(rows),
       "book_munich": ratio([r for r in rows if r["market"] == "Highest Temperature"]),
       "book_other": ratio([r for r in rows if r["market"] != "Highest Temperature"])}
# figures as printed in the papers' own text (pull.py sentences), quoted in the README
out["forecast_dojo"] = {"scale": "multi-option Brier, uniform forecast 0.771", "market": 0.498, "best_model": 0.546,
                        "best_paired_gap": 0.050, "best_ratio": round(0.546 / 0.498, 2),
                        "no_tools_mean": 0.769, "no_tools_ratio": round(0.769 / 0.498, 2)}
out["llm_crowds"] = {"scale": "binary Brier, 208 Manifold items", "final_market": 0.098, "best_model": 0.273,
                     "local_models": [0.362, 0.413], "ratio_at_cutoff_range": [1.61, 2.64], "ratio_at_cutoff_mean": 1.95,
                     "clean_items_ratio_range": [1.40, 2.68]}
json.dump(out, open(os.path.join(HERE, "results.json"), "w"), indent=1)
for k, v in out.items():
    print(k, json.dumps(v))
t = json.load(open(os.path.join(HERE, "tables.json")))
for pid in t:
    for tb in t[pid]["tables"]:
        flat = [" | ".join(c for c in row if c) for row in tb]
        if any(("Nemotron" in x or "Mistral 7B" in x) for x in flat) and 4 <= len(flat) <= 20:
            print("-- table in", pid)
            for x in flat[:20]:
                print("   ", x[:200])
