#!/usr/bin/env python3
"""P-0332's first-link rule on German Wikipedia. Parser imported unchanged, so the rule is the same one.

Polite and bounded: 0.3 s between fetches, backs off on 429, stops at 15 minutes and writes whatever it has.
Usage: python3 de_walk.py N
"""
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter
from pathlib import Path

sys.path.insert(0, "/Users/triton/PROTEUS/experiments/2026-11-05-P-0332")
from walk_rule import FirstLink  # noqa: E402

HERE = Path(__file__).resolve().parent
UA = "ProteusLab-philosophy-walk/1.0 (https://github.com/triton-xxix; one-off research script)"
HOST = "de.wikipedia.org"
TARGET = "Philosophie"
BUDGET = 900
START = time.time()
CACHE = {}
refusals = 0


class OutOfTime(Exception):
    pass


def get(url):
    global refusals
    for wait in (5, 20, 60):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.read().decode("utf-8")
        except urllib.error.HTTPError as e:
            if e.code != 429:
                raise
            refusals += 1
            time.sleep(wait)
    raise OutOfTime("429 three times running")


def page(title):
    if title in CACHE:
        return CACHE[title]
    if time.time() - START > BUDGET:
        raise OutOfTime("budget")
    url = f"https://{HOST}/api/rest_v1/page/html/" + urllib.parse.quote(title.replace(" ", "_"), safe="")
    try:
        html = get(url)
    except OutOfTime:
        raise
    except Exception as e:
        CACHE[title] = (title, None, str(e)[:80])
        return CACHE[title]
    canon = title
    marker = f'<link rel="dc:isVersionOf" href="//{HOST}/wiki/'
    k = html.find(marker)
    if k >= 0:
        canon = urllib.parse.unquote(html[k + len(marker): html.find('"', k + len(marker))]).replace("_", " ")
    p = FirstLink()
    p.feed(html)
    CACHE[title] = (canon, p.found, None)
    time.sleep(0.3)
    return CACHE[title]


def walk(start):
    path, seen, t = [], set(), start
    for _ in range(60):
        canon, nxt, err = page(t)
        path.append(canon)
        if canon == TARGET:
            return "philosophy", path
        if canon in seen:
            return "loop", path
        seen.add(canon)
        if err or not nxt:
            return ("fetch error" if err else "dead end"), path
        t = nxt
    return "too long", path


def main():
    n = int(sys.argv[1])
    q = json.loads(get(f"https://{HOST}/w/api.php?action=query&list=random&rnnamespace=0&rnlimit={n}&format=json"))
    starts = [r["title"] for r in q["query"]["random"]]
    rows, stopped = [], None
    for s in starts:
        try:
            outcome, path = walk(s)
        except OutOfTime as e:
            stopped = str(e)
            break
        rows.append({"start": s, "outcome": outcome, "hops": len(path) - 1, "path": path})
        print(f"{outcome:11s} {len(path)-1:3d}  {s} -> {path[-1]}", flush=True)

    reached = [r for r in rows if r["outcome"] == "philosophy"]
    hops = sorted(r["hops"] for r in reached)
    rings = Counter()
    for r in rows:
        if r["outcome"] == "loop":
            cycle = r["path"][r["path"].index(r["path"][-1]):-1]
            i = cycle.index(min(cycle))
            rings[" > ".join(cycle[i:] + cycle[:i])] += 1
    dead = Counter(r["path"][-1] for r in rows if r["outcome"] == "dead end")
    out = {
        "at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "asked": n, "walked": len(rows), "stopped_early": stopped, "pages_fetched": len(CACHE), "refusals_429": refusals,
        "secs": round(time.time() - START),
        "outcomes": dict(Counter(r["outcome"] for r in rows)),
        "reached": len(reached), "median_hops": hops[len(hops) // 2] if hops else None,
        "rings": rings.most_common(8), "dead_ends": dead.most_common(12),
        "last_step": Counter(r["path"][-2] for r in reached if len(r["path"]) > 1).most_common(5),
        "fetch_error_titles": [k for k, v in CACHE.items() if v[2]][:10],
        "rows": rows,
    }
    (HERE / "walks.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))
    print(json.dumps({k: v for k, v in out.items() if k != "rows"}, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
