"""Builds docs/tools/pacf-check/index.html from experiments/2026-10-22-P-0193/results.json, and exits
if the tool's own run (check-2026-10-22.json) disagrees with the probe on any PACF value or count.
python3 /Users/triton/PROTEUS/docs/tools/pacf-check/build.py"""
import html
import json
import sys

SRC = "/Users/triton/PROTEUS/experiments/2026-10-22-P-0193/results.json"
CHK = "/Users/triton/PROTEUS/docs/tools/pacf-check/check-2026-10-22.json"
OUT = "/Users/triton/PROTEUS/docs/tools/pacf-check/index.html"
R = json.load(open(SRC))
C = json.load(open(CHK))
M = R["markets"]
SYMS = list(M)
LAGS = 10

bad = []
for s in SYMS:
    for w, cw in (("prior", "first"), ("live", "second")):
        probe = [M[s][w]["pacf"][str(k)] for k in range(1, LAGS + 1)]
        tool = C["series"][s][cw]["pacf"]
        if any(abs(a - b) > 0.00011 for a, b in zip(probe, tool)) or M[s][w]["lags_outside_95"] != C["series"][s][cw]["outside"]:
            bad.append((s, w))
if bad:
    sys.exit("tool and probe disagree on %s" % bad)

both = {s: sorted(set(M[s]["prior"]["lags_outside_95"]) & set(M[s]["live"]["lags_outside_95"])) for s in SYMS}
n_both = sum(1 for s in SYMS if both[s])
flags = {w: sum(len(M[s][w]["lags_outside_95"]) for s in SYMS) for w in ("prior", "live")}
SP, SL = R["summary_prior"], R["summary_live"]
band = M["SPY"]["live"]["band"]

CW, CH, LEFT, TOP, GAP = 34, 26, 46, 34, 40
PW = LEFT + CW * LAGS


def panel(w, x0, title):
    out = [f'<text x="{x0 + LEFT}" y="14" class="pt">{title}</text>']
    for k in range(LAGS):
        out.append(f'<text x="{x0 + LEFT + CW * k + CW / 2}" y="{TOP - 6}" class="tick">{k + 1}</text>')
    for i, s in enumerate(SYMS):
        y = TOP + CH * i
        if x0 == 0:
            out.append(f'<text x="{LEFT - 8}" y="{y + CH / 2 + 4}" class="lab">{s}</text>')
        W = M[s][w]
        for k in range(LAGS):
            v = W["pacf"][str(k + 1)]
            r = min(abs(v) / W["band"], 1.6) / 1.6
            cls = "neg" if v < 0 else "pos"
            out_ = (k + 1) in W["lags_outside_95"]
            out.append(f'<rect x="{x0 + LEFT + CW * k + 1}" y="{y + 1}" width="{CW - 2}" height="{CH - 2}" class="c {cls}{" out" if out_ else ""}" '
                       f'style="opacity:{0.12 + 0.88 * r:.2f}"><title>{s} lag {k + 1}: {v:+.4f}, band {W["band"]}{" (outside)" if out_ else ""}</title></rect>')
            if out_:
                out.append(f'<text x="{x0 + LEFT + CW * k + CW / 2}" y="{y + CH / 2 + 4}" class="star">●</text>')
    return out


H = TOP + CH * len(SYMS) + 8
svg = [f'<svg viewBox="0 0 {PW * 2 + GAP} {H}" role="img" aria-label="PACF lags 1 to 10 for nine ETFs in two windows">']
svg += panel("prior", 0, "Oct 2022 to Oct 2024")
svg += panel("live", PW + GAP - LEFT, "Oct 2024 to Oct 2026")
svg.append("</svg>")

BW, BH, BL = 640, 150, 40
bx = lambda k: BL + (BW - BL - 10) * (k - 0.5) / LAGS
by = lambda c: BH - 24 - (BH - 44) * c / 9
bars = [f'<svg viewBox="0 0 {BW} {BH}" role="img" aria-label="ETFs with each lag outside the band, by window">']
for c in (0, 3, 6, 9):
    bars.append(f'<line x1="{BL}" x2="{BW - 10}" y1="{by(c):.1f}" y2="{by(c):.1f}" class="grid"/><text x="{BL - 6}" y="{by(c) + 4:.1f}" class="lab">{c}</text>')
bars.append(f'<line x1="{BL}" x2="{BW - 10}" y1="{by(0.45):.1f}" y2="{by(0.45):.1f}" class="chance"/>')
for k in range(1, LAGS + 1):
    for j, (w, cls) in enumerate((("summary_prior", "bp"), ("summary_live", "bl"))):
        c = R[w]["pooled_lag_counts"][str(k)]
        x = bx(k) - 13 + 13 * j
        bars.append(f'<rect x="{x:.1f}" y="{by(c):.1f}" width="12" height="{by(0) - by(c):.1f}" class="{cls}"><title>lag {k}: {c} of 9</title></rect>')
    bars.append(f'<text x="{bx(k):.1f}" y="{BH - 8}" class="tick">{k}</text>')
bars.append("</svg>")

