"""Scores the blind sheet against RULE.md and writes flag-test.json.
python3 score.py <sheetdir> <dump.jsonl>
Reads sheet.jsonl, key.jsonl and marks-child.jsonl from <sheetdir>, marks-me.json from this folder."""
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import digest as D  # noqa: E402

sheetdir, dumpfile = sys.argv[1], sys.argv[2]


def rows(name):
    return [json.loads(x) for x in open(os.path.join(sheetdir, name))]


sheet = {r["id"]: r for r in rows("sheet.jsonl")}
key = {r["id"]: r for r in rows("key.jsonl")}
child = {r["id"]: r["mark"] for r in rows("marks-child.jsonl")}
ones = set(json.load(open(os.path.join(HERE, "marks-me.json")))["checkable_ids"])
me = {i: int(i in ones) for i in sheet}
if set(child) != set(sheet) or set(key) != set(sheet):
    sys.exit("ids disagree: sheet %d key %d child %d" % (len(sheet), len(key), len(child)))
pop = {"flagged": 0, "cut": 0, "below": 0}
for line in open(dumpfile):
    r = json.loads(line)
    pop["flagged" if r["flagged"] else "cut" if r["score"] >= 3 else "below"] += 1


def wilson(k, n, z=1.96):
    if not n:
        return [0, 0]
    p = k / n
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return [round(max(0, (c - h) / d), 3), round(min(1, (c + h) / d), 3)]


def verdict(f, b):
    if f >= 0.5 and f >= 2 * b:
        return "earns its place"
    if f < 0.3 or (b > 0 and f <= 1.2 * b):
        return "goes"
    return "needs work"


strata = {}
for s in pop:
    ids = [i for i in sheet if key[i]["stratum"] == s]
    n = len(ids)
    km, kc = sum(me[i] for i in ids), sum(child[i] for i in ids)
    strata[s] = {"population": pop[s], "n": n, "me": km, "child": kc, "rate_me": round(km / n, 3),
                 "rate_child": round(kc / n, 3), "ci_me": wilson(km, n), "ci_child": wilson(kc, n)}

vm = verdict(strata["flagged"]["rate_me"], strata["below"]["rate_me"])
vc = verdict(strata["flagged"]["rate_child"], strata["below"]["rate_child"])
order = ["goes", "needs work", "earns its place"]
final = min(vm, vc, key=order.index)

N = len(sheet)
agree = sum(me[i] == child[i] for i in sheet)
pm, pc = sum(me.values()) / N, sum(child.values()) / N
pe = pm * pc + (1 - pm) * (1 - pc)
kappa = round((agree / N - pe) / (1 - pe), 3) if pe < 1 else None


def reach(who):
    est = {s: strata[s]["population"] * strata[s]["rate_" + who] for s in pop}
    tot = sum(est.values())
    return {"estimated_checkable": round(tot), "by_stratum": {s: round(v, 1) for s, v in est.items()},
            "share_flagged": round(est["flagged"] / tot, 3), "share_score3": round((est["flagged"] + est["cut"]) / tot, 3)}


def feats(t):
    return {"a percentage": bool(D.PCT.search(t)), "another number": bool([x for x in D.NUM.findall(t) if not D.YEAR.fullmatch(x)]) and not D.PCT.search(t),
            "a comparison word": bool(D.COMPARE.search(t)), "an absolute word": bool(D.ABSOLUTE.search(t))}


feature = []
for name in ["a percentage", "another number", "a comparison word", "an absolute word"]:
    ids = [i for i in sheet if feats(sheet[i]["text"])[name]]
    feature.append({"feature": name, "n": len(ids), "me": sum(me[i] for i in ids), "child": sum(child[i] for i in ids)})
none = [i for i in sheet if not any(feats(sheet[i]["text"]).values())]
feature.append({"feature": "none of them", "n": len(none), "me": sum(me[i] for i in none), "child": sum(child[i] for i in none)})

flagged_lines = sorted([{"id": i, "video": key[i]["video"], "t": key[i]["t"], "score": key[i]["score"], "text": sheet[i]["text"],
                         "me": me[i], "child": child[i]} for i in sheet if key[i]["stratum"] == "flagged"],
                       key=lambda x: (-x["me"], -x["child"], x["id"]))
marks = [{"id": i, "stratum": key[i]["stratum"], "score": key[i]["score"], "video": key[i]["video"], "t": key[i]["t"],
          "me": me[i], "child": child[i]} for i in sorted(sheet)]
out = {"called": {"flagged": 0.45, "cut": 0.35, "below": 0.12, "verdict": "needs work"}, "strata": strata,
       "verdict_me": vm, "verdict_child": vc, "verdict": final, "agree": agree, "n": N, "kappa": kappa,
       "reach_me": reach("me"), "reach_child": reach("child"), "feature": feature, "flagged_lines": flagged_lines, "marks": marks}
json.dump(out, open(os.path.join(HERE, "flag-test.json"), "w"), indent=1)
print(json.dumps({k: out[k] for k in ("strata", "verdict_me", "verdict_child", "verdict", "agree", "n", "kappa", "reach_me", "reach_child", "feature")}, indent=1))
