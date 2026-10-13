"""Builds docs/tools/luck-test/index.html from experiments/2026-10-07-P-0082/results.json.
python3 /Users/triton/PROTEUS/docs/tools/luck-test/build.py"""
import html
import json
import math

SRC = "/Users/triton/PROTEUS/experiments/2026-10-07-P-0082/results.json"
OUT = "/Users/triton/PROTEUS/docs/tools/luck-test/index.html"
R = json.load(open(SRC))

rows = []  # (label, period, p, real pf, shuffled median)
t1 = R["qs_ma_200_vs_222"]
rows.append(("200-day MA filter", "1993 on", t1["mcpt_fixed_200"]))
rows.append(("Best MA of 281 lengths", "1993 on", t1["mcpt_best_of_281"]))
for k, nm in (("simple", "RSI(5) simple"), ("double", "RSI(5) double"), ("triple", "RSI(5) triple")):
    rows.append((nm, "1993 on", R["qs_rsi5_simple_double_triple"][k]["mcpt"]))
t3 = R["qs_rsi2_threshold_sweep"]
rows.append(("RSI(2) below 30", "1993 on", t3["mcpt_fixed_30"]))
rows.append(("Best RSI(2) of 50 levels", "1993 on", t3["mcpt_best_of_50_min100trades"]))
names = {"rsi2_lt9": "RSI(2) below 9", "rsi2_lt30": "RSI(2) below 30", "rsi5_simple": "RSI(5) simple",
         "rsi5_triple": "RSI(5) triple", "ma200": "200-day MA filter"}
for k, nm in names.items():
    rows.append((nm, "2009 on", R["post_publication_2009_on"][k]["mcpt_2009_on"]))
dav = []
for key, nm in (("davey_golden_cross_daily_etfs", "Golden cross"), ("davey_rsi_cross_daily_etfs", "RSI crossover")):
    m = R[key]["markets"]
    dav.append((nm, sum(1 for v in m.values() if v["best_of_48_p"] < 0.05), len(m),
                min(m.items(), key=lambda kv: kv[1]["best_of_48_p"])))

W, ROWH, LEFT = 640, 30, 210
def xs(p):
    """x position for p on a log scale from 0.001 to 1."""
    return LEFT + (W - LEFT - 20) * (math.log10(max(p, 0.001)) + 3) / 3


H = 40 + ROWH * len(rows)
svg = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="Luck test p-values, log scale">']
x05 = xs(0.05)
svg.append(f'<rect x="{LEFT}" y="20" width="{x05 - LEFT:.1f}" height="{H - 30}" class="pass"/>')
for p in (0.001, 0.01, 0.05, 0.1, 1.0):
    svg.append(f'<line x1="{xs(p):.1f}" x2="{xs(p):.1f}" y1="20" y2="{H - 10}" class="grid"/>'
               f'<text x="{xs(p):.1f}" y="14" class="tick">{p:g}</text>')
for i, (nm, per, t) in enumerate(rows):
    y = 20 + ROWH * i + ROWH / 2
    cls = "dot ok" if t["p"] < 0.05 else "dot no"
    svg.append(f'<text x="{LEFT - 8}" y="{y + 4:.1f}" class="lab">{html.escape(nm)} <tspan class="per">{per}</tspan></text>'
               f'<circle cx="{xs(t["p"]):.1f}" cy="{y:.1f}" r="6" class="{cls}"><title>p = {t["p"]}, profit factor {t["real_bar_pf"]} v shuffled median {t["perm_median_pf"]}</title></circle>')
svg.append("</svg>")

trs = "".join(f'<tr><td>{html.escape(nm)}</td><td>{per}</td><td>{t["real_bar_pf"]}</td><td>{t["perm_median_pf"]}</td>'
              f'<td>{t["p"]}</td><td>{"passes" if t["p"] < 0.05 else "fails"}</td></tr>' for nm, per, t in rows)
dv = "".join(f'<li><b>{nm}</b>: {k} of {n} markets under 0.05 after paying for 48 settings '
             f'(closest {best[0]}, p {best[1]["best_of_48_p"]}).</li>' for nm, k, n, best in dav)

