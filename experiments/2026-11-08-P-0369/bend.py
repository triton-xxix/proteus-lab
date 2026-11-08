#!/usr/bin/env python3
"""P-0369: why does French Wikipedia's Concept page give no first link, and what happens with the rule bent once?

Bent means: on this one page, take a link the rule refused, then walk on under the unchanged rule from
P-0359. Tries the first three article links in the lead, in order, so the choice is visible.
"""
import json, re, sys
from html.parser import HTMLParser
from pathlib import Path

sys.path.insert(0, "/Users/triton/PROTEUS/experiments/2026-11-07-P-0359")
import fr_walk  # noqa: E402

HERE = Path("/Users/triton/PROTEUS/experiments/2026-11-08-P-0369")
html = fr_walk.get("https://fr.wikipedia.org/api/rest_v1/page/html/Concept")
(HERE / "concept.html").write_text(html)

walks_file = Path("/Users/triton/PROTEUS/experiments/2026-11-07-P-0359/walks.json")
old = json.loads(walks_file.read_text())
stuck = [r for r in old["rows"] if r["path"][-1] == "Concept"]
print("P-0359 walks ending on Concept:", len(stuck), {r["outcome"] for r in stuck})


class Lead(HTMLParser):
    """Text and article links of every paragraph and list item before the first heading."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.depth = 0          # parenthesis depth
        self.stack = []
        self.links = []
        self.text = []
        self.done = False
        self.tags = []

    def inside(self, *names):
        return any(t in names for t in self.tags)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in ("h2",):
            self.done = True
        if self.done:
            return
        void = tag in ("br", "img", "link", "meta", "hr", "wbr", "input")
        if not void:
            self.tags.append(tag)
        if tag == "a" and self.inside("p", "li") and "mw:WikiLink" in (a.get("rel") or ""):
            href = a.get("href", "")
            title = href[2:].split("#")[0] if href.startswith("./") else ""
            if title and ":" not in title:
                self.links.append({"title": title.replace("_", " "), "parens": self.depth,
                                   "in_italic": self.inside("i", "em"), "in_list": self.inside("li"),
                                   "in_sup": self.inside("sup"), "in_table": self.inside("table")})

    def handle_endtag(self, tag):
        if self.done:
            return
        for i in range(len(self.tags) - 1, -1, -1):
            if self.tags[i] == tag:
                del self.tags[i:]
                break

    def handle_data(self, data):
        if self.done or not self.inside("p", "li"):
            return
        self.text.append(data)
        for ch in data:
            if ch == "(":
                self.depth += 1
            elif ch == ")":
                self.depth = max(0, self.depth - 1)


p = Lead()
p.feed(html)
text = re.sub(r"\s+", " ", "".join(p.text)).strip()
print("lead text:", text[:700])
print("links in lead:", json.dumps(p.links[:12], ensure_ascii=False))
strict = fr_walk.FirstLink()
strict.feed(html)
print("rule's own first link:", strict.found)

out = {"stuck_walks": len(stuck), "lead_text": text[:700], "lead_links": p.links, "strict_first_link": strict.found, "bent": []}
for link in p.links[:3]:
    outcome, path = fr_walk.walk(link["title"])
    print(link["title"], "->", outcome, len(path) - 1, "hops:", " > ".join(path))
    out["bent"].append({**link, "outcome": outcome, "hops": len(path) - 1, "path": path})
(HERE / "results.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))
