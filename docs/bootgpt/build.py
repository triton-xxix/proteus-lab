"""Builds docs/bootgpt/: index.html (the story, every number read from the committed probe files) and
machine.html (the teardown page built by sites/bootgpt/build.mjs). Exits if the files disagree.
python3 /Users/triton/PROTEUS/docs/bootgpt/build.py"""
import html
import json
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = "/Users/triton/PROTEUS"
E = html.escape

boot = json.load(open(ROOT + "/experiments/2026-11-02-P-0294/results.json"))
screen = open(ROOT + "/experiments/2026-11-02-P-0294/screen.txt").read().rstrip("\n").split("\n")
chk = json.load(open(ROOT + "/sites/bootgpt/results.json"))
machine = ROOT + "/sites/bootgpt/out/dist/bootgpt.html"

d, p = chk["views"]["desktop"], chk["views"]["phone"]
for v in (d, p):
    if v["full_rows_differing"] != boot["rows_differing"] or v["printed_chars_compared"] != boot["printed_chars_compared"] \
            or not v["last_row_prefix_match"] or v["page_errors"] or v["horizontal_overflow_px"]:
        sys.exit("page check and P-0294 disagree, not building: %r" % v)
if boot["seeds_consistent"] != 1:
    sys.exit("seed not unique")

shutil.copyfile(machine, os.path.join(HERE, "machine.html"))
kb = round(os.path.getsize(machine) / 1024)
seed = boot["seed"]
odd = 0x10000 // 2
used = boot["chars_used_for_seed"]
after = boot["printed_chars_compared"] - used

shot = "\n".join(screen)
tiles = [
    (seed, "the seed this boot used, found from the screen"),
    ("1 of %s" % f"{odd:,}", "odd seeds fit the first %d characters" % used),
    ("%d" % boot["rows_differing"], "rows differ, sim v emulator, over %d characters" % boot["printed_chars_compared"]),
    ("%d KB" % kb, "the whole machine below, offline, one file"),
]
tile_html = "".join('<div class="tile"><b>%s</b><span>%s</span></div>' % (E(a), E(b)) for a, b in tiles)

page = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>bootgpt taken apart</title>
<style>
:root{--bg:#f7f5f0;--fg:#1d1d1b;--dim:#6b6860;--line:#dedad0;--acc:#b5451b;--card:#fff;--term:#111;--tfg:#c8c8c8}
@media (prefers-color-scheme:dark){:root{--bg:#141413;--fg:#ecebe6;--dim:#9a978e;--line:#2e2d2a;--acc:#e07b52;--card:#1d1d1b}}
body{margin:0;background:var(--bg);color:var(--fg);font:17px/1.55 Georgia,serif}
main{max-width:860px;margin:0 auto;padding:24px 16px 64px}
h1{font-size:30px;margin:0 0 6px}h2{font-size:21px;margin:32px 0 6px}
a{color:var(--acc)}.dim{color:var(--dim);font-size:14px}
.tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:10px;margin:20px 0}
.tile{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:12px}
.tile b{display:block;font:700 24px/1.2 ui-monospace,Menlo,monospace;color:var(--acc)}.tile span{font-size:14px;color:var(--dim)}
pre{background:var(--term);color:var(--tfg);padding:12px;border-radius:6px;overflow-x:auto;font:12px/1.35 ui-monospace,Menlo,monospace}
.go{display:inline-block;margin:8px 0;padding:10px 16px;background:var(--acc);color:#fff;border-radius:6px;text-decoration:none;font-family:system-ui,sans-serif}
iframe{width:100%%;aspect-ratio:16/9;border:1px solid var(--line);border-radius:8px;background:#f6f4ef}
@media (max-width:600px){iframe{aspect-ratio:9/14}}
</style></head><body><main>
<p class="dim"><a href="../">Proteus lab</a> / bootgpt</p>
<h1>bootgpt taken apart</h1>
<p>bootgpt is a 512-byte boot sector that runs a tiny character-level neural network and dreams a Linux boot
log, with no operating system underneath. I booted it in an emulator, read the screen, and rebuilt the same
integer arithmetic in a web page. The page below is that network running one character per step, and it
types the same screen the emulator did.</p>
<div class="tiles">%(tiles)s</div>
<h2>What the emulator showed</h2>
<p>The disk booted in v86 under Node, headless. This is its screen, rebuilt from the emulator's character events:</p>
<pre>%(shot)s</pre>
<h2>The catch: the seed comes from the clock</h2>
<p>The project's training script prints a sample at seed 0x1234. The disk takes its seed from the PC's timer and
forces it odd, so that sample can never appear on a real boot. The network's scores depend only on the last
eight characters, which the screen shows, so I stepped all %(odd)s odd seeds at once and kept the ones that
print the same first %(used)d characters. One survived: %(seed)s. From it, my rebuild of the network matches the
next %(after)d characters with %(diff)d rows differing.</p>
<h2>The machine</h2>
<p>Eight characters in, 96 hidden units clipped to plus or minus 64, 64 scores out, a little pseudo-random noise,
and the highest wins. Drag the slider to any step; type a new seed to dream a different boot.</p>
<p><a class="go" href="machine.html">Open it full screen</a></p>
<iframe src="machine.html" title="bootgpt machine" loading="lazy"></iframe>
<p class="dim">Checked headless at 1600x900 and 375x812: %(rows)d emulator rows, %(diff)d differing, 0 px sideways
scroll, slider and seed box work, no page errors. Phones held upright get their own layout. Probes P-0294 to P-0296
plus the Workshop of 2 Nov 2026; not yet looked at in a real phone browser.</p>
</main></body></html>
""" % dict(tiles=tile_html, shot=E(shot), odd=f"{odd:,}", used=used, seed=E(seed), after=after,
           diff=boot["rows_differing"], rows=d["rows_compared"])

open(os.path.join(HERE, "index.html"), "w").write(page)
print("index.html %d bytes, machine.html %d KB, seed %s" % (len(page), kb, seed))
