"""Builds docs/tools/bias-check/index.html from the tool's own runs (check-*-2026-10-26.json), and exits
if they disagree with probe P-0225's results.json on any bias, se, MAE or day count.
python3 /Users/triton/PROTEUS/docs/tools/bias-check/build.py"""
import json
import sys

D = "/Users/triton/PROTEUS/docs/tools/bias-check/"
SRC = "/Users/triton/PROTEUS/experiments/2026-10-26-P-0225/results.json"
OUT = D + "index.html"
P = json.load(open(SRC))
ST = {"Muenchen-Stadt": ("stadt", "Munich town (DWD 03379)"),
      "Muenchen-Flughafen": ("flughafen", "Munich airport (DWD 01262)")}
C = {name: json.load(open(D + "check-%s-2026-10-26.json" % k)) for name, (k, _) in ST.items()}
MODELS = [("icon_seamless", "ICON"), ("ecmwf_ifs025", "ECMWF"), ("gfs_seamless", "GFS")]

bad = []
for name in ST:
    for m, _ in MODELS:
        for pw, cw in (("in_sample_15aug_12oct", "before"), ("out_of_sample_from_13oct", "after")):
            p, c = P[name][pw][m], C[name]["models"][m][cw]
            if any(p[k] != c[k] for k in ("n", "bias", "se", "mae")):
                bad.append((name, m, cw))
        if P[name]["out_of_sample_from_13oct"][m]["mae_after_plus1_correction"] != C[name]["models"][m]["after_mae_fixed"]:
            bad.append((name, m, "fixed"))
if bad:
    sys.exit("tool and probe disagree on %s" % bad)

S = C["Muenchen-Stadt"]
SI = S["models"]["icon_seamless"]
FI = C["Muenchen-Flughafen"]["models"]["icon_seamless"]
cells = [(name, m) for name in ST for m, _ in MODELS]
helps = sum(1 for n, m in cells if C[n]["models"][m]["verdict"] == "helps")
shrank = sum(1 for n, m in cells if abs(C[n]["models"][m]["after"]["bias"]) < abs(C[n]["models"][m]["before"]["bias"]))


def strip(name):
    R = C[name]
    days = R["days"]
    W, H, L, T, B = 760, 200, 40, 14, 26
    lo, hi = -4.5, 4.5
    x = lambda i: L + (W - L - 10) * i / (len(days) - 1)
    y = lambda v: T + (H - T - B) * (hi - v) / (hi - lo)
    m = R["models"]["icon_seamless"]
    split = next(i for i, d in enumerate(days) if d["day"] >= R["split"])
    o = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="ICON day-ahead error per day, {ST[name][1]}">']
    for v in (-4, -2, 0, 2, 4):
        o.append(f'<line x1="{L}" x2="{W - 10}" y1="{y(v):.1f}" y2="{y(v):.1f}" class="{"zero" if v == 0 else "grid"}"/>'
                 f'<text x="{L - 6}" y="{y(v) + 4:.1f}" class="lab">{v:+d}</text>')
    sx = (x(split - 1) + x(split)) / 2
    o.append(f'<rect x="{sx:.1f}" y="{T}" width="{W - 10 - sx:.1f}" height="{H - T - B}" class="oos"/>')
    o.append(f'<text x="{sx + 6:.1f}" y="{T + 12}" class="pt">after the bias was measured</text>')
    for i, d in enumerate(days):
        e = d["icon_seamless"] - d["obs"]
        o.append(f'<circle cx="{x(i):.1f}" cy="{y(max(lo, min(hi, e))):.1f}" r="3.2" class="{"da" if i >= split else "db"}">'
                 f'<title>{d["day"]}: ICON {d["icon_seamless"]}, observed {d["obs"]}, error {e:+.1f}</title></circle>')
    for (a, b, s, cls) in ((0, split - 1, m["before"], "mb"), (split, len(days) - 1, m["after"], "ma")):
        o.append(f'<line x1="{x(a):.1f}" x2="{x(b):.1f}" y1="{y(s["bias"]):.1f}" y2="{y(s["bias"]):.1f}" class="{cls}"/>')
        o.append(f'<text x="{x(b):.1f}" y="{y(s["bias"]) + 16:.1f}" class="ml">mean {s["bias"]:+.2f}</text>')
    for i in (0, split, len(days) - 1):
        o.append(f'<text x="{x(i):.1f}" y="{H - 8}" class="tick">{days[i]["day"][5:]}</text>')
    o.append("</svg>")
    return "".join(o)


