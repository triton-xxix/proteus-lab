"""P-0297: are threatened birds named in fewer languages? Over the 11,064 species of huashu-bird-sticker's
data/species.json (sandbox/birdsticker, fetched for P-0288): languages per species = keys of `names` with a
non-empty value; threat = conservation.iucn (Wikidata P141). Per IUCN class: n, median and mean languages.
CR+EN v LC: median gap and a permutation test on the mean gap (5,000 shuffles); Spearman of language count
against the ordered scale LC < NT < VU < EN < CR; per-language coverage (which is thinnest); and the same
gap within each breeding region with 50 or more species, so a region effect cannot fake it.

    /Users/triton/PROTEUS/sandbox/py312-venv/bin/python3 -I experiments/2026-11-02-P-0297/names_v_threat.py
"""
import json
from collections import Counter, defaultdict

import numpy as np
from scipy.stats import spearmanr

d = json.load(open("/Users/triton/PROTEUS/sandbox/birdsticker/species.json"))
sp = d["species"]
ORDER = {"LC": 0, "NT": 1, "VU": 2, "EN": 3, "CR": 4}
rng = np.random.default_rng(20261102)

rows = []
lang_cov = Counter()
for s in sp:
    names = s.get("names") or {}
    langs = [k for k, v in names.items() if v]
    lang_cov.update(langs)
    iucn = ((s.get("conservation") or {}).get("iucn")) or "none"
    reg = (s.get("range") or {}).get("breedingRegion")
    reg = reg if isinstance(reg, str) else json.dumps(reg, ensure_ascii=False)[:40] if reg else "none"
    rows.append((len(langs), iucn, reg))

res = {"species": len(rows), "by_iucn": {}}
by = defaultdict(list)
for n, c, _ in rows:
    by[c].append(n)
for c, v in sorted(by.items(), key=lambda kv: -len(kv[1])):
    a = np.array(v)
    res["by_iucn"][c] = {"n": int(a.size), "median": float(np.median(a)), "mean": round(float(a.mean()), 2)}
    print(c, res["by_iucn"][c])

thr = np.array(by["CR"] + by["EN"])
lc = np.array(by["LC"])
obs = lc.mean() - thr.mean()
allv = np.concatenate([thr, lc]).astype(float)
perm = np.empty(5000)
for j in range(5000):
    rng.shuffle(allv)
    perm[j] = allv[thr.size:].mean() - allv[:thr.size].mean()
res["cr_en_v_lc"] = {"cr_en_n": int(thr.size), "lc_n": int(lc.size),
                     "median_gap": float(np.median(lc) - np.median(thr)), "mean_gap": round(float(obs), 2),
                     "perm_p_two_sided": round(float((np.abs(perm) >= abs(obs)).mean()), 4)}
ranked = [(ORDER[c], n) for n, c, _ in rows if c in ORDER]
rho, p = spearmanr([r for r, _ in ranked], [n for _, n in ranked])
res["spearman_threat_v_languages"] = {"n": len(ranked), "rho": round(float(rho), 3), "p": float(p)}
print("CR+EN v LC", res["cr_en_v_lc"], "spearman", res["spearman_threat_v_languages"])

res["language_coverage"] = {k: v for k, v in lang_cov.most_common()}
res["thinnest_languages"] = lang_cov.most_common()[-5:]
print("thinnest", res["thinnest_languages"], "fullest", lang_cov.most_common(3))

# within-region gap: regions with 50+ species and at least 5 CR+EN
reg_rows = defaultdict(lambda: {"t": [], "lc": []})
for n, c, r in rows:
    if c in ("CR", "EN"):
        reg_rows[r]["t"].append(n)
    elif c == "LC":
        reg_rows[r]["lc"].append(n)
within = {}
for r, v in reg_rows.items():
    if len(v["t"]) >= 5 and len(v["t"]) + len(v["lc"]) >= 50:
        within[r] = {"cr_en": len(v["t"]), "lc": len(v["lc"]),
                     "median_gap": float(np.median(v["lc"]) - np.median(v["t"])),
                     "mean_gap": round(float(np.mean(v["lc"]) - np.mean(v["t"])), 2)}
res["within_region"] = within
pos = sum(1 for w in within.values() if w["mean_gap"] > 0)
res["within_region_positive_gap"] = f"{pos} of {len(within)}"
print("regions", len(within), "with LC named in more languages:", pos)
json.dump(res, open("/Users/triton/PROTEUS/experiments/2026-11-02-P-0297/results.json", "w"), indent=1, ensure_ascii=False)
