"""first_link.py: follow the first link of Wikipedia articles and see where they end.

The "getting to Philosophy" game, as one standard-library file that keeps its paths, so the same
starts can be walked again later and the changes named.

  python3 first_link.py "Banana"                         walk one article, print the path
  python3 first_link.py --random 100 --out walks.json    walk 100 random articles, save every path
  python3 first_link.py --recheck walks.json --out again.json
                                                         walk the same starts again; say which paths
                                                         changed and at which page they first part

Rule: the first link in the lead paragraphs that is not inside parentheses, not in italics, not in a
hatnote, infobox, table, figure or footnote, and points to another article. A walk stops on
Philosophy, on a page it has already visited (loop), on a page with no such link or that does not
exist (dead end), or after 60 hops. English Wikipedia's REST HTML, no key. Fetch errors other than
404 are retried twice and reported, never counted quietly as dead ends.
"""
import argparse
import json
import sys
import time
import urllib.parse
import urllib.request
from collections import Counter
from html.parser import HTMLParser

UA = "proteus-first-link/1.0 (https://triton-xxix.github.io/proteus-lab/tools/first-link/)"
TARGET = "Philosophy"
MAX_HOPS = 60
CACHE = {}


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8")


class FirstLink(HTMLParser):
    """The parser from the 5 Nov 2026 walk, unchanged, so old paths stay comparable."""

    def __init__(self):
        super().__init__()
        self.stack = []  # (tag, skipping)
        self.in_p = 0
        self.paren = 0
        self.italic = 0
        self.skip = 0
        self.found = None
        self.in_section0 = True
        self.section_depth = 0

    def handle_starttag(self, tag, attrs):
        if self.found:
            return
        a = dict(attrs)
        cls = a.get("class", "") or ""
        skip_this = False
        if tag in ("table", "sup", "style", "figure", "math", "small"):
            skip_this = True
        if tag in ("div", "span") and any(k in cls for k in ("hatnote", "infobox", "navbox", "thumb", "mw-ref", "reference", "noprint", "IPA", "rt-commentedText", "nowrap")):
            skip_this = True
        if a.get("role") == "note" or a.get("typeof", "").startswith("mw:Transclusion") and tag in ("div", "table"):
            skip_this = True
        if tag == "section":
            self.section_depth += 1
            if self.section_depth == 1 and a.get("data-mw-section-id") not in (None, "0"):
                self.in_section0 = False
        self.stack.append((tag, skip_this))
        if skip_this:
            self.skip += 1
        if tag in ("i", "em"):
            self.italic += 1
        if tag == "p":
            self.in_p += 1
        if tag == "a" and self.in_p and not self.skip and not self.italic and self.paren == 0 and self.in_section0:
            href = a.get("href", "")
            rel = a.get("rel", "")
            if href.startswith("./") and "mw:WikiLink" in rel:
                title = urllib.parse.unquote(href[2:].split("#")[0])
                if ":" not in title and title:
                    self.found = title.replace("_", " ")

    def handle_endtag(self, tag):
        if self.found:
            return
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                for t, s in self.stack[i:]:
                    if s:
                        self.skip -= 1
                    if t in ("i", "em"):
                        self.italic -= 1
                    if t == "p":
                        self.in_p -= 1
                        self.paren = 0
                    if t == "section":
                        self.section_depth -= 1
                del self.stack[i:]
                break

    def handle_data(self, data):
        if self.found or not self.in_p or self.skip:
            return
        for ch in data:
            if ch == "(":
                self.paren += 1
            elif ch == ")" and self.paren > 0:
                self.paren -= 1


def first_link(html):
    p = FirstLink()
    p.feed(html)
    return p.found


def fetch(title):
    """(canonical title after redirects, first link or None, error or None), cached."""
    if title in CACHE:
        return CACHE[title]
    url = "https://en.wikipedia.org/api/rest_v1/page/html/" + urllib.parse.quote(title.replace(" ", "_"), safe="")
    err = None
    for attempt in range(3):
        try:
            html = get(url)
            err = None
            break
        except Exception as e:
            err = str(e)[:80]
            if "404" in err:
                break
            time.sleep(2 + 3 * attempt)
    if err:
        CACHE[title] = (title, None, err)
        return CACHE[title]
    canon = title
    marker = '<link rel="dc:isVersionOf" href="//en.wikipedia.org/wiki/'
    k = html.find(marker)
    if k >= 0:
        canon = urllib.parse.unquote(html[k + len(marker): html.find('"', k + len(marker))]).replace("_", " ")
    CACHE[title] = (canon, first_link(html), None)
    time.sleep(0.05)
    return CACHE[title]


