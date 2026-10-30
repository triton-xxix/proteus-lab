#!/usr/bin/env python3
"""D-018: called shots, second read at 80 scored. Reads state/probes.json the way probe.py shots
does (shot present, status done, verdict set), then splits the book at the D-012 read (first 65
scored, by verdict time) so the question "did the stated p move toward the hit rate" has a before
and an after. Nothing here changes a rule; the lines are PASS-MARKS.md "Called shots"."""
import json
import sys

PROBES = "/Users/triton/PROTEUS/state/probes.json"
KEEP, KILL, FLOOR_FINAL, D012_N = 0.160, 0.200, 80, 65


def stats(rows):
    hits = [1 if r["verdict"] == r["shot"]["expect"] else 0 for r in rows]
    n = len(rows)
    brier = sum((r["shot"]["p"] - h) ** 2 for r, h in zip(rows, hits)) / n
    mean_p = sum(r["shot"]["p"] for r in rows) / n
    hit = sum(hits) / n
    return n, hit, mean_p, brier


def main():
    st = json.load(open(PROBES))
    rows = [i for i in st["items"] if i.get("shot") and i.get("status") == "done" and i.get("verdict")]
    rows.sort(key=lambda i: (i.get("verdict_at") or "", i["id"]))
    n, hit, mean_p, brier = stats(rows)
    print("all: %d scored; hit rate %.2f; mean stated p %.2f; Brier %.3f" % (n, hit, mean_p, brier))
    if n < FLOOR_FINAL:
        sys.exit("under the 80 floor; D-018 is not due by count")
    verdict = "KEEP" if brier <= KEEP else "KILL"
    print("lines: KEEP at or below %.3f, KILL otherwise at %d or more -> %s" % (KEEP, FLOOR_FINAL, verdict))
    works = sum(1 for r in rows if r["verdict"] == "works") / n
    print("always-works baseline at this book: p %.2f, Brier %.3f" % (works, works * (1 - works)))
    a, b = rows[:D012_N], rows[D012_N:]
    for name, part in (("first %d (the D-012 slice)" % D012_N, a), ("the %d since" % len(b), b)):
        pn, ph, pp, pb = stats(part)
        print("%s: hit rate %.2f; mean stated p %.2f; gap %.2f; Brier %.3f" % (name, ph, pp, ph - pp, pb))
    _, ha, pa, _ = stats(a)
    _, hb, pb_, _ = stats(b)
    moved = abs(hb - pb_) < abs(ha - pa)
    print("stated p moved toward the hit rate since D-012: %s (gap %.2f -> %.2f)" % (
        "yes" if moved else "no", ha - pa, hb - pb_))
    for r in b:
        print("  %s %s p=%.2f -> %s %s" % (r["id"], r["shot"]["expect"], r["shot"]["p"], r["verdict"],
                                           "hit" if r["verdict"] == r["shot"]["expect"] else "MISS"))


if __name__ == "__main__":
    main()
