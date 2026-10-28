"""P-0242: Murphy decomposition of the called-shot Brier (BS = REL - RES + UNC).

Same rows as `probe.py shots`: items with a shot, status done and a verdict; hit = verdict == expect.
Grouped by the exact p values used, so the identity holds to rounding. A second grouping into
five bins shows how much binning would have hidden.
"""
import json
from collections import defaultdict

ST = '/Users/triton/PROTEUS/state/probes.json'
OUT = '/Users/triton/PROTEUS/experiments/2026-10-28-P-0242/results.json'
items = json.load(open(ST))['items']
rows = [(i['shot']['p'], 1 if i['verdict'] == i['shot']['expect'] else 0, i['shot']['expect'], i['id'])
        for i in items if i.get('shot') and i.get('status') == 'done' and i.get('verdict')]
N = len(rows)
obar = sum(h for _, h, _, _ in rows) / N
bs = sum((p - h) ** 2 for p, h, _, _ in rows) / N


def decompose(key):
    g = defaultdict(list)
    for p, h, e, _ in rows:
        g[key(p)].append((p, h))
    rel = res = within = 0.0
    table = []
    for k, v in sorted(g.items()):
        n = len(v)
        fk = sum(p for p, _ in v) / n
        ok = sum(h for _, h in v) / n
        rel += n * (fk - ok) ** 2
        res += n * (ok - obar) ** 2
        within += sum((p - fk) ** 2 for p, _ in v)
        table.append({'group': k, 'n': n, 'mean_p': round(fk, 3), 'hit_rate': round(ok, 3)})
    return {'REL': rel / N, 'RES': res / N, 'UNC': obar * (1 - obar), 'within_bin_var': within / N, 'table': table}


exact = decompose(lambda p: round(p, 2))
binned = decompose(lambda p: min(4, int(p * 5)) / 5)
for d in (exact, binned):
    d['REL-RES+UNC'] = d['REL'] - d['RES'] + d['UNC']
    d['residual'] = bs - d['REL-RES+UNC']

by_expect = defaultdict(lambda: [0, 0, 0.0])
for p, h, e, _ in rows:
    by_expect[e][0] += 1
    by_expect[e][1] += h
    by_expect[e][2] += p
res = {'N': N, 'hit_rate': obar, 'BS': bs, 'BS_always_base_rate': obar * (1 - obar),
       'BSS_vs_base_rate': 1 - bs / (obar * (1 - obar)),
       'exact': exact, 'five_bins': binned,
       'by_expect': {e: {'n': n, 'hits': h, 'mean_p': round(sp / n, 3)} for e, (n, h, sp) in by_expect.items()}}
json.dump(res, open(OUT, 'w'), indent=1)
show = {k: (round(v, 4) if isinstance(v, float) else v) for k, v in res.items() if k not in ('exact', 'five_bins')}
print(show)
for name in ('exact', 'five_bins'):
    d = res[name]
    print(name, {k: round(v, 4) for k, v in d.items() if k != 'table'})
    print('  ', d['table'])
