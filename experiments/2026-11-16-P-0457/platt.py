"""P-0457: Platt-scale my called shots' stated p against whether the verdict landed.

Called shot (before the run): the fit maps 0.6 to about 0.9 and 0.7 to about 0.93, and the
leave-one-out Brier improves by more than 0.05.

Outcome is the verdict hit (expect == verdict), the same as P-0444's verdict_hit. Fit:
hit ~ logistic(A + B * logit(p)), Newton's method, stdlib. The honest Brier is leave-one-out:
each shot scored by a fit that never saw it. Reads state/probes.json, writes results.json here.
"""
import json, math
from pathlib import Path

HERE = Path(__file__).parent
raw = json.loads(Path("/Users/triton/PROTEUS/state/probes.json").read_text())
items = raw if isinstance(raw, list) else next(v for v in raw.values() if isinstance(v, list) and v and isinstance(v[0], dict))

rows = []
for it in items:
    s = it.get("shot") if isinstance(it, dict) else None
    if not s or it.get("status") != "done" or not it.get("verdict") or s.get("p") is None:
        continue
    p = min(max(float(s["p"]), 0.01), 0.99)
    rows.append((p, 1.0 if s.get("expect") == it["verdict"] else 0.0))


def logit(p):
    return math.log(p / (1 - p))


def fit(data):
    A, B = 0.0, 1.0
    for _ in range(50):
        g0 = g1 = h00 = h01 = h11 = 0.0
        for p, y in data:
            x = logit(p)
            q = 1 / (1 + math.exp(-(A + B * x)))
            g0 += y - q
            g1 += (y - q) * x
            w = q * (1 - q) + 1e-9
            h00 += w; h01 += w * x; h11 += w * x * x
        det = h00 * h11 - h01 * h01
        if abs(det) < 1e-12:
            break
        dA = (h11 * g0 - h01 * g1) / det
        dB = (h00 * g1 - h01 * g0) / det
        A, B = A + dA, B + dB
        if abs(dA) + abs(dB) < 1e-9:
            break
    return A, B


def pred(A, B, p):
    return 1 / (1 + math.exp(-(A + B * logit(p))))


A, B = fit(rows)
n = len(rows)
brier_raw = sum((p - y) ** 2 for p, y in rows) / n
brier_in = sum((pred(A, B, p) - y) ** 2 for p, y in rows) / n
loo = 0.0
for i, (p, y) in enumerate(rows):
    a, b = fit(rows[:i] + rows[i + 1:])
    loo += (pred(a, b, p) - y) ** 2
loo /= n
base = sum(y for _, y in rows) / n
brier_const = sum((base - y) ** 2 for _, y in rows) / n
bins = {}
for p, y in rows:
    k = round(p, 1)
    b = bins.setdefault(k, [0, 0])
    b[0] += 1; b[1] += y
out = {"shots": n, "hit_rate": round(base, 3), "mean_stated_p": round(sum(p for p, _ in rows) / n, 3),
       "A": round(A, 3), "B": round(B, 3),
       "map": {str(x): round(pred(A, B, x), 3) for x in (0.5, 0.6, 0.7, 0.8, 0.9)},
       "brier_stated": round(brier_raw, 4), "brier_platt_in_sample": round(brier_in, 4),
       "brier_platt_leave_one_out": round(loo, 4), "brier_constant_hit_rate": round(brier_const, 4),
       "gain_loo": round(brier_raw - loo, 4),
       "by_stated_p": {str(k): {"n": v[0], "hit_rate": round(v[1] / v[0], 3)} for k, v in sorted(bins.items())}}
(HERE / "results.json").write_text(json.dumps(out, indent=1))
print(json.dumps(out, indent=1))
