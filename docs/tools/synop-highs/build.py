"""Builds docs/tools/synop-highs/index.html from the tool's own runs (run-*-2026-11-04.json), and exits if
- the tool's parser, run over P-0323's saved Ogimet pulls, differs from today's fresh Heathrow run on any day, or
  finds other than P-0323's 61 days;
- fewer than 50 Strasbourg days line up with Meteo-France's own TX (P-0324's file).
City offsets are read from the committed results.json of P-0319, P-0323, P-0324 and P-0225, never typed.
python3 -I /Users/triton/PROTEUS/docs/tools/synop-highs/build.py"""
import csv
import gzip
import io
import json
import sys

R = "/Users/triton/PROTEUS/"
D = R + "docs/tools/synop-highs/"
sys.path.insert(0, D)
from synop_highs import parse  # noqa: E402

LH = json.load(open(D + "run-03772-2026-11-04.json"))
SX = json.load(open(D + "run-07190-2026-11-04.json"))
lh = {d["day"]: d["tmax"] for d in LH["days"]}
sx = {d["day"]: d["tmax"] for d in SX["days"]}

# 1. the parser over P-0323's own saved pulls must give P-0323's days, and agree with today's pull
old = {}
for mth in ("202609", "202610"):
    old.update(parse(open(R + "sandbox/ogimet-03772-%s.txt" % mth, encoding="latin-1").read(), "03772")[0])
P23 = json.load(open(R + "experiments/2026-11-04-P-0323/results.json"))
if len(old) != P23["obs_days"] or [min(old), max(old)] != P23["obs_range"]:
    sys.exit("parser on P-0323's files: %d days %s v P-0323 %d %s" % (len(old), [min(old), max(old)],
             P23["obs_days"], P23["obs_range"]))
diff = [d for d in old if lh.get(d) != old[d]]
if diff:
    sys.exit("fresh Heathrow pull differs from P-0323's on %s" % diff[:5])

# 2. Strasbourg SYNOP 06-18 UTC max v Meteo-France climate-day TX
rd = csv.DictReader(io.StringIO(gzip.decompress(open(R + "sandbox/mf-q67-latest-2025-2026.csv.gz", "rb").read())
                                .decode("latin-1")), delimiter=";")
mf = {}
for r in rd:
    if "ENTZHEIM" in r["NOM_USUEL"] and r.get("TX", "").strip():
        d = r["AAAAMMJJ"]
        mf["%s-%s-%s" % (d[:4], d[4:6], d[6:8])] = float(r["TX"].replace(",", "."))
both = sorted(d for d in sx if d in mf)
if len(both) < 50:
    sys.exit("only %d Strasbourg days line up with Meteo-France TX" % len(both))
dd = [round(sx[d] - mf[d], 1) for d in both]
n = len(dd)
same = sum(1 for x in dd if abs(x) < 0.05)
within = sum(1 for x in dd if abs(x) <= 0.5)
lower = sum(1 for x in dd if x < -0.05)
mean_d = round(sum(dd) / n, 2)
worst = min(both, key=lambda d: sx[d] - mf[d])
if same == n:
    VERDICT = ("Every day the same. I expected a few low days, since the group covers 06 to 18 UTC and a warm evening "
               "would sit outside it; in this autumn none did. The UK's group has the same window, unchecked against "
               "the Met Office's own record.")
else:
    VERDICT = ("Worst %s (%.1f v %.1f). The group covers 06 to 18 UTC; TX is the climate day, so a warm evening sits "
               "outside it." % (worst, sx[worst], mf[worst]))

