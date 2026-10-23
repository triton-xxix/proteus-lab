#!/usr/bin/env python3
"""P-0203: does track_edges.py (rossark-motion-skill) recover a known 2 percent sway to within half a point?

Synthetic clip: a 500x400 frame, a 160x240 orange rectangle whose centre sways sideways with a
peak-to-peak excursion of exactly 2.0 percent of the frame width (10 px, amplitude 5 px) at 1 Hz, and a
vertical bob of 1.0 percent of frame height (4 px peak to peak) at 0.5 Hz. Sub-pixel positions are
rendered with anti-aliasing (area coverage), so the clip is the sort of thing a real renderer makes.
Encoded twice with ffmpeg: lossless (libx264 qp 0, yuv444p) and ordinary (crf 18, yuv420p). Then the
tool is run as its README says, with python3 -I, and its printed table is parsed.
Run: /Users/triton/PROTEUS/.venv/bin/python3 /Users/triton/PROTEUS/experiments/2026-10-23-P-0203/sway_test.py
"""
import json
import math
import os
import subprocess
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
TOOL = "/Users/triton/PROTEUS/sandbox/rossark-motion/track_edges.py"
OUT = "/Users/triton/PROTEUS/sandbox/rossark-motion"
W, H, FPS, SECS = 500, 400, 60, 2.0
RW, RH = 160, 240
CX0, CY0 = 250.0, 200.0
SWAY_PP_PCT = 2.0           # of frame width, peak to peak
BOB_PP_PCT = 1.0            # of frame height, peak to peak
BG = (24, 28, 36)
FG = (235, 120, 30)         # EB781E


def frame(t):
    ax = SWAY_PP_PCT / 100 * W / 2
    ay = BOB_PP_PCT / 100 * H / 2
    cx = CX0 + ax * math.sin(2 * math.pi * 1.0 * t)
    cy = CY0 + ay * math.sin(2 * math.pi * 0.5 * t)
    x0, x1 = cx - RW / 2, cx + RW / 2
    y0, y1 = cy - RH / 2, cy + RH / 2
    xs = np.arange(W)
    ys = np.arange(H)
    covx = np.clip(np.minimum(xs + 1, x1) - np.maximum(xs, x0), 0, 1)
    covy = np.clip(np.minimum(ys + 1, y1) - np.maximum(ys, y0), 0, 1)
    cov = covy[:, None] * covx[None, :]
    img = np.empty((H, W, 3), dtype=np.float32)
    for c in range(3):
        img[..., c] = BG[c] + (FG[c] - BG[c]) * cov
    return np.round(img).astype(np.uint8), x0, x1, y0


def encode(path, extra):
    n = int(FPS * SECS)
    truth = []
    cmd = ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
           "-r", str(FPS), "-i", "-"] + extra + [path]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for i in range(n):
        img, x0, x1, y0 = frame(i / FPS)
        p.stdin.write(img.tobytes())
        truth.append({"frame": i, "left": x0, "right": x1, "top": y0})
    p.stdin.close()
    p.wait()
    return truth


def run_tool(path):
    cmd = [sys.executable, "-I", TOOL, path, "--start", "0", "--dur", str(SECS), "--fps", str(FPS),
           "--crop", f"0:0:{W}:{H}", "--colors", "EB781E", "--tol", "60", "--cols", "250", "--row", "200"]
    t0 = time.time()
    out = subprocess.run(cmd, capture_output=True, text=True, check=True).stdout
    secs = time.time() - t0
    rows = []
    for line in out.splitlines()[1:]:
        parts = line.split()
        if len(parts) < 6:
            continue
        f, ms, top, left, right, width = parts[:6]
        rows.append({"frame": int(f), "top": None if top == "-" else int(top),
                     "left": None if left == "-" else int(left), "right": None if right == "-" else int(right),
                     "width": None if width == "-" else int(width)})
    return rows, secs, out


def score(rows, truth):
    lefts = [r["left"] for r in rows if r["left"] is not None]
    rights = [r["right"] for r in rows if r["right"] is not None]
    tops = [r["top"] for r in rows if r["top"] is not None]
    centres = [(r["left"] + r["right"]) / 2 for r in rows if r["left"] is not None and r["right"] is not None]
    true_centres = [(t["left"] + t["right"]) / 2 for t in truth]
    n = min(len(centres), len(true_centres))
    err = [abs(centres[i] - true_centres[i]) for i in range(n)]
    sway_pp_px = max(centres) - min(centres)
    return {
        "frames_read": len(rows),
        "frames_with_edges": len(centres),
        "sway_pp_px_measured": sway_pp_px,
        "sway_pp_pct_measured": round(100 * sway_pp_px / W, 2),
        "sway_pp_pct_true": SWAY_PP_PCT,
        "sway_error_points": round(100 * sway_pp_px / W - SWAY_PP_PCT, 2),
        "left_range_px": [min(lefts), max(lefts)],
        "right_range_px": [min(rights), max(rights)],
        "width_values": sorted(set(r["width"] for r in rows if r["width"] is not None)),
        "bob_pp_px_measured": max(tops) - min(tops),
        "bob_pp_pct_measured": round(100 * (max(tops) - min(tops)) / H, 2),
        "bob_pp_pct_true": BOB_PP_PCT,
        "centre_abs_err_px_mean": round(float(np.mean(err)), 3),
        "centre_abs_err_px_max": round(float(np.max(err)), 3),
    }


def main():
    os.makedirs(OUT, exist_ok=True)
    res = {"frame": [W, H], "fps": FPS, "seconds": SECS, "rect": [RW, RH], "tool": TOOL, "cases": {}}
    for name, extra in {
        "lossless_qp0_yuv444p": ["-c:v", "libx264", "-qp", "0", "-pix_fmt", "yuv444p"],
        "crf18_yuv420p": ["-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p"],
    }.items():
        path = os.path.join(OUT, f"sway_{name}.mp4")
        truth = encode(path, extra)
        rows, secs, raw = run_tool(path)
        s = score(rows, truth)
        s["tool_seconds"] = round(secs, 2)
        res["cases"][name] = s
        with open(os.path.join(HERE, f"tool_output_{name}.txt"), "w") as fh:
            fh.write(raw)
        print(name, json.dumps(s))
    with open(os.path.join(HERE, "results.json"), "w") as fh:
        json.dump(res, fh, indent=1)


if __name__ == "__main__":
    main()
