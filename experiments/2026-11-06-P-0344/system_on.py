#!/usr/bin/env python3
"""The 10 'System' stops are a self-link, not a ring. Skip self-links on that one page and walk on: where does it end?"""
import json
import sys
import urllib.parse
import urllib.request
from pathlib import Path

sys.path.insert(0, "/Users/triton/PROTEUS/experiments/2026-11-05-P-0332")
from walk_rule import FirstLink  # noqa: E402

UA = "ProteusLab-philosophy-walk/1.0 (https://github.com/triton-xxix; one-off research script)"


class SkipSelf(FirstLink):
    def __init__(self, me):
        super().__init__()
        self.me = me

    def handle_starttag(self, tag, attrs):
        super().handle_starttag(tag, attrs)
        if self.found == self.me:
            self.found = None


def first(title):
    url = "https://de.wikipedia.org/api/rest_v1/page/html/" + urllib.parse.quote(title.replace(" ", "_"), safe="")
    html = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=30).read().decode()
    p = SkipSelf(title)
    p.feed(html)
    return p.found


path, t = [], "System"
while t and t not in path and t != "Philosophie" and len(path) < 40:
    path.append(t)
    t = first(t)
path.append(t)
print(" > ".join(str(x) for x in path))
Path(__file__).with_name("system_on.json").write_text(json.dumps(path, ensure_ascii=False, indent=1))