def walk(start):
    path, seen, errs, t = [], set(), [], start
    for _ in range(MAX_HOPS):
        canon, nxt, err = fetch(t)
        path.append(canon)
        if err:
            errs.append([canon, err])
        if canon == TARGET:
            return "philosophy", path, errs
        if canon in seen:
            return "loop", path, errs
        seen.add(canon)
        if err or not nxt:
            return "dead end", path, errs
        t = nxt
    return "too long", path, errs


def row(start):
    outcome, path, errs = walk(start)
    return {"start": start, "outcome": outcome, "hops": len(path) - 1, "end": path[-1], "errors": errs, "path": path}


def now():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def summarise(rows):
    reached = sorted(r["hops"] for r in rows if r["outcome"] == "philosophy")
    return {"n": len(rows), "outcomes": dict(Counter(r["outcome"] for r in rows)),
            "median_hops_to_philosophy": reached[len(reached) // 2] if reached else None,
            "rows_with_fetch_errors_not_404": sum(any("404" not in e[1] for e in r["errors"]) for r in rows),
            "pages_fetched": len(CACHE)}


def diverge(old, new):
    for i, (a, b) in enumerate(zip(old, new)):
        if a != b:
            return {"after": old[i - 1] if i else None, "was": a, "now": b}
    k = min(len(old), len(new))
    return {"after": new[k - 1], "was": old[k] if len(old) > k else None, "now": new[k] if len(new) > k else None}


def recheck(old_rows, quiet=False):
    rows = []
    for o in old_rows:
        r = row(o["start"])
        r.update({"old_outcome": o["outcome"], "old_end": o["path"][-1], "old_hops": len(o["path"]) - 1,
                  "same_path": r["path"] == o["path"],
                  "diverge": None if r["path"] == o["path"] else diverge(o["path"], r["path"])})
        rows.append(r)
        if not quiet:
            print("%-10s -> %-10s %s%s" % (o["outcome"], r["outcome"], o["start"],
                  "" if r["same_path"] else "   CHANGED after %(after)s: %(was)s -> %(now)s" % r["diverge"]), flush=True)
    s = summarise(rows)
    s.update({"old_outcomes": dict(Counter(r["old_outcome"] for r in rows)),
              "outcome_class_changed": sum(r["old_outcome"] != r["outcome"] for r in rows),
              "end_page_changed": sum(r["old_end"] != r["end"] for r in rows),
              "path_changed": sum(not r["same_path"] for r in rows),
              "edits_behind_changes": dict(Counter("%(after)s: %(was)s -> %(now)s" % r["diverge"]
                                                   for r in rows if r["diverge"]))})
    return s, rows


def main():
    ap = argparse.ArgumentParser(description="Follow first links on English Wikipedia.")
    ap.add_argument("title", nargs="?", help="walk this one article")
    ap.add_argument("--random", type=int, metavar="N", help="walk N random articles")
    ap.add_argument("--recheck", metavar="FILE", help="walk the starts in a saved file again and compare")
    ap.add_argument("--out", metavar="FILE", help="write the paths here as JSON")
    a = ap.parse_args()
    if a.recheck:
        old = json.load(open(a.recheck))
        summary, rows = recheck(old["rows"])
        summary["old_at"] = (old.get("summary") or old).get("at")
    elif a.random:
        q = json.loads(get("https://en.wikipedia.org/w/api.php?action=query&list=random&rnnamespace=0&rnlimit=%d&format=json" % a.random))
        rows = []
        for r in q["query"]["random"]:
            rows.append(row(r["title"]))
            print("%-10s %3d  %s -> ... -> %s" % (rows[-1]["outcome"], rows[-1]["hops"], r["title"], rows[-1]["end"]), flush=True)
        summary = summarise(rows)
    elif a.title:
        rows = [row(a.title)]
        print(" -> ".join(rows[0]["path"]))
        print(rows[0]["outcome"], "in", rows[0]["hops"], "hops")
        summary = summarise(rows)
    else:
        ap.print_help()
        return 2
    summary["at"] = now()
    if not a.title or a.recheck or a.random:
        print(json.dumps(summary, indent=1))
    if a.out:
        json.dump({"summary": summary, "rows": rows}, open(a.out, "w"), indent=1)
        print("wrote", a.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
