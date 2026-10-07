#!/usr/bin/env python3
"""Validator for the Nolan site's data files. Standard library, Python 3.9 safe.

    check.py tenet                  the deep timeline: film.json, events.json, threads.json, images
    check.py film <digest.json>     a standard film digest (Workstream C), against films.json

Exit 1 on any FAIL. Prints FAIL lines, then WARN lines, then PASS or FAIL: n.
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
DIRECTIONS = {"forward", "inverted", "contested"}
STATUS = {"stated", "inferred", "contested", "unstated"}
QUOTE = re.compile(r'[“"]([^”"]{1,400})[”"]')
EM_DASH = "—"


def words(s):
    return len(s.split())


def scan_text(obj, path, fails, warns):
    """Shared text rules: no em dash, every quoted span under 15 words, at most one per field."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            scan_text(v, path + "." + k, fails, warns)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            scan_text(v, "%s[%d]" % (path, i), fails, warns)
    elif isinstance(obj, str):
        if EM_DASH in obj:
            fails.append("%s: em dash" % path)
        q = QUOTE.findall(obj)
        if len(q) > 1:
            fails.append("%s: %d quoted spans, at most one per field" % (path, len(q)))
        for span in q:
            if words(span) >= 15:
                fails.append("%s: quoted span of %d words (limit 14): %r" % (path, words(span), span[:60]))


def check_tenet():
    base = os.path.join(ROOT, "tenet")
    fails, warns = [], []
    film = json.load(open(os.path.join(base, "film.json")))
    ev = json.load(open(os.path.join(base, "events.json")))["events"]
    th = json.load(open(os.path.join(base, "threads.json")))["threads"]
    ids = [e["id"] for e in ev]
    if len(ids) != len(set(ids)):
        fails.append("events: duplicate ids")
    n = len(ev)
    if sorted(e["watch_order"] for e in ev) != list(range(1, n + 1)):
        fails.append("events: watch_order is not 1..%d" % n)
    if sorted(e["world_order"] for e in ev) != list(range(1, n + 1)):
        fails.append("events: world_order is not a permutation of 1..%d" % n)
    img_dir = os.path.join(base, "img")
    thread_ids = {t["id"] for t in th}
    for e in ev:
        p = "events." + e["id"]
        for k in ("title", "world_time", "location", "threads", "what_happens", "why_it_matters", "certainty", "sources"):
            if k not in e:
                fails.append("%s: missing %s" % (p, k))
        wt = e.get("world_time", {})
        if wt.get("status") not in STATUS:
            fails.append("%s: world_time.status %r" % (p, wt.get("status")))
        if wt.get("day") is not None and wt.get("status") != "stated":
            fails.append("%s: a day is set but status is %r; days are only allowed when stated" % (p, wt.get("status")))
        if e.get("certainty") not in STATUS:
            fails.append("%s: certainty %r" % (p, e.get("certainty")))
        if not e.get("sources"):
            fails.append("%s: no sources" % p)
        for t in e.get("threads", []):
            if t.get("who") not in thread_ids:
                fails.append("%s: unknown thread %r" % (p, t.get("who")))
            if t.get("direction") not in DIRECTIONS:
                fails.append("%s: direction %r" % (p, t.get("direction")))
        if e.get("image"):
            for suffix in (".jpg", "-800.jpg"):
                if not os.path.exists(os.path.join(img_dir, e["image"] + suffix)):
                    fails.append("%s: image file missing: %s%s" % (p, e["image"], suffix))
        if words(e.get("what_happens", "")) > 90:
            warns.append("%s: what_happens is %d words" % (p, words(e["what_happens"])))
    for t in th:
        for i, s in enumerate(t["segments"]):
            p = "threads.%s[%d]" % (t["id"], i)
            for k in ("from", "to"):
                if s.get(k) not in ids:
                    fails.append("%s: %s %r is not an event id" % (p, k, s.get(k)))
            if s.get("direction") not in DIRECTIONS:
                fails.append("%s: direction %r" % (p, s.get("direction")))
            if s.get("status") not in STATUS:
                fails.append("%s: status %r" % (p, s.get("status")))
    for k in ("anchor", "colour_code", "rules", "sator_square", "facts", "credit", "disclaimer"):
        if k not in film:
            fails.append("film.json: missing %s" % k)
    scan_text(film, "film", fails, warns)
    scan_text(ev, "events", fails, warns)
    scan_text(th, "threads", fails, warns)
    return fails, warns


KINDS = {"linear", "linear-with-flashbacks", "two-threads-converging", "interleaved-strands", "nested-levels",
         "parallel-timescales", "dilation", "inverted-crossing", "unverified"}


