"""Getting to Philosophy, measured: follow the first link of random English Wikipedia articles.

Rule used (the common one): first link in the article's lead paragraphs that is not inside
parentheses, not in italics, not in a hatnote, infobox, table or footnote, and points to
another article (no namespace). Stop on Philosophy, on a loop, on a dead end, or at 60 hops.

Usage: python3 walk.py N OUTDIR
"""
import json
import sys
import time
import urllib.parse
import urllib.request
from html.parser import HTMLParser

UA = "ProteusLab-philosophy-walk/1.0 (https://github.com/triton-xxix; one-off research script)"
CACHE = {}


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8")


class FirstLink(HTMLParser):
    SKIP_TAGS = {"table", "sup", "style", "figure", "math", "span_skip"}

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
        # pop to matching tag
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


def resolve_and_first(title):
    if title in CACHE:
        return CACHE[title]
    url = "https://en.wikipedia.org/api/rest_v1/page/html/" + urllib.parse.quote(title.replace(" ", "_"), safe="")
    try:
        html = get(url)
    except Exception as e:  # dead end
        CACHE[title] = (title, None, str(e)[:80])
        return CACHE[title]
    # canonical title after redirects
    canon = title
    marker = '<link rel="dc:isVersionOf" href="//en.wikipedia.org/wiki/'
    k = html.find(marker)
    if k >= 0:
        canon = urllib.parse.unquote(html[k + len(marker): html.find('"', k + len(marker))]).replace("_", " ")
    p = FirstLink()
    p.feed(html)
    CACHE[title] = (canon, p.found, None)
    time.sleep(0.05)
    return CACHE[title]


def walk(start):
    path = []
    seen = set()
    t = start
    for _ in range(60):
        canon, nxt, err = resolve_and_first(t)
        path.append(canon)
        if canon == "Philosophy":
            return "philosophy", path
        if canon in seen:
            return "loop", path
        seen.add(canon)
        if err or not nxt:
            return "dead end", path
        t = nxt
    return "too long", path


def main():
    n = int(sys.argv[1])
    out = sys.argv[2]
    q = json.loads(get(f"https://en.wikipedia.org/w/api.php?action=query&list=random&rnnamespace=0&rnlimit={n}&format=json"))
    starts = [r["title"] for r in q["query"]["random"]]
    rows = []
    for s in starts:
        outcome, path = walk(s)
        rows.append({"start": s, "outcome": outcome, "hops": len(path) - 1, "path": path})
        print(f"{outcome:11s} {len(path)-1:3d}  {s} -> ... -> {path[-1]}", flush=True)
    with open(out + "/walks.json", "w") as f:
        json.dump({"at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "n": n, "rows": rows,
                   "pages_fetched": len(CACHE)}, f, indent=1)
    reached = [r for r in rows if r["outcome"] == "philosophy"]
    hops = sorted(r["hops"] for r in reached)
    print(f"reached Philosophy {len(reached)} of {n}; median hops {hops[len(hops)//2] if hops else '-'}; pages fetched {len(CACHE)}")
    from collections import Counter
    print("outcomes", dict(Counter(r["outcome"] for r in rows)))
    ends = Counter(r["path"][-1] for r in rows if r["outcome"] != "philosophy")
    print("other ends", ends.most_common(6))
    # the funnel: the most common page just before Philosophy
    pre = Counter(r["path"][-2] for r in reached if len(r["path"]) > 1)
    print("last step into Philosophy", pre.most_common(5))


if __name__ == "__main__":
    main()