page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>Luck Test</title>
<style>
:root{{--bg:#fbfaf7;--fg:#1d1d1b;--mut:#6b6a66;--line:#e2dfd8;--ok:#2f7d55;--no:#b5543c;--band:#2f7d5514;--code:#f0eee8}}
@media (prefers-color-scheme:dark){{:root{{--bg:#151514;--fg:#ecebe6;--mut:#9c9a93;--line:#33322f;--ok:#5fbf8a;--no:#e08468;--band:#5fbf8a1c;--code:#22211f}}}}
body{{background:var(--bg);color:var(--fg);font:17px/1.55 Georgia,serif;margin:0}}
main{{max-width:760px;margin:0 auto;padding:32px 16px 64px}}
h1{{font-size:2.1rem;margin:.2em 0}} h2{{font-size:1.25rem;margin-top:2em}}
.k{{font:13px/1.4 ui-monospace,Menlo,monospace;color:var(--mut);text-transform:uppercase;letter-spacing:.08em}}
pre,code{{font:14px/1.5 ui-monospace,Menlo,monospace;background:var(--code)}} pre{{padding:12px;overflow-x:auto;border-radius:6px}}
svg{{width:100%;height:auto;display:block;margin:16px 0}}
.lab{{font:13px ui-sans-serif,system-ui;fill:var(--fg);text-anchor:end}} .per{{fill:var(--mut)}}
.tick{{font:11px ui-monospace,Menlo,monospace;fill:var(--mut);text-anchor:middle}}
.grid{{stroke:var(--line)}} .pass{{fill:var(--band)}} .dot.ok{{fill:var(--ok)}} .dot.no{{fill:var(--no)}}
.tw{{overflow-x:auto}} table{{border-collapse:collapse;font:14px ui-sans-serif,system-ui;width:100%}}
td,th{{border-bottom:1px solid var(--line);padding:6px 8px;text-align:left}}
a{{color:inherit}} .mut{{color:var(--mut)}}
</style></head><body><main>
<div class="k">Proteus tools · from probe P-0082</div>
<h1>Luck test</h1>
<p>A backtest says a rule made money. Would it have made as much on a market with the same moves in a random order?
This script shuffles the overnight gaps and the moves inside each day separately, rebuilds the price series, runs the
same rule, and counts how often the shuffle does at least as well. A rule that only rides the market's drift scores about
the same on shuffles. A real timing edge does not.</p>
<h2>What it said about five YouTube strategies</h2>
<p class="mut">Each dot is one test on SPY daily bars. Green band: p below 0.05. Log scale; 0.001 is the floor at 1,000 shuffles.</p>
{''.join(svg)}
<div class="tw"><table><tr><th>Rule</th><th>Period</th><th>Profit factor</th><th>Shuffled median</th><th>p</th><th></th></tr>{trs}</table></div>
<ul>{dv}</ul>
<p>Short-term dip buying inside an uptrend survived. RSI(2), published in 2008, passed before and failed after.
The trend filter cut drawdowns but did not beat luck. <a href="https://github.com/triton-xxix/proteus-lab/blob/main/experiments/2026-10-07-P-0082/README.md">Full write-up</a>.</p>
<h2>Use it</h2>
<pre>pip install numpy
python3 luck_test.py prices.csv --rule rsi5 --perms 1000
python3 luck_test.py prices.csv --rule sma --n 200 --from 2009-01-01</pre>
<p>Repo: <a href="https://github.com/triton-xxix/proteus-luck-test">github.com/triton-xxix/proteus-luck-test</a> (MIT). <a href="luck_test.py">luck_test.py</a> needs only numpy. The CSV needs <code>date, open, high, low, close</code>; an
<code>adjclose</code> column scales prices to total return. Three rules are built in; add your own as a function returning
daily log returns. <a href="README.md">README</a>.</p>
<p class="mut">Method after neurotrader888/mcpt (MIT). No costs or slippage. Not advice. Numbers drawn from
results.json by build.py.</p>
</main></body></html>
"""
open(OUT, "w").write(page)
print("wrote", OUT, len(rows), "tests")
