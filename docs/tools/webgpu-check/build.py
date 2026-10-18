"""Builds docs/tools/webgpu-check/index.html from runs/*/results.json and P-0173's one-shot results.
python3 /Users/triton/PROTEUS/docs/tools/webgpu-check/build.py"""
import html
import json
import re

HERE = "/Users/triton/PROTEUS/docs/tools/webgpu-check"
P173 = "/Users/triton/PROTEUS/experiments/2026-10-18-P-0173"
OCEAN = json.load(open(f"{HERE}/runs/ocean/results.json"))
BROKEN = json.load(open(f"{HERE}/runs/broken/results.json"))
VIRT = json.load(open(f"{P173}/results.json"))
REAL = json.load(open(f"{P173}/results-real.json"))


v_dump, r_dump = VIRT["dump"], REAL["dump"]
fps_re = re.compile(r"^(\d+) fps")
rows = []  # per second of the CDP run: (ms, fps or None)
for s in OCEAN["samples"]:
    m = fps_re.match(s.get("#fps") or "")
    rows.append((s["ms"], int(m.group(1)) if m else None))
first = next(ms for ms, f in rows if f is not None)
fps_vals = [f for _, f in rows if f is not None]
SPAN = max(ms for ms, _ in rows) + 500

# Three lanes on one 0 to SPAN ms axis: what each way of running headless Chrome saw.
W, LEFT, LANE = 680, 190, 46
xs = lambda ms: LEFT + (W - LEFT - 14) * ms / SPAN
lanes = [
    ("--dump-dom, virtual time", v_dump["seconds"] * 1000, v_dump["fps_text"]),
    ("--dump-dom, --timeout", r_dump["seconds"] * 1000, r_dump["fps_text"]),
    ("webgpu_check.mjs (CDP)", None, None),
]
H = 34 + LANE * len(lanes) + 20
svg = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="Three ways of running headless Chrome on a WebGPU page">']
for t in range(0, int(SPAN / 1000) + 1, 2):
    x = xs(t * 1000)
    svg.append(f'<line x1="{x:.1f}" x2="{x:.1f}" y1="22" y2="{H - 18}" class="grid"/><text x="{x:.1f}" y="14" class="tick">{t} s</text>')
for i, (name, end, txt) in enumerate(lanes):
    y = 30 + LANE * i
    svg.append(f'<text x="{LEFT - 10}" y="{y + 22}" class="lab">{html.escape(name)}</text>')
    if end is not None:
        svg.append(f'<rect x="{LEFT}" y="{y + 8}" width="{xs(end) - LEFT:.1f}" height="20" class="wait"/>'
                   f'<text x="{xs(end) + 8:.1f}" y="{y + 23}" class="note">dumped at {end / 1000:g} s: “{html.escape(txt)}”</text>')
    else:
        svg.append(f'<rect x="{LEFT}" y="{y + 8}" width="{xs(first) - LEFT:.1f}" height="20" class="wait"/>')
        prev = first
        for ms, f in rows:
            if f is None:
                continue
            h = 30 * f / 60
            svg.append(f'<rect x="{xs(ms) - 9:.1f}" y="{y + 28 - h:.1f}" width="18" height="{h:.1f}" class="bar"><title>{ms / 1000:.1f} s: {f} fps</title></rect>')
        svg.append(f'<text x="{xs(first) - 12:.1f}" y="{y + 44}" class="note" text-anchor="end">first frame by {first / 1000:.1f} s</text>')
svg.append("</svg>")

ev = "".join(f'<li><code>{html.escape(e["kind"])}</code> at {e["ms"]} ms: {html.escape(e["text"].splitlines()[0])}</li>' for e in BROKEN["events"])
ad = OCEAN["gpu"]["adapter"]
adapter = " ".join(x for x in (ad["vendor"], ad["architecture"]) if x) or "unnamed"


def verdict_row(name, r, note):
    fr = r["frame"]
    return (f'<tr><td>{name}</td><td class="{r["verdict"]}">{r["verdict"]}</td><td>{r["errors"]}</td>'
            f'<td>{fr["colours"]}</td><td>{fr["top"] * 100:.1f}%</td><td>{html.escape("; ".join(r["reasons"]) or note)}</td></tr>')


trs = verdict_row("ocean.min.html (61 KB WebGPU sea)", OCEAN, "renders") + verdict_row("fixtures/broken.html", BROKEN, "")

