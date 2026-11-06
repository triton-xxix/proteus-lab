#!/usr/bin/env python3
"""Build docs/probes/numbers/data.json from shots-input.jsonl and scores.jsonl (Workshop, 6 Nov 2026).

Scores come from a reader applying RULE.md, not from this script. This script only validates and counts.
Exits non-zero if ids differ, a score is malformed, or the verdict-word totals differ from
docs/probes/shots/data.json on the same ids. A snapshot: new shots are not scored until someone reads them.
"""
import json
import os
import sys

HERE = "/Users/triton/PROTEUS/docs/probes/numbers"
SHOTS = "/Users/triton/PROTEUS/docs/probes/shots/data.json"
SCORES = ("hit", "partial", "miss", "unscored")
BINS = [(0.0, 0.6, "under 60%"), (0.6, 0.7, "60 to 65%"), (0.7, 0.8, "70 to 75%"), (0.8, 1.01, "80% and up")]
TOLS = [0.10, 0.25, 0.50, 1.00]
AUDITED = 32  # rows I read against the source after the reader finished: chosen for looking wrong or mattering, not at random


def load(name):
    return [json.loads(l) for l in open(os.path.join(HERE, name)) if l.strip()]


def tally(rows):
    c = {k: sum(1 for r in rows if r["score"] == k) for k in SCORES}
    c["n"] = len(rows)
    c["scored"] = len(rows) - c["unscored"]
    c["hit_rate"] = round(c["hit"] / c["scored"], 3) if c["scored"] else None
    return c


def main():
    shots = load("shots-input.jsonl")
    raw = load("scores-raw.jsonl")
    corrections = json.load(open(os.path.join(HERE, "corrections.json")))
    if set(corrections) - {r["id"] for r in raw}:
        sys.exit("numbers: correction for an unknown id")
    merged = [dict(r, **corrections.get(r["id"], {}).get("set", {})) for r in raw]
    with open(os.path.join(HERE, "scores.jsonl"), "w") as f:
        for r in merged:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    scores = {r["id"]: r for r in merged}
    if set(scores) != {s["id"] for s in shots}:
        sys.exit("numbers: ids differ: %s" % sorted(set(scores) ^ {s["id"] for s in shots}))
    rows = []
    for s in shots:
        c = scores[s["id"]]
        if c["score"] not in SCORES:
            sys.exit("numbers: bad score on %s: %r" % (s["id"], c["score"]))
        cl, he = c.get("claims"), c.get("held")
        if not isinstance(cl, int) or not isinstance(he, int) or cl < 1 or he < 0 or he > cl:
            sys.exit("numbers: bad claims/held on %s: %r %r" % (s["id"], cl, he))
        want = {"hit": he == cl, "miss": he == 0, "unscored": he == 0, "partial": 0 < he < cl}[c["score"]]
        if not want:
            sys.exit("numbers: %s scored %s with %d of %d claims held" % (s["id"], c["score"], he, cl))
        said, got = c.get("said"), c.get("got")
        if (said is None) != (got is None):
            sys.exit("numbers: %s has said without got" % s["id"])
        rows.append({
            "id": s["id"], "title": s["title"], "at": s["at"][:10], "p": s["p"], "expect": s["expect"],
            "verdict": s["verdict"], "word": 1 if s["expect"] == s["verdict"] else 0, "number": s["number"],
            "score": c["score"], "claims": cl, "held": he, "said": said, "got": got, "unit": c.get("unit"),
            "reason": c.get("reason", ""),
        })
    rows.sort(key=lambda r: r["at"])
    # the word totals must agree with the called-shots page on these ids
    book = {r["id"]: r for r in json.load(open(SHOTS))["rows"]}
    for r in rows:
        if r["id"] not in book or book[r["id"]]["hit"] != r["word"]:
            sys.exit("numbers: word score for %s differs from the called-shots page" % r["id"])
    word_hits = sum(r["word"] for r in rows)
    pairs = [r for r in rows if r["said"] not in (None, 0) and r["got"] is not None]
    same_sign = [r for r in pairs if r["said"] * r["got"] > 0]
    tol = [{"tol": t, "within": sum(1 for r in pairs if abs(r["got"] - r["said"]) / abs(r["said"]) <= t)} for t in TOLS]
    bins = []
    for lo, hi, label in BINS:
        b = [r for r in rows if lo <= r["p"] < hi]
        if b:
            t = tally(b)
            t["label"] = label
            t["mean_p"] = round(sum(r["p"] for r in b) / len(b), 3)
            t["word_rate"] = round(sum(r["word"] for r in b) / len(b), 3)
            bins.append(t)
    months = []
    # four equal slices in call order, so "am I improving" has the same n each side
    k = len(rows) / 4
    for i in range(4):
        sl = rows[int(i * k):int((i + 1) * k)]
        t = tally(sl)
        t["label"] = "%s to %s" % (sl[0]["at"], sl[-1]["at"])
        t["word_rate"] = round(sum(r["word"] for r in sl) / len(sl), 3)
        months.append(t)
    multi = [r for r in rows if r["claims"] > 1 and r["score"] != "unscored"]
    single = [r for r in rows if r["claims"] == 1 and r["score"] != "unscored"]
    summary = tally(rows)
    summary.update({
        "word_hits": word_hits, "word_rate": round(word_hits / len(rows), 3), "mean_p": round(sum(r["p"] for r in rows) / len(rows), 3),
        "word_and_hit": sum(1 for r in rows if r["word"] and r["score"] == "hit"),
        "word_and_miss": sum(1 for r in rows if r["word"] and r["score"] == "miss"),
        "word_and_partial": sum(1 for r in rows if r["word"] and r["score"] == "partial"),
        "word_and_unscored": sum(1 for r in rows if r["word"] and r["score"] == "unscored"),
        "partial_half_rate": round((summary["hit"] + summary["partial"] / 2) / summary["scored"], 3),
        "single": tally(single), "multi": tally(multi),
        "pairs": len(pairs), "same_sign": len(same_sign),
        "got_bigger": sum(1 for r in same_sign if abs(r["got"]) > abs(r["said"])),
        "got_smaller": sum(1 for r in same_sign if abs(r["got"]) < abs(r["said"])),
        "got_equal": sum(1 for r in same_sign if abs(r["got"]) == abs(r["said"])),
        "first": rows[0]["at"], "last": rows[-1]["at"], "last_id": max(r["id"] for r in rows),
        "audited": AUDITED,
        "score_corrections": sum(1 for c in corrections.values() if "score" in c["set"]),
        "pair_corrections": sum(1 for c in corrections.values() if "score" not in c["set"]),
    })
    with open(os.path.join(HERE, "data.json"), "w") as f:
        json.dump({"summary": summary, "bins": bins, "slices": months, "tol": tol, "rows": rows}, f, indent=1, ensure_ascii=False)
    print("numbers: %d shots; word %d of %d; number hit %d partial %d miss %d unscored %d, rate %.3f; %d said-got pairs"
          % (len(rows), word_hits, len(rows), summary["hit"], summary["partial"], summary["miss"], summary["unscored"], summary["hit_rate"], len(pairs)))


if __name__ == "__main__":
    main()