# 3. ICON lead-1 offsets by city, from the probes
P19 = json.load(open(R + "experiments/2026-11-04-P-0319/results.json"))["models"]["icon_seamless"]["1"]
P24 = json.load(open(R + "experiments/2026-11-04-P-0324/results.json"))["models"]["icon_seamless"]["1"]
P25 = json.load(open(R + "experiments/2026-10-26-P-0225/results.json"))["Muenchen-Stadt"]["in_sample_15aug_12oct"]["icon_seamless"]
L1 = P23["leads"]["1"]
CITIES = [("Paris-Montsouris", "P-0319", "Meteo-France TX", P19["mean_obs_minus_fc"], P19["se"], P19["days"]),
          ("Munich town", "P-0225", "DWD TXK, 15 Aug to 12 Oct", round(-P25["bias"], 2), P25["se"], P25["n"]),
          ("Strasbourg-Entzheim", "P-0324", "Meteo-France TX", P24["mean_obs_minus_fc"], P24["se"], P24["days"]),
          ("London Heathrow", "P-0323", "Ogimet SYNOP, this tool", L1["mean_obs_minus_icon"], L1["se"], L1["days"])]


def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;")


def highs():
    days = sorted(set(lh) | set(sx))
    W, H, L, T, B = 760, 230, 40, 14, 26
    vals = [v for v in list(lh.values()) + list(sx.values())]
    lo, hi = int(min(vals)) - 1, int(max(vals)) + 2
    x = lambda i: L + (W - L - 12) * i / (len(days) - 1)
    y = lambda v: T + (H - T - B) * (hi - v) / (hi - lo)
    o = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="Daily highs from SYNOP, Heathrow and Strasbourg, {days[0]} to {days[-1]}">']
    for v in range(lo + (5 - lo % 5) % 5, hi, 5):
        o.append(f'<line x1="{L}" x2="{W - 12}" y1="{y(v):.1f}" y2="{y(v):.1f}" class="grid"/>'
                 f'<text x="{L - 6}" y="{y(v) + 4:.1f}" class="lab">{v}°</text>')
    for series, cls in ((lh, "s1"), (sx, "s2")):
        pts = " ".join(f"{x(i):.1f},{y(series[d]):.1f}" for i, d in enumerate(days) if d in series)
        o.append(f'<polyline points="{pts}" class="{cls}"/>')
        for i, d in enumerate(days):
            if d in series:
                o.append(f'<circle cx="{x(i):.1f}" cy="{y(series[d]):.1f}" r="2.4" class="d{cls}">'
                         f'<title>{d}: {series[d]:.1f}°C</title></circle>')
    for i in (0, 30, len(days) - 1):
        o.append(f'<text x="{x(i):.1f}" y="{H - 8}" class="tick">{days[i][5:]}</text>')
    o.append("</svg>")
    return "".join(o)


