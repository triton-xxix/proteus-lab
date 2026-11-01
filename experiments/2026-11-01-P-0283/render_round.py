"""P-0283: take the last snap event with marks from a Sketch Stadium SSE capture and draw it to an SVG,
following the site's own sketch.js: strokes {p: [[x,y],...] on a 0-100 grid, c: colour, w: width} and
shapes {sh: ...} as outlines, scaled by SIZE/100. Prints the event's keys and the mark counts.

    python3 experiments/2026-11-01-P-0283/render_round.py <capture.txt> <out.svg>
"""
import json
import sys

SIZE = 512
cap = open(sys.argv[1], encoding="utf-8", errors="replace").read()
events = []
for block in cap.split("\n\n"):
    ev, data = None, []
    for line in block.splitlines():
        if line.startswith("event:"):
            ev = line[6:].strip()
        elif line.startswith("data:"):
            data.append(line[5:].strip())
    if ev == "snap" and data:
        try:
            events.append(json.loads("".join(data)))
        except json.JSONDecodeError:
            pass
print("snap events parsed", len(events))
if not events:
    sys.exit(1)
print("keys of one snap:", sorted(events[-1].keys()))
best = max(events, key=lambda e: len(e.get("strokes") or []))
strokes = best.get("strokes") or []
print("most marks in one snap:", len(strokes), "round/word fields:", {k: best.get(k) for k in ("round", "phase", "word", "hint", "seq", "drawer") if k in best})
kinds = {"stroke": 0, "shape": 0, "other": 0}
for m in strokes:
    kinds["shape" if "sh" in m else "stroke" if "p" in m else "other"] += 1
print("mark kinds", kinds)
if strokes:
    print("first mark", json.dumps(strokes[0])[:300])
    sh = next((m for m in strokes if "sh" in m), None)
    if sh:
        print("a shape", json.dumps(sh)[:300])
# any image-looking field anywhere in the snap
flat = json.dumps(best)
for key in ("png", "image", "canvas", "snapshot", "thumb"):
    if key in flat:
        print("snap mentions", key)

COLORS = {"black": "#1d1d1f", "gray": "#8d99ae", "white": "#ffffff", "red": "#e5383b", "orange": "#f77f00",
          "yellow": "#fcbf49", "green": "#2a9d55", "blue": "#2667ff", "purple": "#7b2cbf", "pink": "#ff70a6",
          "brown": "#8d5524"}  # sketch.js COLORS, unknown names fall back to black


def colour(c):
    return COLORS.get(c, COLORS["black"])


def shape_svg(sh):
    d = []
    for sp in sh.get("d") or []:
        pts = sp.get("p") or []
        if not pts:
            continue
        d.append("M %.1f %.1f " % (pts[0][0] * SIZE / 100, pts[0][1] * SIZE / 100) +
                 " ".join("L %.1f %.1f" % (x * SIZE / 100, y * SIZE / 100) for x, y in pts[1:]) + (" Z" if sp.get("z") else ""))
    if not d:
        return None
    fill = colour(sh["f"]) if sh.get("f") else "none"
    fa = sh.get("fa")
    fo = ' fill-opacity="%.2f"' % fa if isinstance(fa, (int, float)) and 0 < fa < 1 else ""
    stroke = ""
    if sh.get("c") and (sh.get("w") or 0) > 0:
        sa = sh.get("sa")
        so = ' stroke-opacity="%.2f"' % sa if isinstance(sa, (int, float)) and 0 < sa < 1 else ""
        stroke = ' stroke="%s" stroke-width="%.1f" stroke-linecap="round" stroke-linejoin="round"%s' % (colour(sh["c"]), sh["w"] * SIZE / 100, so)
    return '<path d="%s" fill="%s" fill-rule="nonzero"%s%s/>' % (" ".join(d), fill, fo, stroke)


parts = ['<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d">' % (SIZE, SIZE, SIZE, SIZE),
         '<rect width="100%" height="100%" fill="white"/>']
drawn = 0
for m in strokes:
    if "p" in m and len(m["p"]) >= 1:
        pts = " ".join("%.1f,%.1f" % (x * SIZE / 100, y * SIZE / 100) for x, y in m["p"])
        w = float(m.get("w", 2)) * SIZE / 100 if float(m.get("w", 2)) < 20 else float(m.get("w", 2))
        if len(m["p"]) == 1:
            x, y = m["p"][0]
            parts.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s"/>' % (x * SIZE / 100, y * SIZE / 100, w / 2, colour(m.get("c"))))
        else:
            parts.append('<polyline points="%s" fill="none" stroke="%s" stroke-width="%.1f" stroke-linecap="round" stroke-linejoin="round"/>' % (pts, colour(m.get("c")), w))
        drawn += 1
    elif "sh" in m:
        s = shape_svg(m["sh"])
        if s:
            parts.append(s)
            drawn += 1
parts.append("</svg>")
open(sys.argv[2], "w").write("\n".join(parts))
print("drew", drawn, "strokes of", len(strokes), "marks to", sys.argv[2])
