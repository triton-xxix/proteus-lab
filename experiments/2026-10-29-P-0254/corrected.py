"""P-0254: bias-corrected Murphy split of the called-shot Brier (Ferro and Fricker 2012).

Same rows and exact-p grouping as P-0242. With N rows, groups k of size n_k and hit rate o_k, overall o:
    REL' = REL - (1/N) sum_k n_k o_k (1 - o_k) / (n_k - 1)
    RES' = RES - (1/N) sum_k n_k o_k (1 - o_k) / (n_k - 1) + o (1 - o) / (N - 1)
    UNC' = N / (N - 1) o (1 - o)
REL' - RES' + UNC' = REL - RES + UNC, so the identity still closes. A group of one contributes 0.
Estimators written from memory: the Exeter PDF and its handle page returned empty (202) on 29 Oct.
Rows are taken up to P-0253; P-0254 itself is open.
"""
import json
from collections import defaultdict

ST = '/Users/triton/PROTEUS/state/probes.json'
OUT = '/Users/triton/PROTEUS/experiments/2026-10-29-P-0254/results.json'
items = json.load(open(ST))['items']
rows = [(i['shot']['p'], 1 if i['verdict'] == i['shot']['expect'] else 0, i['id'])
        for i in items if i.get('shot') and i.get('status') == 'done' and i.get('verdict')]
N = len(rows)
obar = sum(h for _, h, _ in rows) / N
bs = sum((p - h) ** 2 for p, h, _ in rows) / N


def decompose(key):
    g = defaultdict(list)
    for p, h, _ in rows:
        g[key(p)].append((p, h))
    rel = res = within = bias = 0.0
    for v in g.values():
        n = len(v)
        fk = sum(p for p, _ in v) / n
        ok = sum(h for _, h in v) / n
        rel += n * (fk - ok) ** 2
        res += n * (ok - obar) ** 2
        within += sum((p - fk) ** 2 for p, _ in v)
        if n > 1:
            bias += n * ok * (1 - ok) / (n - 1)
    rel, res, within, bias = rel / N, res / N, within / N, bias / N
    unc = obar * (1 - obar)
    d = {'groups': len(g), 'REL': rel, 'RES': res, 'UNC': unc, 'within_bin_var': within, 'bias_term': bias,
         'REL_corr': rel - bias, 'RES_corr': res - bias + unc / (N - 1), 'UNC_corr': N / (N - 1) * unc}
    d['check_uncorrected'] = rel - res + unc + within - bs
    d['check_corrected'] = d['REL_corr'] - d['RES_corr'] + d['UNC_corr'] + within - bs
    return d


res = {'N': N, 'hit_rate': obar, 'BS': bs, 'exact': decompose(lambda p: round(p, 2)),
       'five_bins': decompose(lambda p: min(4, int(p * 5)) / 5)}
json.dump(res, open(OUT, 'w'), indent=1)
print({k: round(v, 4) if isinstance(v, float) else v for k, v in res.items() if k not in ('exact', 'five_bins')})
for name in ('exact', 'five_bins'):
    print(name, {k: round(v, 4) if isinstance(v, float) else v for k, v in res[name].items()})