def strip():
    W, H, L, T, B = 760, 170, 40, 14, 26
    lo, hi = min(-3.0, min(dd) - 0.5), max(1.0, max(dd) + 0.5)
    x = lambda i: L + (W - L - 12) * i / (n - 1)
    y = lambda v: T + (H - T - B) * (hi - v) / (hi - lo)
    o = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="Strasbourg SYNOP high minus Meteo-France TX, per day">']
    for v in range(int(lo), int(hi) + 1):
        o.append(f'<line x1="{L}" x2="{W - 12}" y1="{y(v):.1f}" y2="{y(v):.1f}" class="{"zero" if v == 0 else "grid"}"/>'
                 f'<text x="{L - 6}" y="{y(v) + 4:.1f}" class="lab">{v:+d}</text>')
    for i, d in enumerate(both):
        o.append(f'<circle cx="{x(i):.1f}" cy="{y(dd[i]):.1f}" r="3" class="{"ds2" if abs(dd[i]) < 0.05 else "dlow"}">'
                 f'<title>{d}: SYNOP {sx[d]:.1f}, TX {mf[d]:.1f}, {dd[i]:+.1f}</title></circle>')
    for i in (0, n // 2, n - 1):
        o.append(f'<text x="{x(i):.1f}" y="{H - 8}" class="tick">{both[i][5:]}</text>')
    o.append("</svg>")
    return "".join(o)


def bars():
    W, RH, L, T = 760, 40, 200, 30
    H = T + RH * len(CITIES) + 12
    lo, hi = -0.25, 1.75
    x = lambda v: L + (W - L - 30) * (v - lo) / (hi - lo)
    o = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="ICON day-ahead high, observed minus forecast, four cities">']
    for v in (0, 0.5, 1.0, 1.5):
        o.append(f'<line x1="{x(v):.1f}" x2="{x(v):.1f}" y1="{T - 8}" y2="{H - 8}" class="{"zero" if v == 0 else "grid"}"/>'
                 f'<text x="{x(v):.1f}" y="{T - 12}" class="tick">{v:+.1f}°C</text>')
    for i, (name, pid, src, m, se, nd) in enumerate(CITIES):
        yy = T + RH * i + RH / 2
        o.append(f'<text x="{L - 10}" y="{yy:.1f}" class="lab">{esc(name)}</text>'
                 f'<text x="{L - 10}" y="{yy + 13:.1f}" class="lab sm">{pid}, {nd} days</text>')
        o.append(f'<rect x="{x(0):.1f}" y="{yy - 9:.1f}" width="{x(m) - x(0):.1f}" height="18" class="bar">'
                 f'<title>{esc(name)}: {m:+.2f} (se {se:.2f}, {nd} days, {esc(src)})</title></rect>')
        o.append(f'<line x1="{x(m - 2 * se):.1f}" x2="{x(m + 2 * se):.1f}" y1="{yy:.1f}" y2="{yy:.1f}" class="wh"/>')
        o.append(f'<text x="{x(m + 2 * se) + 6:.1f}" y="{yy + 4:.1f}" class="val">{m:+.2f}</text>')
    o.append("</svg>")
    return "".join(o)


rows = "".join(f"<tr><td>{esc(c[0])}</td><td>{c[1]}</td><td>{esc(c[2])}</td><td>{c[5]}</td><td>{c[3]:+.2f}</td><td>{c[4]:.2f}</td></tr>"
               for c in CITIES)
lh_days = sorted(lh)
page = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>SYNOP Highs</title>
<meta name="description" content="Daily highs for any WMO station from Ogimet's SYNOP archive, keyless and current to the day, in one stdlib Python file.">
<style>
:root{{--bg:#fbfaf7;--fg:#1d1c1a;--mut:#6b675f;--line:#dedad2;--a:#2a6f97;--b:#c4622d;--bar:#2a6f97;--card:#fff}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#151513;--fg:#ecebe6;--mut:#a29e95;--line:#34322e;--a:#6fb3d9;--b:#e8935f;--bar:#6fb3d9;--card:#1d1c1a}}}}
:root[data-theme="dark"]{{--bg:#151513;--fg:#ecebe6;--mut:#a29e95;--line:#34322e;--a:#6fb3d9;--b:#e8935f;--bar:#6fb3d9;--card:#1d1c1a}}
body{{background:var(--bg);color:var(--fg);font:16px/1.55 system-ui,-apple-system,sans-serif;margin:0}}
main{{max-width:820px;margin:0 auto;padding:24px 16px 60px}}
a{{color:var(--a)}} h1{{font-size:1.9rem;line-height:1.2;margin:.4em 0}} h2{{font-size:1.2rem;margin-top:2em}}
.mut{{color:var(--mut)}} .big{{font-size:1.15rem}}
svg{{width:100%;height:auto;display:block;margin:10px 0}}
.grid{{stroke:var(--line);stroke-width:1}} .zero{{stroke:var(--mut);stroke-width:1.3}}
.lab,.tick,.val{{fill:var(--mut);font-size:12px}} .lab{{text-anchor:end}} .tick{{text-anchor:middle}} .sm{{font-size:10.5px}}
.val{{fill:var(--fg)}}
.s1{{fill:none;stroke:var(--a);stroke-width:1.6}} .s2{{fill:none;stroke:var(--b);stroke-width:1.6}}
.ds1{{fill:var(--a)}} .ds2{{fill:var(--b)}} .dlow{{fill:var(--fg)}}
.bar{{fill:var(--bar);opacity:.8}} .wh{{stroke:var(--fg);stroke-width:1.4}}
.key span{{display:inline-block;width:12px;height:3px;vertical-align:middle;margin:0 6px 0 14px}}
pre{{background:var(--card);border:1px solid var(--line);padding:12px;overflow-x:auto;font-size:13.5px}}
table{{border-collapse:collapse;width:100%;font-size:14px}} td,th{{border-bottom:1px solid var(--line);padding:6px 4px;text-align:left}}
.tw{{overflow-x:auto}}
</style></head><body><main>
<p class="mut"><a href="../../index.html">Proteus lab</a> / tools / synop-highs</p>
<h1>Yesterday's high at any airport, without a key</h1>
<p class="big">Free observation feeds go stale: GHCN daily stops in August 2025 and Meteostat's bulk files stopped in March 2026 for Heathrow. Ogimet keeps every SYNOP report up to the hour, and the 18 UTC report carries the day's maximum. This one file turns that into a <code>date,tmax</code> CSV.</p>
<p>Run on {SX["hour"]} UTC reports on 4 Nov 2026: Heathrow (03772) and Strasbourg-Entzheim (07190), {len(lh)} days each, {lh_days[0]} to {lh_days[-1]}, no day missing.</p>
<div class="key mut"><span style="background:var(--a)"></span>Heathrow<span style="background:var(--b)"></span>Strasbourg</div>
{highs()}

<h2>Does it match the official record?</h2>
<p>At Strasbourg I have Météo-France's own daily TX for the same station (the file P-0324 used). Of {n} days, the SYNOP high is the same to the tenth on {same}, within half a degree on {within}, and lower on {lower}: mean {mean_d:+.2f}°C. {VERDICT}</p>
{strip()}
<p class="mut">SYNOP high minus TX per day. Orange: identical; dark: different. Hover a dot for the two values.</p>

<h2>What I used it for</h2>
<p>ICON's day-ahead high, observed minus forecast, at four stations. London's {L1["mean_obs_minus_icon"]:+.2f} comes from this tool's numbers; there was no other keyless 2026 source for Heathrow. Whiskers are two standard errors.</p>
{bars()}
<div class="tw"><table><tr><th>station</th><th>probe</th><th>observations</th><th>days</th><th>obs minus ICON</th><th>se</th></tr>{rows}</table></div>
<p class="mut">Munich's window is 15 Aug to 12 Oct; the rest are September and October 2026. A market on any of these highs priced straight off ICON starts half a degree to a degree and a quarter low.</p>

<h2>Use it</h2>
<pre>python3 synop_highs.py --wmo 03772 --start 2026-09 --end 2026-11 --csv heathrow.csv
python3 bias_check.py --lat 51.47 --lon -0.4543 --csv heathrow.csv --split 2026-10-15</pre>
<p>One request per month, two seconds apart; standard library only. <code>--hour</code> picks another report if your country puts its maximum elsewhere: the tool prints how many reports at that hour lacked a max group, so a wrong hour shows at once. At Heathrow {LH["missing"]} of the 18 UTC lines had none (duplicates and corrections in the feed; every day still had one). It feeds <a href="../bias-check/">bias-check</a>'s <code>--csv</code> straight in.</p>
<p><a href="synop_highs.py">synop_highs.py</a> · <a href="heathrow-2026-11-04.csv">Heathrow CSV</a> · <a href="README.md">README</a> · <a href="build.py">how this page is built</a></p>
<p class="mut">Checked: the tool's parser, run on P-0323's saved pulls, gives its {P23["obs_days"]} days, and today's fresh pull matches them on every day, or this page does not build. Not yet checked at phone width in a real browser.</p>
</main></body></html>
"""
open(D + "index.html", "w").write(page)
print("built", D + "index.html", len(page), "bytes | strasbourg", n, "days, same", same, "within 0.5", within,
      "lower", lower, "mean", mean_d, "| cities", [(c[0], c[3]) for c in CITIES])
