"""P-0112: what does an xAI cashtag count cost, and what drives it? Least-squares fit of cost on cited posts
over the ten xmentions calls in ../2026-10-09-prelisting/xai-calls.jsonl. Writes costfit.json."""
import json
from pathlib import Path

HERE = Path(__file__).parent
rows = [json.loads(l) for l in open(HERE.parent / "2026-10-09-prelisting" / "xai-calls.jsonl") if l.strip()]
xs, ys = [], []
for r in rows:
    if r.get("tag", "").startswith("xmentions-") and r.get("cost_usd"):
        u = r.get("urls") or 0
        xs.append(u if isinstance(u, int) else len(u))
        ys.append(r["cost_usd"])
n = len(xs)
mx, my = sum(xs) / n, sum(ys) / n
slope = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs)
base = my - slope * mx
pred = [base + slope * x for x in xs]
ss_res = sum((y - p) ** 2 for y, p in zip(ys, pred))
ss_tot = sum((y - my) ** 2 for y in ys)
out = {"calls": n, "mean_cost_usd": round(my, 4), "base_usd": round(base, 4), "per_cited_post_usd": round(slope, 5),
       "r2": round(1 - ss_res / ss_tot, 3), "min_cost_usd": min(ys), "min_cited": min(xs),
       "posts_affordable_at_0.05": round((0.05 - base) / slope, 1) if slope else None}
(HERE / "costfit.json").write_text(json.dumps(out, indent=1))
print(json.dumps(out))
