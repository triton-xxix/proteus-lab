#!/usr/bin/env python3
"""Why does the top German 'ring' have one member? Print the first link and opening of the pages that stop walks."""
import re
import sys
import urllib.parse
import urllib.request

sys.path.insert(0, "/Users/triton/PROTEUS/experiments/2026-11-05-P-0332")
from walk_rule import FirstLink  # noqa: E402

UA = "ProteusLab-philosophy-walk/1.0 (https://github.com/triton-xxix; one-off research script)"
for title in ("System", "Sport", "Liste interkontinentaler Staaten", "Elena Florea", "Institut für Mathematik"):
    url = "https://de.wikipedia.org/api/rest_v1/page/html/" + urllib.parse.quote(title.replace(" ", "_"), safe="")
    html = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=30).read().decode()
    p = FirstLink()
    p.feed(html)
    m = re.search(r"<p[ >].*?</p>", html, re.S)
    text = re.sub(r"<[^>]+>", "", m.group(0))[:220] if m else None
    print(f"{title!r}: first link {p.found!r}; disambig={'disambiguation' in html.lower() or 'Begriffsklärung' in html[:4000]}")
    print("   ", text)
