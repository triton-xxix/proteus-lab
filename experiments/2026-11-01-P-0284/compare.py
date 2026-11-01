"""P-0284: draw a snap's marks with PIL at 512 px using sketch.js's rules (shapes: fill nonzero then round
outline; strokes: round-capped polyline), then count pixels that differ from the server's canvas.png.

    /Users/triton/PROTEUS/sandbox/py312-venv/bin/python3 experiments/2026-11-01-P-0284/compare.py
"""
import json
import os

import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
SIZE = 512
COLORS = {"black": "#1d1d1f", "gray": "#8d99ae", "white": "#ffffff", "red": "#e5383b", "orange": "#f77f00",
          "yellow": "#fcbf49", "green": "#2a9d55", "blue": "#2667ff", "purple": "#7b2cbf", "pink": "#ff70a6",
          "brown": "#8d5524"}


def rgb(name, alpha=None):
    h = COLORS.get(name, COLORS["black"]).lstrip("#")
    c = tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
    return c + ((int(round(alpha * 255)),) if alpha is not None else (255,))


def sc(pt):
    return (pt[0] * SIZE / 100, pt[1] * SIZE / 100)


def outline(layer, pts, colour, w, closed):
    d = ImageDraw.Draw(layer)
    p = [sc(q) for q in pts]
    if closed and len(p) > 1:
        p = p + [p[0]]
    if len(p) == 1:
        x, y = p[0]
        d.ellipse([x - w / 2, y - w / 2, x + w / 2, y + w / 2], fill=colour)
        return
    d.line(p, fill=colour, width=max(1, int(round(w))), joint="curve")
    for x, y in (p[0], p[-1]):
        d.ellipse([x - w / 2, y - w / 2, x + w / 2, y + w / 2], fill=colour)


snap = json.load(open(os.path.join(HERE, "snap.json")))
img = Image.new("RGBA", (SIZE, SIZE), (255, 255, 255, 255))
for m in snap.get("strokes") or []:
    layer = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    if "sh" in m:
        sh = m["sh"]
        subs = [sp for sp in sh.get("d") or [] if sp.get("p")]
        if sh.get("f"):
            fa = sh.get("fa")
            col = rgb(sh["f"], fa if isinstance(fa, (int, float)) and 0 < fa < 1 else None)
            d = ImageDraw.Draw(layer)
            for sp in subs:
                if len(sp["p"]) >= 3:
                    d.polygon([sc(q) for q in sp["p"]], fill=col)
        if sh.get("c") and (sh.get("w") or 0) > 0:
            sa = sh.get("sa")
            col = rgb(sh["c"], sa if isinstance(sa, (int, float)) and 0 < sa < 1 else None)
            for sp in subs:
                outline(layer, sp["p"], col, sh["w"] * SIZE / 100, bool(sp.get("z")))
    elif "p" in m and m["p"]:
        outline(layer, m["p"], rgb(m.get("c")), float(m.get("w", 2)) * SIZE / 100, False)
    img = Image.alpha_composite(img, layer)
mine = img.convert("RGB")
mine.save(os.path.join(HERE, "canvas-mine.png"))
server = Image.open(os.path.join(HERE, "canvas-server.png")).convert("RGB")
print("server size", server.size, "mine", mine.size)
if server.size != mine.size:
    server = server.resize(mine.size, Image.LANCZOS)
a = np.asarray(mine).astype(int)
b = np.asarray(server).astype(int)
dist = np.abs(a - b).max(axis=2)
res = {"seq": snap.get("seq"), "marks": len(snap.get("strokes") or []), "size": SIZE,
       "differ_any_pct": round(100 * float((dist > 0).mean()), 2),
       "differ_over_32_pct": round(100 * float((dist > 32).mean()), 2),
       "differ_over_96_pct": round(100 * float((dist > 96).mean()), 2),
       "mine_nonwhite_pct": round(100 * float((a.min(axis=2) < 250).mean()), 2),
       "server_nonwhite_pct": round(100 * float((b.min(axis=2) < 250).mean()), 2)}
print(res)
json.dump(res, open(os.path.join(HERE, "results.json"), "w"), indent=1)
Image.fromarray((np.clip(dist, 0, 255)).astype("uint8")).save(os.path.join(HERE, "diff.png"))
