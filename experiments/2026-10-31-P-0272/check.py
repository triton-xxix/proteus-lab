"""P-0272: count pixelfx effect files and compare three renders (two same-seed, one other seed)."""
import hashlib
import json
import os
import re
import zlib

SRC = "/Users/triton/PROTEUS/sandbox/pixelfx-src/pixelfx-main"
RUNS = "/Users/triton/PROTEUS/sandbox/pixelfx-src"
OUT = "/Users/triton/PROTEUS/experiments/2026-10-31-P-0272/results.json"
FX = ["fire/torch", "explosions/big-explosion", "transitions/iris"]

# 1. count
files = []
for cat in sorted(os.listdir(os.path.join(SRC, "src/fx"))):
    d = os.path.join(SRC, "src/fx", cat)
    if not os.path.isdir(d):
        continue
    for f in sorted(os.listdir(d)):
        if f.endswith(".js") and not f.startswith("_"):
            files.append(f"{cat}/{f[:-3]}")
readme = open(os.path.join(SRC, "README.md"), encoding="utf-8").read()
m = re.search(r"<!-- count -->(\d+)<!-- /count -->", readme)
claimed = int(m.group(1)) if m else None
cats = {}
for f in files:
    cats[f.split("/")[0]] = cats.get(f.split("/")[0], 0) + 1
kinds = {"draw": 0, "create": 0, "other": 0}
sizes = []
for f in files:
    src = open(os.path.join(SRC, "src/fx", f + ".js"), encoding="utf-8").read()
    sizes.append(len(src.encode()))
    if re.search(r"export\s+function\s+create\b|export\s*\{[^}]*\bcreate\b", src):
        kinds["create"] += 1
    elif re.search(r"export\s+function\s+draw\b|export\s*\{[^}]*\bdraw\b", src):
        kinds["draw"] += 1
    else:
        kinds["other"] += 1
sizes.sort()


# 2. renders: decode the sprite-sheet PNG to raw pixels so the comparison is on pixels, not file bytes
def png_pixels(path):
    data = open(path, "rb").read()
    pos = 8
    idat = b""
    w = h = 0
    while pos < len(data):
        ln = int.from_bytes(data[pos:pos + 4], "big")
        typ = data[pos + 4:pos + 8]
        body = data[pos + 8:pos + 8 + ln]
        if typ == b"IHDR":
            w, h = int.from_bytes(body[:4], "big"), int.from_bytes(body[4:8], "big")
            assert body[8] == 8 and body[9] == 6, "expected 8-bit RGBA"
        elif typ == b"IDAT":
            idat += body
        pos += 12 + ln
    raw = zlib.decompress(idat)
    stride = w * 4
    out = bytearray()
    prev = bytearray(stride)
    i = 0
    for _ in range(h):
        ft = raw[i]
        line = bytearray(raw[i + 1:i + 1 + stride])
        i += 1 + stride
        for x in range(stride):
            a = line[x - 4] if x >= 4 else 0
            b = prev[x]
            c = prev[x - 4] if x >= 4 else 0
            if ft == 1:
                line[x] = (line[x] + a) & 255
            elif ft == 2:
                line[x] = (line[x] + b) & 255
            elif ft == 3:
                line[x] = (line[x] + ((a + b) >> 1)) & 255
            elif ft == 4:
                p = a + b - c
                pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
                pr = a if pa <= pb and pa <= pc else (b if pb <= pc else c)
                line[x] = (line[x] + pr) & 255
        out += line
        prev = line
    return w, h, bytes(out)


renders = {}
for fx in FX:
    name = fx.split("/")[1]
    px = {}
    meta = {}
    for run in ("run1", "run2", "run3"):
        p = os.path.join(RUNS, run, fx, name + ".png")
        w, h, pix = png_pixels(p)
        px[run] = pix
        meta[run] = {"w": w, "h": h, "sha256": hashlib.sha256(pix).hexdigest()[:16], "bytes": os.path.getsize(p)}
    j1 = json.load(open(os.path.join(RUNS, "run1", fx, name + ".json")))
    frames = j1.get("frames") if isinstance(j1, dict) else None
    n_frames = len(frames) if isinstance(frames, (list, dict)) else None
    diff13 = sum(1 for i in range(0, min(len(px["run1"]), len(px["run3"])), 4)
                 if px["run1"][i:i + 4] != px["run3"][i:i + 4]) if meta["run1"]["w"] == meta["run3"]["w"] else None
    renders[fx] = {
        "frames": n_frames,
        "same_seed_identical": px["run1"] == px["run2"],
        "other_seed_identical": px["run1"] == px["run3"],
        "pixels_differing_run1_v_run3": diff13,
        "pixels_total": (meta["run1"]["w"] * meta["run1"]["h"]),
        "runs": meta,
    }

res = {
    "count_src_fx": len(files),
    "readme_claim": claimed,
    "categories": cats,
    "kinds_by_export": kinds,
    "file_bytes_median": sizes[len(sizes) // 2],
    "file_bytes_min_max": [sizes[0], sizes[-1]],
    "renders": renders,
}
json.dump(res, open(OUT, "w"), indent=1)
print(json.dumps({k: v for k, v in res.items() if k != "categories"}, indent=1))