def dumbbell():
    W, RH, L, T = 760, 30, 190, 30
    H = T + RH * len(cells) + 20
    lo, hi = -2.5, 0.5
    x = lambda v: L + (W - L - 20) * (v - lo) / (hi - lo)
    o = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="Bias before and after the split, six station and model pairs">']
    for v in (-2, -1, 0):
        o.append(f'<line x1="{x(v):.1f}" x2="{x(v):.1f}" y1="{T - 8}" y2="{H - 18}" class="{"zero" if v == 0 else "grid"}"/>'
                 f'<text x="{x(v):.1f}" y="{T - 12}" class="tick">{v:+d}°C</text>')
    for i, (n, m) in enumerate(cells):
        r = C[n]["models"][m]
        yy = T + RH * i + RH / 2
        lab = "%s, %s" % ("town" if "Stadt" in n else "airport", dict(MODELS)[m])
        b, a = r["before"]["bias"], r["after"]["bias"]
        o.append(f'<text x="{L - 10}" y="{yy + 4:.1f}" class="lab">{lab}</text>')
        o.append(f'<line x1="{x(b):.1f}" x2="{x(a):.1f}" y1="{yy:.1f}" y2="{yy:.1f}" class="bar"/>')
        o.append(f'<line x1="{x(a - 1.96 * r["after"]["se"]):.1f}" x2="{x(min(hi, a + 1.96 * r["after"]["se"])):.1f}" y1="{yy + 7:.1f}" y2="{yy + 7:.1f}" class="ci"/>')
        o.append(f'<circle cx="{x(b):.1f}" cy="{yy:.1f}" r="5" class="db"><title>{lab} before: {b:+.2f} (se {r["before"]["se"]})</title></circle>')
        o.append(f'<circle cx="{x(a):.1f}" cy="{yy:.1f}" r="5" class="da"><title>{lab} after: {a:+.2f} (se {r["after"]["se"]})</title></circle>')
    o.append("</svg>")
    return "".join(o)


rows = []
for n, m in cells:
    r = C[n]["models"][m]
    rows.append(f'<tr><td>{"town" if "Stadt" in n else "airport"}</td><td>{dict(MODELS)[m]}</td>'
                f'<td>{r["before"]["bias"]:+.2f}</td><td>{r["after"]["bias"]:+.2f} ({r["after"]["se"]})</td>'
                f'<td>{r["after"]["mae"]:.2f}</td><td>{r["after_mae_learned"]:.2f}</td>'
                f'<td class="{r["verdict"]}">{r["verdict"]}</td></tr>')

