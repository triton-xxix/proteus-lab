"""Replay the first-link rule on Wikipedia as it stood on past dates (P-0332).

For each date, each title resolves to its latest revision at or before that date, and redirects are
followed as they stood then, not as they stand now. The rule is the parser from the 5 Nov walk, copied
into this folder as walk_rule.py. Starts: Science, Knowledge, Belief, then the 100 random titles of
experiments/2026-11-05-philosophy/walks.json. A title with no revision by that date is counted as absent.

Old wikitext renders through today's templates, so a template that has since changed can move a link.

Usage: python3 ringdate.py OUTDIR WALL_SECONDS
"""
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
from collections import Counter
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from walk_rule import FirstLink, UA

DATES = ["2011-07-01", "2014-07-01", "2016-07-01", "2018-07-01", "2021-07-01", "2026-11-05"]
ROOT = "/Users/triton/PROTEUS/experiments/2026-11-05-philosophy/walks.json"
FIXED = ["Science", "Knowledge", "Belief"]
REDIRECT = re.compile(r'<link rel="mw:PageProp/redirect" href="\./([^"#]+)')
calls = 0


def get(url):
    global calls
    calls += 1
    for attempt in range(6):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.read().decode("utf-8")
        except urllib.error.HTTPError as e:
            if e.code == 429:
                time.sleep(5 * (attempt + 1))
                continue
            if e.code >= 500 and attempt < 2:
                time.sleep(2)
                continue
            raise
        except OSError:
            if attempt < 2:
                time.sleep(2)
                continue
            raise
    raise RuntimeError("retries spent " + url)


def revid_at(title, date):
    q = urllib.parse.urlencode({"action": "query", "prop": "revisions", "titles": title, "rvlimit": 1,
                                "rvstart": date + "T23:59:59Z", "rvdir": "older", "rvprop": "ids",
                                "format": "json"})
    pages = json.loads(get("https://en.wikipedia.org/w/api.php?" + q))["query"]["pages"]
    for p in pages.values():
        revs = p.get("revisions")
        if revs:
            return revs[0]["revid"]
    # No history under this title on this date. A later page move leaves a redirect here whose own
    # history starts after the move, while the article's old revisions went with it. Follow today's
    # redirect and read the target's history. First run without this: 13 of 39 dead ends in 2011 were
    # 'Social sciences', a false stop.
    moved_from = title
    q = urllib.parse.urlencode({"action": "query", "prop": "revisions", "titles": moved_from, "redirects": 1,
                                "rvlimit": 1, "rvstart": date + "T23:59:59Z", "rvdir": "older", "rvprop": "ids",
                                "format": "json"})
    pages = json.loads(get("https://en.wikipedia.org/w/api.php?" + q))["query"]["pages"]
    for p in pages.values():
        revs = p.get("revisions")
        if revs:
            return revs[0]["revid"]
    return None


def html_of(title, rev):
    u = "https://en.wikipedia.org/api/rest_v1/page/html/%s/%d" % (urllib.parse.quote(title.replace(" ", "_"), safe=""), rev)
    return get(u)


def step(title, date, cache):
    """Return (canonical title, next title, note) for a title on a date."""
    if title in cache:
        return cache[title]
    canon, seen = title, set()
    # Note: redirect-followed titles keep the name they were linked by, so one page can appear under two
    # names and a ring can read one hop longer. The outcome is unaffected.
    result = None
    for _ in range(4):
        if canon in seen:
            result = (canon, None, "redirect loop")
            break
        seen.add(canon)
        try:
            rev = revid_at(canon, date)
            if rev is None:
                result = (canon, None, "absent")
                break
            html = html_of(canon, rev)
        except Exception as e:
            result = (canon, None, "error " + str(e)[:60])
            break
        m = REDIRECT.search(html)
        if m:
            canon = urllib.parse.unquote(m.group(1)).replace("_", " ")
            continue
        p = FirstLink()
        p.feed(html)
        result = (canon, p.found, None)
        break
    if result is None:
        result = (canon, None, "redirect chain")
    if not (result[2] or "").startswith("error"):
        cache[title] = result
    return result


def walk(start, date, cache):
    path, seen = [], set()
    t = start
    for _ in range(60):
        canon, nxt, note = step(t, date, cache)
        if note == "absent" and not path:
            return "absent", [start]
        path.append(canon)
        if canon == "Philosophy":
            return "philosophy", path
        if canon in seen:
            return "loop", path
        seen.add(canon)
        if note and note.startswith("error"):
            return "error", path
        if not nxt:
            return "dead end", path
        t = nxt
    return "too long", path


def ring_of(path):
    """The cycle at the end of a looping path."""
    last = path[-1]
    i = path.index(last)
    return path[i:-1]


def main():
    out, wall = sys.argv[1], float(sys.argv[2])
    t0 = time.time()
    with open(ROOT) as fh:
        sample = [r["start"] for r in json.load(fh)["rows"]]
    results = {"dates": {}, "sample_n": len(sample), "complete": True}
    # Oldest first would spend the wall on old years only, so take the fixed starts for every date, then
    # the sample a date at a time.
    caches = {d: {} for d in DATES}
    for d in DATES:
        results["dates"][d] = {"fixed": {}, "rows": []}
        for s in FIXED:
            outcome, path = walk(s, d, caches[d])
            results["dates"][d]["fixed"][s] = {"outcome": outcome, "path": path}
            print(d, s, outcome, " > ".join(path), flush=True)
    def one(args):
        s, d = args
        if time.time() - t0 > wall:
            return None
        outcome, path = walk(s, d, caches[d])
        return {"start": s, "outcome": outcome, "hops": len(path) - 1, "path": path}

    for d in DATES:
        with ThreadPoolExecutor(6) as pool:
            got = list(pool.map(one, [(s, d) for s in sample]))
        results["dates"][d]["rows"] = [g for g in got if g]
        if len(results["dates"][d]["rows"]) < len(sample):
            results["complete"] = False
            results["stopped"] = "%s at %d of %d" % (d, len(results["dates"][d]["rows"]), len(sample))
        rows = results["dates"][d]["rows"]
        c = Counter(r["outcome"] for r in rows)
        rings = Counter(" > ".join(sorted(ring_of(r["path"]))) for r in rows if r["outcome"] == "loop")
        results["dates"][d]["counts"] = dict(c)
        results["dates"][d]["rings"] = rings.most_common(5)
        results["dates"][d]["pages"] = len(caches[d])
        present = len(rows) - c.get("absent", 0)
        print(d, "rows", len(rows), "present", present, dict(c), "top ring", rings.most_common(1), "calls", calls,
              "secs", round(time.time() - t0), flush=True)
        results["calls"] = calls
        results["secs"] = round(time.time() - t0)
        with open(os.path.join(out, "results.json"), "w") as fh:
            json.dump(results, fh, indent=1)
        if not results["complete"]:
            break
    print("done", results["complete"], results.get("stopped", ""), "calls", calls, flush=True)


if __name__ == "__main__":
    main()