page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>WebGPU Check</title>
<style>
:root{{--bg:#fbfaf7;--fg:#1d1d1b;--mut:#6b6a66;--line:#e2dfd8;--ok:#2f7d55;--no:#b5543c;--wait:#d9d5cc;--code:#f0eee8}}
@media (prefers-color-scheme:dark){{:root{{--bg:#151514;--fg:#ecebe6;--mut:#9c9a93;--line:#33322f;--ok:#5fbf8a;--no:#e08468;--wait:#3a3935;--code:#22211f}}}}
body{{background:var(--bg);color:var(--fg);font:17px/1.55 Georgia,serif;margin:0}}
main{{max-width:760px;margin:0 auto;padding:32px 16px 64px}}
h1{{font-size:2.1rem;margin:.2em 0}} h2{{font-size:1.25rem;margin-top:2em}}
.k{{font:13px/1.4 ui-monospace,Menlo,monospace;color:var(--mut);text-transform:uppercase;letter-spacing:.08em}}
pre,code{{font:14px/1.5 ui-monospace,Menlo,monospace;background:var(--code)}} pre{{padding:12px;overflow-x:auto;border-radius:6px}}
code{{word-break:break-word}}
svg{{width:100%;height:auto;display:block;margin:16px 0}}
.lab{{font:13px ui-sans-serif,system-ui;fill:var(--fg);text-anchor:end}}
.tick,.note{{font:11px ui-monospace,Menlo,monospace;fill:var(--mut)}} .tick{{text-anchor:middle}}
.grid{{stroke:var(--line)}} .wait{{fill:var(--wait)}} .bar{{fill:var(--ok)}}
img{{width:100%;height:auto;border-radius:6px;display:block}}
.tw{{overflow-x:auto}} table{{border-collapse:collapse;font:14px ui-sans-serif,system-ui;width:100%}}
td,th{{border-bottom:1px solid var(--line);padding:6px 8px;text-align:left}}
td.pass{{color:var(--ok);font-weight:600}} td.fail{{color:var(--no);font-weight:600}}
a{{color:inherit}} .mut{{color:var(--mut)}}
</style></head><body><main>
<div class="k">Proteus tools · from probe P-0173</div>
<h1>WebGPU check</h1>
<p>Does a WebGPU page actually draw something in headless Chrome, with nothing in the console? You would think
<code>chrome --headless --screenshot</code> answers that. It does not. A WebGPU page starts asynchronously
(adapter, device, shader compile), and Chrome's one-shot flags either freeze the clock or stop waiting. Both
gave me a screenshot and a clean console of a page that had not started. This script drives Chrome over the
DevTools protocol on a real clock, waits, and then judges the frame.</p>
<h2>Same page, three ways</h2>
<p class="mut">A 61 KB single-file WebGPU ocean. Grey: the page's own HUD still reads “starting…”. Green: frames per second
read from the HUD each second. Same Intel Mac, {adapter} adapter.</p>
{''.join(svg)}
<p>The one-shot runs exited cleanly, with a {VIRT["screenshot"]["png_bytes"]:,}-byte screenshot and no console errors,
on a page that had drawn nothing. Over CDP the first frame arrived by {first / 1000:.1f} s and the sea then held
{min(fps_vals)} to {max(fps_vals)} fps at {OCEAN["canvases"][0][0]}x{OCEAN["canvases"][0][1]}. On this machine about eight
seconds go before anything is drawn, so any check that waits less than that will tell you a working page is fine
for the wrong reason, and a broken one too.</p>
<img src="runs/ocean/shot-640.jpg" alt="Headless Chrome screenshot of the WebGPU ocean after {OCEAN['waitMs'] // 1000} seconds: a lit sea under a pale sky" loading="lazy">
<h2>Pass and fail</h2>
<p class="mut">A run fails on any of: no <code>navigator.gpu</code>, no adapter, a console error or uncaught exception, or a
frame where one colour covers more than 98% of the screenshot. Exit code 0 pass, 1 fail, 2 could not run.</p>
<div class="tw"><table><tr><th>Page</th><th>Verdict</th><th>Errors</th><th>Colours</th><th>Top colour</th><th>Why</th></tr>{trs}</table></div>
<p>The broken fixture is mine: it gets a device and then misspells a WGSL builtin. What the script caught:</p>
<ul>{ev}</ul>
<p class="mut">The WGSL parse message arrives as a warning, not an error, so the shader failure alone would not fail the run;
the page's own throw and the blank frame do. A page that swallows its errors and draws black still fails on the frame.</p>
<h2>Use it</h2>
<pre>node webgpu_check.mjs page.html --wait 12000 --watch "#fps,#err" --out run/
node webgpu_check.mjs https://example.com/demo --size 1920x1080</pre>
<p><a href="webgpu_check.mjs">webgpu_check.mjs</a> needs Node 22 or later and an installed Chrome; no npm install. It writes
<code>results.json</code> (adapter, canvases, per-second text of any selectors you watch, every console event, the
frame test) and <code>shot.png</code>. A temporary profile is made and removed each run. <a href="README.md">README</a>.</p>
<p class="mut">One machine, one window size, Chrome only. The blank test reads the screenshot, not the canvas, so a page that
paints a busy HTML overlay over a dead canvas will pass it. Numbers drawn from runs/*/results.json and P-0173's
results files by build.py. <a href="https://github.com/triton-xxix/proteus-lab/blob/main/experiments/2026-10-18-P-0173/README.md">Probe write-up</a>.</p>
</main></body></html>
"""
open(f"{HERE}/index.html", "w").write(page)
print("wrote", f"{HERE}/index.html", "first frame", first, "fps", min(fps_vals), max(fps_vals))
