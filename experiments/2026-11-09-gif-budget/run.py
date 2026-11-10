#!/usr/bin/env python3
"""How hard is WeChat's 500KB limit on a 12-frame 240x240 animated sticker?

Own script, no third-party repo. Pillow and ffmpeg only. Three synthetic clips of one
bobbing character, flat, shaded with the same grain every frame, and shaded with fresh
grain every frame (the stand-in for an image model redrawing each frame slightly differently).
Each is encoded many ways; the score is bytes and mean PSNR against the source frames.
Synthetic content, so the absolute sizes are illustrative; the ordering is the finding.
"""
import json
import math
import subprocess
import tempfile
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
W = 240
FRAMES = 12
LIMIT = 500_000
FFMPEG = "/usr/local/bin/ffmpeg"


def draw_character(t, shaded):
    s = 4
    im = Image.new("RGB", (W * s, W * s), (250, 240, 200))
    d = ImageDraw.Draw(im)
    y = int((120 + 22 * math.sin(2 * math.pi * t)) * s)
    x = int((120 + 14 * math.cos(2 * math.pi * t)) * s)
    r = 62 * s
    d.ellipse((x - r, y - r, x + r, y + r), fill=(240, 120, 60), outline=(60, 30, 20), width=3 * s)
    for ex in (-24, 24):
        d.ellipse((x + (ex - 9) * s, y - 26 * s, x + (ex + 9) * s, y - 8 * s), fill=(255, 255, 255))
        d.ellipse((x + (ex - 4) * s, y - 20 * s, x + (ex + 4) * s, y - 12 * s), fill=(20, 20, 30))
    d.arc((x - 30 * s, y - 6 * s, x + 30 * s, y + 36 * s), 20, 160, fill=(60, 30, 20), width=3 * s)
    im = im.resize((W, W), Image.LANCZOS)
    if not shaded:
        return np.asarray(im, dtype=np.float32)
    a = np.asarray(im, dtype=np.float32)
    yy, xx = np.mgrid[0:W, 0:W]
    light = 1.12 - 0.5 * np.hypot((xx - x / s + 30) / W, (yy - y / s + 30) / W)
    return np.clip(a * light[..., None], 0, 255)


def make_clip(kind):
    rng = np.random.default_rng(20261109)
    fixed = rng.normal(0, 3.0, (W, W, 3))
    out = []
    for i in range(FRAMES):
        a = draw_character(i / FRAMES, kind != "flat")
        if kind == "shaded_fixed_grain":
            a = a + fixed
        elif kind == "shaded_fresh_grain":
            a = a + rng.normal(0, 3.0, (W, W, 3))
        out.append(Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), "RGB"))
    return out


def pil_encode(frames, path, colors, dither):
    strip = Image.new("RGB", (W * FRAMES, W))
    for i, f in enumerate(frames):
        strip.paste(f, (i * W, 0))
    pal = strip.quantize(colors=colors, method=Image.MEDIANCUT)
    d = Image.FLOYDSTEINBERG if dither else Image.NONE
    ps = [f.quantize(palette=pal, dither=d) for f in frames]
    ps[0].save(path, save_all=True, append_images=ps[1:], duration=100, loop=0, optimize=True)


def ff_encode(srcdir, path, colors, dither, diff):
    use = f"paletteuse=dither={dither}:diff_mode={diff}"
    flt = f"[0:v]split[a][b];[a]palettegen=max_colors={colors}:stats_mode=full[p];[b][p]{use}"
    subprocess.run([FFMPEG, "-y", "-loglevel", "error", "-framerate", "10", "-i", str(srcdir / "f%02d.png"),
                    "-filter_complex", flt, "-loop", "0", str(path)], check=True)


def psnr(frames, path):
    im = Image.open(path)
    vals = []
    for i, f in enumerate(frames):
        im.seek(i)
        a = np.asarray(f.convert("RGB"), dtype=np.float64)
        b = np.asarray(im.convert("RGB"), dtype=np.float64)
        mse = float(np.mean((a - b) ** 2))
        vals.append(99.0 if mse == 0 else 10 * math.log10(255 ** 2 / mse))
    return round(float(np.mean(vals)), 2), getattr(im, "n_frames", 0)


def main():
    rows = []
    with tempfile.TemporaryDirectory(dir=str(HERE.parents[1] / "sandbox")) as tmp:
        tmp = Path(tmp)
        for kind in ("flat", "shaded_fixed_grain", "shaded_fresh_grain"):
            frames = make_clip(kind)
            src = tmp / kind
            src.mkdir()
            for i, f in enumerate(frames):
                f.save(src / f"f{i:02d}.png")
            jobs = []
            for c in (256, 128, 64, 32):
                for dd in (False, True):
                    jobs.append((f"pillow c{c} {'fs' if dd else 'none'}", "pil", c, dd, None))
                for dd in ("none", "bayer:bayer_scale=3", "sierra2_4a"):
                    for diff in ("none", "rectangle"):
                        jobs.append((f"ffmpeg c{c} {dd} diff={diff}", "ff", c, dd, diff))
            for i, (name, eng, c, dd, diff) in enumerate(jobs):
                p = tmp / f"{kind}-{i}.gif"
                if eng == "pil":
                    pil_encode(frames, p, c, dd)
                else:
                    ff_encode(src, p, c, dd, diff)
                q, n = psnr(frames, p)
                b = p.stat().st_size
                rows.append({"clip": kind, "encoder": name, "colors": c, "bytes": b, "psnr": q,
                             "frames": n, "under_limit": b <= LIMIT})
    (HERE / "results.json").write_text(json.dumps(rows, indent=1))
    for kind in ("flat", "shaded_fixed_grain", "shaded_fresh_grain"):
        sub = [r for r in rows if r["clip"] == kind]
        ok = [r for r in sub if r["under_limit"]]
        print(f"{kind}: {len(ok)} of {len(sub)} under 500KB; bytes {min(r['bytes'] for r in sub):,} to {max(r['bytes'] for r in sub):,}")
        best = max(ok, key=lambda r: r["psnr"]) if ok else None
        if best:
            print(f"  best under limit: {best['encoder']}, {best['bytes']:,} bytes, PSNR {best['psnr']}")
        for r in sorted(sub, key=lambda r: -r["psnr"])[:3]:
            print(f"  top quality: {r['encoder']}, {r['bytes']:,} bytes, PSNR {r['psnr']}")
    for c in (256, 128, 64, 32):
        for kind in ("flat", "shaded_fresh_grain"):
            for eng in ("pillow", "ffmpeg"):
                s = [r for r in rows if r["clip"] == kind and r["colors"] == c and r["encoder"].startswith(eng)]
                print(f"{kind} {eng} c{c}: mean bytes {int(np.mean([r['bytes'] for r in s])):,}, mean PSNR {np.mean([r['psnr'] for r in s]):.1f}")


if __name__ == "__main__":
    main()
