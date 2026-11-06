"""Print a page's section ids and its first paragraphs' links for one title on one date."""
import re
import sys

sys.path.insert(0, "/Users/triton/PROTEUS/experiments/2026-11-05-P-0332")
from ringdate import revid_at, html_of

for title, date in [("Social sciences", "2011-07-01"), ("Tribe (biology)", "2014-07-01"), ("Group decision making", "2011-07-01")]:
    rev = revid_at(title, date)
    html = html_of(title, rev)
    sec = re.findall(r'<section data-mw-section-id="(-?\d+)"', html)[:6]
    print(title, date, "rev", rev, "bytes", len(html), "section ids", sec)
    k = html.find("<p")
    para = html[k:k + 900]
    print("  first p:", re.sub(r"\s+", " ", para)[:900])
    print()