page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>Bias Check</title>
<style>
:root{{--bg:#fbfaf7;--fg:#1d1d1b;--mut:#6b6a66;--line:#e2dfd8;--b:#9c9a93;--a:#c0532f;--oos:#f3ede4;--code:#f0eee8;--ok:#2f7a4a}}
@media (prefers-color-scheme:dark){{:root{{--bg:#151514;--fg:#ecebe6;--mut:#9c9a93;--line:#33322f;--b:#6b6a66;--a:#e7845f;--oos:#211e1a;--code:#22211f;--ok:#6cc08b}}}}
body{{background:var(--bg);color:var(--fg);font:17px/1.55 Georgia,serif;margin:0}}
main{{max-width:820px;margin:0 auto;padding:32px 16px 64px}}
h1{{font-size:2.1rem;margin:.2em 0}} h2{{font-size:1.25rem;margin-top:2em}}
.k{{font:13px/1.4 ui-monospace,Menlo,monospace;color:var(--mut);text-transform:uppercase;letter-spacing:.08em}}
pre,code{{font:14px/1.5 ui-monospace,Menlo,monospace;background:var(--code)}} pre{{padding:12px;overflow-x:auto;border-radius:6px}}
svg{{width:100%;height:auto;display:block;margin:12px 0 20px}}
.lab{{font:12px ui-monospace,Menlo,monospace;fill:var(--fg);text-anchor:end}}
.tick{{font:11px ui-monospace,Menlo,monospace;fill:var(--mut);text-anchor:middle}}
.pt{{font:12px ui-sans-serif,system-ui;fill:var(--mut)}} .ml{{font:12px ui-monospace,Menlo,monospace;fill:var(--fg);text-anchor:end}}
.grid{{stroke:var(--line)}} .zero{{stroke:var(--mut)}} .oos{{fill:var(--oos)}}
.db{{fill:var(--b)}} .da{{fill:var(--a)}} .mb{{stroke:var(--b);stroke-width:2.5}} .ma{{stroke:var(--a);stroke-width:2.5}}
.bar{{stroke:var(--mut);stroke-width:2}} .ci{{stroke:var(--a);stroke-width:1.5;opacity:.45}}
.big{{font-size:1.15rem}} .sw{{display:inline-block;width:12px;height:12px;border-radius:6px;vertical-align:-1px}}
.tw{{overflow-x:auto}} table{{border-collapse:collapse;font:14px/1.4 ui-monospace,Menlo,monospace;width:100%}}
th,td{{border-bottom:1px solid var(--line);padding:6px 8px;text-align:right}} th:nth-child(-n+2),td:nth-child(-n+2){{text-align:left}}
.helps{{color:var(--ok)}} .hurts{{color:var(--a)}} a{{color:inherit}} .mut{{color:var(--mut)}}
</style></head><body><main>
<div class="k">Proteus tools · from probe P-0225</div>
<h1>Bias check</h1>
<p>Weather markets settle on a station's daily high, and the obvious edge is a model that runs cold: measure its bias,
add it back, beat the crowd. This script asks the question that comes after. Measure the bias on one stretch of days,
then see whether it is still there on the days that came later, and whether subtracting it still helps.</p>
<p class="big">In Munich town, ICON ran <b>{SI["before"]["bias"]:+.2f}°C</b> cold over {SI["before"]["n"]} days to 12 Oct.
Over the next {SI["after"]["n"]} it ran <b>{SI["after"]["bias"]:+.2f}°C</b> (se {SI["after"]["se"]}). Adding the learned
{SI["learned_correction"]:+.2f} still cut the mean error, {SI["after"]["mae"]:.2f} to {SI["after_mae_learned"]:.2f}°C.
At the airport the same move made ICON worse, {FI["after"]["mae"]:.2f} to {FI["after_mae_learned"]:.2f}.</p>
<h2>ICON's error, day by day</h2>
<p class="mut">Forecast issued the day before minus the observed high. <span class="sw" style="background:var(--b)"></span>
the days the bias was learned on, <span class="sw" style="background:var(--a)"></span> the days after; lines are the means.</p>
<h3 class="k">{ST["Muenchen-Stadt"][1]}</h3>
{strip("Muenchen-Stadt")}
<h3 class="k">{ST["Muenchen-Flughafen"][1]}</h3>
{strip("Muenchen-Flughafen")}
<p>The three warm days of 14 to 16 Oct carry most of the cold miss in town; after them ICON misses both ways.
Thirteen days cannot say whether that is the season turning or noise.</p>
<h2>Every model, both stations</h2>
<p class="mut">Bias before (grey) and after (red), with a 95% bar on the after value. {shrank} of 6 moved towards zero.</p>
{dumbbell()}
<div class="tw"><table><thead><tr><th>station</th><th>model</th><th>bias before</th><th>after (se)</th><th>MAE after</th>
<th>minus learned</th><th>correction</th></tr></thead><tbody>{"".join(rows)}</tbody></table></div>
<p>The learned correction helps in {helps} of 6. It hurts exactly where the bias was small to begin with, and
where it was big (ECMWF, both stations) it still helps. A correction you measured is a forecast too.</p>
<h2>Use it</h2>
<pre>python3 bias_check.py --lat 48.137 --lon 11.575 --tz Europe/Berlin --dwd 03379 --start 2026-08-15 --split 2026-10-13
python3 bias_check.py --lat 51.48 --lon -0.45 --meteostat 03772 --split 2026-10-01 --correct 1.0
python3 bias_check.py --lat 40.78 --lon -73.97 --csv my_station.csv --split 2026-10-01 --json out.json</pre>
<p><a href="bias_check.py">bias_check.py</a> uses only the Python standard library and no keys. Forecasts come from the
Open-Meteo previous-runs API (the hourly temperature as issued one day before, max per local day; it goes back about
three months). Observations from a DWD station, a Meteostat station anywhere, or your own CSV with date and tmax
columns. <a href="README.md">README</a>.</p>
<p class="mut">Checked: run on 26 Oct 2026 for both stations, it reproduced every bias, standard error, MAE and the +1°C
column in P-0225's results.json; build.py exits if they ever disagree. Write-up:
<a href="https://github.com/triton-xxix/proteus-lab/blob/main/experiments/2026-10-26-P-0225/README.md">P-0225</a>.
Numbers drawn from check-*.json by build.py. Not advice.</p>
</main></body></html>
"""
open(OUT, "w").write(page)
print("wrote", OUT, "| helps", helps, "of 6 | shrank", shrank, "| town ICON", SI["before"]["bias"], "->", SI["after"]["bias"])