page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>PACF Check</title>
<style>
:root{{--bg:#fbfaf7;--fg:#1d1d1b;--mut:#6b6a66;--line:#e2dfd8;--neg:#2b5f9e;--pos:#b5543c;--prior:#9c9a93;--live:#2b5f9e;--code:#f0eee8}}
@media (prefers-color-scheme:dark){{:root{{--bg:#151514;--fg:#ecebe6;--mut:#9c9a93;--line:#33322f;--neg:#6fa3e0;--pos:#e08468;--prior:#6b6a66;--live:#6fa3e0;--code:#22211f}}}}
body{{background:var(--bg);color:var(--fg);font:17px/1.55 Georgia,serif;margin:0}}
main{{max-width:820px;margin:0 auto;padding:32px 16px 64px}}
h1{{font-size:2.1rem;margin:.2em 0}} h2{{font-size:1.25rem;margin-top:2em}}
.k{{font:13px/1.4 ui-monospace,Menlo,monospace;color:var(--mut);text-transform:uppercase;letter-spacing:.08em}}
pre,code{{font:14px/1.5 ui-monospace,Menlo,monospace;background:var(--code)}} pre{{padding:12px;overflow-x:auto;border-radius:6px}}
svg{{width:100%;height:auto;display:block;margin:16px 0}}
.lab{{font:12px ui-monospace,Menlo,monospace;fill:var(--fg);text-anchor:end}}
.tick{{font:11px ui-monospace,Menlo,monospace;fill:var(--mut);text-anchor:middle}}
.pt{{font:13px ui-sans-serif,system-ui;fill:var(--fg);font-weight:600}}
.c.neg{{fill:var(--neg)}} .c.pos{{fill:var(--pos)}} .star{{font:11px sans-serif;fill:#fff;text-anchor:middle}}
.grid{{stroke:var(--line)}} .chance{{stroke:var(--mut);stroke-dasharray:4 3}} .bp{{fill:var(--prior)}} .bl{{fill:var(--live)}}
.big{{font-size:1.15rem}} .sw{{display:inline-block;width:12px;height:12px;border-radius:2px;vertical-align:-1px}}
a{{color:inherit}} .mut{{color:var(--mut)}}
</style></head><body><main>
<div class="k">Proteus tools · from probes P-0191 and P-0193</div>
<h1>PACF check</h1>
<p>A course says daily returns remember yesterday: plot the partial autocorrelation, see a lag poke out of the 95%
band, build a rule on it. Before building, ask a second window. This script computes PACF lags 1 to {LAGS} of daily log
returns in two windows split at a date and flags any lag that clears the band in one window and not the other.</p>
<p class="big">On nine index ETFs, {flags["live"]} lags cleared the band in the last two years and {flags["prior"]} in the two before.
<b>{n_both} of 9</b> had a lag clear it in both windows.</p>
<h2>Nine ETFs, two windows</h2>
<p class="mut">Each cell is one lag. <span class="sw" style="background:var(--neg)"></span> negative (mean reversion),
<span class="sw" style="background:var(--pos)"></span> positive; darker is closer to the band (±{band}), a dot is outside it.
About 1 cell in 20 clears the band by chance alone, so 4 or 5 of these 90 per window would.</p>
{''.join(svg)}
<p>Lag 3 looked like the find: outside the band in {SL["lag3_outside"]} of 9 in 2024-26, mean PACF {SL["mean_pacf3"]:+.3f}. In
2022-24 it was outside in {SP["lag3_outside"]} of 9 and its mean flipped to {SP["mean_pacf3"]:+.3f}. That window had its own
lag, 6, in four non-US ETFs, which the later window lacks. Lag 1 is the only one that keeps its sign: negative in
{SL["lag1_negative"]} of 9 then {SP["lag1_negative"]} of 9, mean {SL["mean_pacf1"]:+.3f} then {SP["mean_pacf1"]:+.3f}, real but small and only once outside the band.</p>
<h2>How many ETFs clear the band at each lag</h2>
<p class="mut"><span class="sw" style="background:var(--prior)"></span> 2022-24 <span class="sw" style="background:var(--live)"></span> 2024-26.
Dashed line: what chance alone gives on nine independent series (0.45). These nine are not independent: when SPY's
lag 3 dips, DIA's does too, so four at once is one coincidence counted four times.</p>
{''.join(bars)}
<h2>Use it</h2>
<pre>python3 pacf_check.py prices.csv --split 2024-10-23
python3 pacf_check.py --yahoo SPY QQQ EWU --start 2022-10-23 --split 2024-10-23
python3 pacf_check.py a.csv b.csv --split 2024-10-23 --lags 10 --json out.json</pre>
<p><a href="pacf_check.py">pacf_check.py</a> uses only the Python standard library. A CSV needs a date column and a close
column (adjclose is used when present); <code>--yahoo</code> pulls five years keyless. It prints both windows with a star on
each lag outside the band, the lags outside in both, the lags outside in one only, and with several series the pooled
count per lag. <a href="README.md">README</a>.</p>
<p class="mut">Checked: run on 22 Oct 2026 against today's Yahoo bars with the probe's dates, it reproduced every one of
P-0193's 180 PACF values and its band flags; build.py exits if the two ever disagree. Write-ups:
<a href="https://github.com/triton-xxix/proteus-lab/blob/main/experiments/2026-10-22-P-0191/README.md">P-0191</a>,
<a href="https://github.com/triton-xxix/proteus-lab/blob/main/experiments/2026-10-22-P-0193/README.md">P-0193</a>.
Numbers drawn from results.json by build.py. Not advice.</p>
</main></body></html>
"""
open(OUT, "w").write(page)
print("wrote", OUT, "both-window ETFs", n_both, "flags prior", flags["prior"], "live", flags["live"])
