"""P-0360: P-0339's read-or-not measure on the German (P-0344) and French (P-0359) walks.
Spearman of October 2026 views against walks through each page, share of steps on pages under
1,000 October views, and the ring pages' views. Edition size differs, so views are also given as a
share of the target page's own October views.
Usage: python3 -I views.py
"""
import glob
import json
import statistics
from collections import Counter

SETS = {
    "de": ("/Users/triton/PROTEUS/experiments/2026-11-06-P-0344/walks.json", "/Users/triton/PROTEUS/sandbox/p0360/de", "Philosophie"),
    "fr": ("/Users/triton/PROTEUS/experiments/2026-11-07-P-0359/walks.json", "/Users/triton/PROTEUS/sandbox/p0360/fr", "Philosophie"),
}


def ranks(xs):
    order = sorted(range(len(xs)), key=lambda i: xs[i])
    out_r = [0.0] * len(xs)
    i = 0
    while i < len(xs):
        j = i
        while j + 1 < len(xs) and xs[order[j + 1]] == xs[order[i]]:
            j += 1
        for k in range(i, j + 1):
            out_r[order[k]] = (i + j) / 2
        i = j + 1
    return out_r


def spearman(a, b):
    ra, rb = ranks(a), ranks(b)
    ma, mb = statistics.mean(ra), statistics.mean(rb)
    num = sum((x - ma) * (y - mb) for x, y in zip(ra, rb))
    den = (sum((x - ma) ** 2 for x in ra) * sum((y - mb) ** 2 for y in rb)) ** 0.5
    return num / den if den else None


res = {}
for lang, (walks_file, d, target) in SETS.items():
    rows = json.load(open(walks_file))["rows"]
    through, visits = Counter(), Counter()
    for r in rows:
        path = r.get("path") or []
        for p in set(path[1:]):
            through[p] += 1
        visits.update(path[1:])
    v, conts, calls, missing = {}, 0, 0, []
    for f in sorted(glob.glob(d + "/batch*.json")) + sorted(glob.glob(d + "/small*.json")):
        calls += 1
        try:
            data = json.load(open(f))
        except ValueError:  # Wikimedia's "too many requests" text, not JSON
            missing.append("REFUSED " + f.rsplit("/", 1)[-1])
            continue
        conts += "continue" in data
        norm = {x["to"]: x["from"] for x in data.get("query", {}).get("normalized", [])}
        for p in data.get("query", {}).get("pages", []):
            t = norm.get(p["title"], p["title"])
            if p.get("missing"):
                missing.append(t)
                continue
            pv = p.get("pageviews")
            if not pv:
                continue
            octo = {k: n for k, n in pv.items() if k.startswith("2026-10-")}
            if len(octo) < 31:
                continue
            v[t] = sum(n or 0 for n in octo.values())
    pages = sorted(p for p in v if p in through)
    xs, ys = [v[p] for p in pages], [through[p] for p in pages]
    tot = sum(visits[p] for p in pages)
    low = sum(visits[p] for p in pages if v[p] < 1000)
    multi = [p for p in pages if through[p] >= 2]
    tv = v.get(target)
    top = sorted(multi, key=lambda p: -through[p])[:12]
    res[lang] = {
        "walk_pages": len(through), "views_found": len(pages), "calls": calls, "batches_with_continue": conts,
        "missing": missing[:10],
        "spearman_all": round(spearman(xs, ys), 3),
        "spearman_2plus": round(spearman([v[p] for p in multi], [through[p] for p in multi]), 3),
        "pages_2plus": len(multi),
        "share_steps_under_1000": round(low / tot, 4) if tot else None,
        "share_pages_under_1000": round(sum(n < 1000 for n in xs) / len(xs), 4),
        "median_views": statistics.median(xs),
        "target_october_views": tv,
        "median_views_over_target": round(statistics.median(xs) / tv, 4) if tv else None,
        "busiest_shared_pages": [{"page": p, "walks": through[p], "oct_views": v[p]} for p in top],
        "least_read_2plus": [{"page": p, "walks": through[p], "oct_views": v[p]} for p in sorted(multi, key=lambda p: v[p])[:6]],
    }
json.dump(res, open("/Users/triton/PROTEUS/experiments/2026-11-07-P-0360/results.json", "w"), indent=1, ensure_ascii=False)
print(json.dumps(res, indent=1, ensure_ascii=False))