def check_film(path):
    """Workstream C: a standard film digest written by a research child."""
    fails, warns = [], []
    try:
        d = json.load(open(path))
    except Exception as e:
        return ["not valid JSON: %s" % e], []
    reg = json.load(open(os.path.join(ROOT, "films.json")))["films"]
    row = next((f for f in reg if f["slug"] == d.get("slug")), None)
    if row is None:
        fails.append("slug %r is not in films.json" % d.get("slug"))
    else:
        if d.get("title") != row["title"] or d.get("year") != row["year"]:
            fails.append("title/year do not match the register (%s, %s)" % (row["title"], row["year"]))
    for k in ("one_line", "facts", "time_structure", "themes", "inspirations", "collaborators", "reception", "missed", "sources"):
        if k not in d:
            fails.append("missing %s" % k)
    facts = d.get("facts", {})
    for k in ("release", "runtime_min", "writers", "dp", "editor", "composer", "budget_usd", "gross_usd", "cast_top5"):
        if k not in facts:
            fails.append("facts.%s missing" % k)
    cast = facts.get("cast_top5", {}).get("value", [])
    if len(cast) != 5:
        fails.append("facts.cast_top5 has %d entries, want 5" % len(cast))
    fetched = {s["url"] for s in d.get("sources", []) if s.get("fetched")}
    urls = [s.get("url") for s in d.get("sources", [])]
    if len(urls) != len(set(urls)):
        fails.append("sources: duplicate urls")
    sourced, unverified = 0, 0

    def walk(obj, path):
        nonlocal sourced, unverified
        if isinstance(obj, dict):
            if "source" in obj and ("value" in obj or "claim" in obj or "point" in obj or "scene" in obj):
                sourced += 1
                src = obj.get("source")
                if obj.get("unverified"):
                    unverified += 1
                elif not (isinstance(src, str) and src.startswith("http") and src in fetched):
                    fails.append("%s: source %r was not fetched (or mark unverified: true)" % (path, src))
            for k, v in obj.items():
                walk(v, path + "." + k)
        elif isinstance(obj, list):
            for i, v in enumerate(obj):
                walk(v, "%s[%d]" % (path, i))
    walk({k: v for k, v in d.items() if k != "sources"}, "digest")
    if sourced:
        share = unverified / float(sourced)
        if share > 0.5 and d.get("slug") != "the-odyssey":
            fails.append("%d of %d sourced fields unverified (%.0f%%, limit 50%%)" % (unverified, sourced, 100 * share))
        elif share > 0.25:
            warns.append("%d of %d sourced fields unverified (%.0f%%)" % (unverified, sourced, 100 * share))
    ts = d.get("time_structure", {})
    if ts.get("kind") not in KINDS:
        fails.append("time_structure.kind %r not in vocabulary" % ts.get("kind"))
    elif row and ts.get("kind") != row.get("time_structure_kind"):
        warns.append("time_structure.kind %r differs from the register's prior %r" % (ts.get("kind"), row.get("time_structure_kind")))
    sk = ts.get("sketch", {})
    tids = set()
    for i, t in enumerate(sk.get("threads", [])):
        tids.add(t.get("id"))
        if t.get("direction") not in ("forward", "backward", "static"):
            fails.append("sketch.threads[%d].direction %r" % (i, t.get("direction")))
        if not (isinstance(t.get("level"), int) and t["level"] >= 0):
            fails.append("sketch.threads[%d].level" % i)
        if not (isinstance(t.get("rate"), (int, float)) and t["rate"] > 0):
            fails.append("sketch.threads[%d].rate" % i)
        sp = t.get("span", [])
        if not (len(sp) == 2 and 0 <= sp[0] <= sp[1] <= 1):
            fails.append("sketch.threads[%d].span" % i)
    if not tids:
        fails.append("sketch has no threads")
    for i, j in enumerate(sk.get("joins", [])):
        if j.get("from") not in tids or j.get("to") not in tids:
            fails.append("sketch.joins[%d] references an unknown thread" % i)
    themes = d.get("themes", [])
    if not 3 <= len(themes) <= 6:
        fails.append("%d themes, want 3 to 6" % len(themes))
    vocab = {t["id"] for t in json.load(open(os.path.join(ROOT, "themes.json")))["themes"]}
    for i, t in enumerate(themes):
        w = words(t.get("scene", ""))
        if not 20 <= w <= 80:
            fails.append("themes[%d].scene is %d words, want 20 to 80" % (i, w))
        if t.get("id") not in vocab and not t.get("new"):
            fails.append("themes[%d].id %r not in themes.json and not marked new" % (i, t.get("id")))
        elif t.get("new"):
            warns.append("themes[%d] proposes a new theme %r" % (i, t.get("id")))
    if len(d.get("inspirations", [])) < 2:
        fails.append("fewer than 2 inspirations")
    if len(d.get("missed", [])) != 3:
        fails.append("%d missed items, want exactly 3" % len(d.get("missed", [])))
    for i, im in enumerate(d.get("images", [])):
        for k in ("url", "caption", "source"):
            if not im.get(k):
                fails.append("images[%d].%s missing" % (i, k))
    blob = json.dumps({k: v for k, v in d.items() if k != "images"})
    if re.search(r"<img|\.jpe?g|\.png|\.webp|\.gif", blob, re.I):
        fails.append("image reference outside images[]")
    if "Luke" in blob:
        fails.append("names Luke")
    scan_text(d, "digest", fails, warns)
    return fails, warns


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in ("tenet", "film"):
        print(__doc__)
        sys.exit(2)
    if sys.argv[1] == "tenet":
        fails, warns = check_tenet()
    else:
        fails, warns = check_film(sys.argv[2])
    for f in fails:
        print("FAIL:", f)
    for w in warns:
        print("WARN:", w)
    print("PASS" if not fails else "FAIL: %d" % len(fails), "(%d warn)" % len(warns))
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
