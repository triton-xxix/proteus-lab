#!/usr/bin/env python3
"""dupcheck: how much of a set of HTML pages is the same text on more than one page.

usage: dupcheck.py FOLDER [--top N] [--json OUT]

Reads every .html file under FOLDER, keeps the visible text (script, style,
nav, header and footer dropped), splits it into sentences and into 5-word
shingles, and reports for the set and for each page the share that also
appears on at least one other page. Standard library only.
"""
import collections
import html.parser
import json
import os
import re
import sys

SKIP = {"script", "style", "noscript", "svg", "nav", "header", "footer", "template"}
BLOCK = {"p", "div", "li", "h1", "h2", "h3", "h4", "h5", "h6", "td", "th", "tr", "br",
         "section", "article", "blockquote", "figcaption", "dt", "dd", "title", "summary"}


class Text(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.skip = 0
        self.out = []

    def handle_starttag(self, tag, attrs):
        if tag in SKIP:
            self.skip += 1
        if tag in BLOCK:
            self.out.append("\n")

    def handle_endtag(self, tag):
        if tag in SKIP and self.skip:
            self.skip -= 1
        if tag in BLOCK:
            self.out.append("\n")

    def handle_data(self, data):
        if not self.skip:
            self.out.append(data)


def visible(path):
    p = Text()
    with open(path, encoding="utf-8", errors="replace") as f:
        p.feed(f.read())
    return "".join(p.out)


def norm(s):
    return re.sub(r"[^a-z0-9£$%]+", " ", s.lower()).strip()


def sentences(text):
    out = []
    for block in text.split("\n"):
        for s in re.split(r"(?<=[.!?])\s+", block):
            n = norm(s)
            if len(n.split()) >= 4:          # a three-word fragment is a label, not a sentence
                out.append(n)
    return out


def shingles(sents, k=5):
    out = []
    for s in sents:
        w = s.split()
        for i in range(len(w) - k + 1):
            out.append(" ".join(w[i:i + k]))
    return out


def measure(folder, top=5):
    pages = {}
    for root, _dirs, files in os.walk(folder):
        for name in sorted(files):
            if name.endswith(".html"):
                path = os.path.join(root, name)
                sents = sentences(visible(path))
                if sents:
                    pages[os.path.relpath(path, folder)] = sents
    sent_pages = collections.defaultdict(set)
    shin_pages = collections.defaultdict(set)
    for page, sents in pages.items():
        for s in sents:
            sent_pages[s].add(page)
        for g in shingles(sents):
            shin_pages[g].add(page)
    per_page = {}
    tot_s = rep_s = tot_g = rep_g = 0
    for page, sents in pages.items():
        gs = shingles(sents)
        rs = sum(1 for s in sents if len(sent_pages[s]) > 1)
        rg = sum(1 for g in gs if len(shin_pages[g]) > 1)
        per_page[page] = {
            "sentences": len(sents), "sentence_repeat": round(rs / len(sents), 4),
            "shingles": len(gs), "shingle_repeat": round(rg / len(gs), 4) if gs else 0.0,
        }
        tot_s += len(sents)
        rep_s += rs
        tot_g += len(gs)
        rep_g += rg
    worst = sorted(sent_pages.items(), key=lambda kv: -len(kv[1]))[:top]
    return {
        "folder": folder,
        "pages": len(pages),
        "sentences": tot_s,
        "sentence_repeat": round(rep_s / tot_s, 4) if tot_s else 0.0,
        "shingles": tot_g,
        "shingle_repeat": round(rep_g / tot_g, 4) if tot_g else 0.0,
        "most_repeated": [{"on_pages": len(v), "sentence": k[:120]} for k, v in worst if len(v) > 1],
        "per_page": per_page,
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    top = int(sys.argv[sys.argv.index("--top") + 1]) if "--top" in sys.argv else 5
    res = measure(sys.argv[1], top)
    if "--json" in sys.argv:
        with open(sys.argv[sys.argv.index("--json") + 1], "w") as f:
            json.dump(res, f, indent=1)
    print("%s: %d pages, %d sentences, %.1f%% on another page too; %d five-word shingles, %.1f%% repeated" % (
        res["folder"], res["pages"], res["sentences"], 100 * res["sentence_repeat"],
        res["shingles"], 100 * res["shingle_repeat"]))
    for m in res["most_repeated"]:
        print("  on %d pages: %s" % (m["on_pages"], m["sentence"]))
