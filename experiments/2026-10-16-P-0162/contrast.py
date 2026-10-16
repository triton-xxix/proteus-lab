#!/usr/bin/env python3
"""WCAG contrast of the lab site's (docs/index.html) text tokens on its two surfaces, light and dark."""
import json

def lum(h):
    h = h.lstrip("#")
    c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    c = [x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]

def ratio(a, b):
    la, lb = sorted([lum(a), lum(b)], reverse=True)
    return (la + 0.05) / (lb + 0.05)

themes = {
    "light": dict(paper="#e8eeec", raised="#f4f7f6", ink="#10242b", muted="#4f6268", tide="#1d6b74", buoy="#b8402b", keep="#2f6b3f"),
    "dark": dict(paper="#0d1b20", raised="#13252b", ink="#e3ecea", muted="#93a8ad", tide="#67c0c6", buoy="#ec8a72", keep="#8fcf9c"),
}
rows = []
for t, p in themes.items():
    for fg in ("ink", "muted", "tide", "buoy", "keep"):
        for bg in ("paper", "raised"):
            r = ratio(p[fg], p[bg])
            rows.append({"theme": t, "fg": fg, "bg": bg, "ratio": round(r, 2), "pass_4.5": r >= 4.5})
json.dump(rows, open("/Users/triton/PROTEUS/experiments/2026-10-16-P-0162/results.json", "w"), indent=1)
fails = [r for r in rows if not r["pass_4.5"]]
print(len(rows), "pairs,", len(fails), "fail")
for r in rows:
    print(r["theme"], r["fg"], "on", r["bg"], r["ratio"], "" if r["pass_4.5"] else "FAIL")
