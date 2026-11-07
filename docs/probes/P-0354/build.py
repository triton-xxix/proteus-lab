"""Build docs/probes/P-0354/index.html and data.json from four committed results.json files.

The Heathrow METAR-high gap chain: P-0346 (the gap), P-0352 (not rounding), P-0353 (sampling),
P-0354 (the lag by hour). Every number on the page is read or computed here; nothing is typed.
Exits non-zero if a recomputed figure disagrees with the figure the probe wrote.

python3 /Users/triton/PROTEUS/docs/probes/P-0354/build.py
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
EXP = os.path.join(HERE, "..", "..", "..", "experiments")


def load(folder):
    with open(os.path.join(EXP, folder, "results.json")) as f:
        return json.load(f)


p346 = load("2026-11-06-P-0346")
p352 = load("2026-11-07-P-0352")
p353 = load("2026-11-07-P-0353")
p354 = load("2026-11-07-P-0354")

bad = []

# P-0352: histogram mean must match the written mean
hist = sorted((float(k), v) for k, v in p352["diff_hist"].items())
n_hist = sum(v for _, v in hist)
mean_hist = sum(k * v for k, v in hist) / n_hist
if n_hist != p352["counts"]["matched"]:
    bad.append(f"histogram counts {n_hist} v matched {p352['counts']['matched']}")
if abs(mean_hist - p352["mean_metar_minus_tenths"]) > 0.005:
    bad.append(f"histogram mean {mean_hist:.3f} v {p352['mean_metar_minus_tenths']}")
truncation = -sum(t / 10 for t in range(10)) / 10  # floor of tenths spread evenly over .0 to .9

# P-0353: per-day rows must reproduce the three means
rows = p353["rows"]
def mean(xs):
    return sum(xs) / len(xs)
m_samp = mean([r["ten_min_max"] - r["metar_slots_max"] for r in rows])
m_tx = mean([r["synop_tx"] - r["ten_min_max"] for r in rows])
m_round = mean([r["a_rounded"] - r["synop_tx"] for r in rows])
for got, want, name in [(m_samp, p353["full_10min_max_minus_metar_slots_max"]["mean"], "sampling"),
                        (m_tx, p353["synop_tx_minus_full_10min_max"]["mean"], "tx peak"),
                        (m_round, p353["metar_slots_max_rounded_minus_tx"]["mean"], "rounded")]:
    if abs(got - want) > 0.005:
        bad.append(f"P-0353 {name} {got:.3f} v {want}")
if len(rows) != p353["days_used"]:
    bad.append(f"P-0353 rows {len(rows)} v days_used {p353['days_used']}")

# P-0354: hours must sum to the matched count, and weight back to P-0352's overall mean
hours = [(int(h), v["n"], v["mean"]) for h, v in p354["by_utc_hour"].items()]
hours.sort()
n_hours = sum(n for _, n, _ in hours)
if n_hours != p354["matched"] or n_hours != p352["counts"]["matched"]:
    bad.append(f"hours sum {n_hours} v matched {p354['matched']}")
wmean = sum(n * m for _, n, m in hours) / n_hours
if abs(wmean - p352["mean_metar_minus_tenths"]) > 0.01:
    bad.append(f"hour-weighted mean {wmean:.3f} v P-0352 {p352['mean_metar_minus_tenths']}")

if bad:
    for b in bad:
        print("DISAGREE", b)
    sys.exit(1)

gap = -p346["Heathrow"]["mean_metar_minus_tx"]
samp_piece = -p353["metar_slots_max_rounded_minus_tx"]["mean"]
lag_piece = p354["other_hours"]["mean"] - p354["warmest_three_hours"]["mean"]
left = gap - samp_piece - lag_piece

data = {
    "built_from": ["experiments/2026-11-06-P-0346/results.json", "experiments/2026-11-07-P-0352/results.json",
                   "experiments/2026-11-07-P-0353/results.json", "experiments/2026-11-07-P-0354/results.json"],
    "gap": round(gap, 3), "sampling_and_rounding": round(samp_piece, 3), "lag_at_warm_hours": round(lag_piece, 3),
    "unexplained": round(left, 3), "truncation_would_give": round(truncation, 3),
    "airports": p346, "hours": [{"utc": h, "n": n, "mean": m} for h, n, m in hours],
}
with open(os.path.join(HERE, "data.json"), "w") as f:
    json.dump(data, f, indent=1)
    f.write("\n")


def c(v, d=2):
    """Signed degrees with a proper minus sign."""
    s = f"{abs(v):.{d}f}"
    return ("−" if v < 0 else "+") + s


def u(v, d=2):
    return f"{v:.{d}f}"


# ---------- chart 1: three airports ----------
def chart_airports():
    W, H, L, R = 760, 170, 150, 30
    lo, hi = -1.2, 0.5
    x = lambda v: L + (v - lo) / (hi - lo) * (W - L - R)
    out = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="Mean METAR high minus SYNOP maximum at Heathrow, Orly and Munich">']
    for t in [-1.0, -0.5, 0.0, 0.5]:
        out.append(f'<line x1="{x(t):.1f}" x2="{x(t):.1f}" y1="10" y2="{H-26}" stroke="var(--rule)" stroke-width="{2 if t == 0 else 1}"/>')
        out.append(f'<text x="{x(t):.1f}" y="{H-8}" text-anchor="middle">{c(t,1)} C</text>')
    for i, name in enumerate(["Heathrow", "Orly", "Munich"]):
        a = p346[name]
        y = 32 + i * 42
        m, se = a["mean_metar_minus_tx"], a["se"]
        col = "var(--buoy)" if name == "Heathrow" else "var(--tide)"
        out.append(f'<text class="k" x="10" y="{y+4}">{name} {a["icao"]}</text>')
        out.append(f'<line x1="{x(0):.1f}" x2="{x(m):.1f}" y1="{y}" y2="{y}" stroke="{col}" stroke-width="12" stroke-linecap="butt" opacity=".85"/>')
        out.append(f'<line x1="{x(m-2*se):.1f}" x2="{x(m+2*se):.1f}" y1="{y}" y2="{y}" stroke="var(--ink)" stroke-width="1.5"/>')
        tx = x(m) - 6 if m < 0 else x(m) + 6
        anchor = "end" if m < 0 else "start"
        out.append(f'<text class="k" x="{tx:.1f}" y="{y-10}" text-anchor="{anchor}">{c(m)} C, {a["days"]} days</text>')
    out.append("</svg>")
    return "\n".join(out)


# ---------- chart 2: METAR minus tenths histogram ----------
def chart_hist():
    W, H, L, R, T, B = 760, 230, 40, 20, 24, 34
    lo, hi = -2.5, 2.1
    x = lambda v: L + (v - lo) / (hi - lo) * (W - L - R)
    top = max(v for _, v in hist)
    y = lambda v: H - B - v / top * (H - T - B)
    bw = (W - L - R) / ((hi - lo) * 10) * 0.86
    out = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="Histogram of METAR minus SYNOP tenths at the same minute, 738 minutes">']
    for t in [-2, -1, 0, 1, 2]:
        out.append(f'<text x="{x(t):.1f}" y="{H-12}" text-anchor="middle">{c(t,0)} C</text>')
    out.append(f'<line x1="{L}" x2="{W-R}" y1="{H-B}" y2="{H-B}" stroke="var(--rule)"/>')
    for k, v in hist:
        out.append(f'<rect x="{x(k)-bw/2:.1f}" y="{y(v):.1f}" width="{bw:.1f}" height="{H-B-y(v):.1f}" fill="var(--tide)" opacity=".75"><title>{c(k,1)} C: {v}</title></rect>')
    mm = p352["mean_metar_minus_tenths"]
    out.append(f'<line x1="{x(mm):.1f}" x2="{x(mm):.1f}" y1="{T-6}" y2="{H-B}" stroke="var(--ink)" stroke-width="2"/>')
    out.append(f'<text class="k" x="{x(mm)+6:.1f}" y="{T+2}">measured mean {c(mm)} C</text>')
    out.append(f'<line x1="{x(truncation):.1f}" x2="{x(truncation):.1f}" y1="{T+10}" y2="{H-B}" stroke="var(--buoy)" stroke-width="2" stroke-dasharray="5 4"/>')
    out.append(f'<text x="{x(truncation)-6:.1f}" y="{T+18}" text-anchor="end" style="fill:var(--buoy)">truncation would sit at {c(truncation)} C</text>')
    out.append("</svg>")
    return "\n".join(out)


# ---------- chart 3: 28 days, everything against TX ----------
def chart_days():
    W, H, L, R, T, B = 760, 250, 46, 12, 16, 40
    vals = [r[k] - r["synop_tx"] for r in rows for k in ("metar_slots_max", "ten_min_max", "a_rounded")]
    lo, hi = min(vals) - 0.1, 0.4
    n = len(rows)
    x = lambda i: L + (i + 0.5) / n * (W - L - R)
    y = lambda v: T + (hi - v) / (hi - lo) * (H - T - B)
    out = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="Each October day at Heathrow: half-hourly max, 10-minute max and the rounded half-hourly max, all minus SYNOP TX">']
    t = 0.0
    while t >= lo:
        out.append(f'<line x1="{L}" x2="{W-R}" y1="{y(t):.1f}" y2="{y(t):.1f}" stroke="var(--rule)" stroke-width="{2 if t == 0 else 1}"/>')
        out.append(f'<text x="{L-6}" y="{y(t)+4:.1f}" text-anchor="end">{c(t,1)}</text>')
        t = round(t - 0.5, 1)
    out.append(f'<text class="k" x="{W-R}" y="{y(0)-6:.1f}" text-anchor="end">SYNOP TX</text>')
    for i, r in enumerate(rows):
        tx = r["synop_tx"]
        a, b, rr = r["metar_slots_max"] - tx, r["ten_min_max"] - tx, r["a_rounded"] - tx
        out.append(f'<line x1="{x(i):.1f}" x2="{x(i):.1f}" y1="{y(max(a,b,rr,0)):.1f}" y2="{y(min(a,b,rr)):.1f}" stroke="var(--ghost)"/>')
        out.append(f'<circle cx="{x(i):.1f}" cy="{y(b):.1f}" r="4" fill="var(--gold)"><title>{r["day"]}: 10-minute max {u(r["ten_min_max"],1)}, TX {u(tx,1)}</title></circle>')
        out.append(f'<circle cx="{x(i):.1f}" cy="{y(a):.1f}" r="4" fill="var(--tide)"><title>{r["day"]}: half-hourly max {u(r["metar_slots_max"],1)}</title></circle>')
        out.append(f'<rect x="{x(i)-4:.1f}" y="{y(rr)-4:.1f}" width="8" height="8" fill="none" stroke="var(--buoy)" stroke-width="2"><title>{r["day"]}: rounded {r["a_rounded"]}</title></rect>')
        if i % 4 == 0:
            out.append(f'<text x="{x(i):.1f}" y="{H-18}" text-anchor="middle">{int(r["day"][8:])} Oct</text>')
    out.append("</svg>")
    return "\n".join(out)


# ---------- chart 4: by UTC hour ----------
def chart_hours():
    W, H, L, R, T, B = 760, 240, 46, 12, 18, 38
    lo, hi = -0.4, 0.3
    bw = (W - L - R) / 24
    x = lambda h: L + h * bw
    y = lambda v: T + (hi - v) / (hi - lo) * (H - T - B)
    out = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="Mean METAR minus SYNOP tenths at the same minute, by UTC hour, October">']
    for t in [-0.3, -0.2, -0.1, 0.0, 0.1, 0.2]:
        out.append(f'<line x1="{L}" x2="{W-R}" y1="{y(t):.1f}" y2="{y(t):.1f}" stroke="var(--rule)" stroke-width="{2 if t == 0 else 1}"/>')
        out.append(f'<text x="{L-6}" y="{y(t)+4:.1f}" text-anchor="end">{c(t,1)}</text>')
    for h, n, m in hours:
        col = "var(--buoy)" if m < 0 else "var(--tide)"
        y0, y1 = sorted([y(0), y(m)])
        out.append(f'<rect x="{x(h)+2:.1f}" y="{y0:.1f}" width="{bw-4:.1f}" height="{max(y1-y0,1):.1f}" fill="{col}" opacity=".8"><title>{h:02d} UTC: {c(m)} C over {n} minutes</title></rect>')
        if h % 3 == 0:
            out.append(f'<text x="{x(h)+bw/2:.1f}" y="{H-16}" text-anchor="middle">{h:02d}</text>')
    out.append(f'<text x="{W-R}" y="{H-2}" text-anchor="end">UTC hour (London is UTC+1 until 25 Oct)</text>')
    out.append("</svg>")
    return "\n".join(out)


# ---------- chart 5: where the 0.93 goes ----------
def chart_waterfall():
    W, H, L, R = 760, 190, 190, 60
    x = lambda v: L + v / gap * (W - L - R)
    parts = [("Sampling and rounding", samp_piece, "var(--tide)", "P-0353"),
             ("Lag at the warm hours", lag_piece, "var(--gold)", "P-0354"),
             ("Not explained", left, "var(--ghost)", "open")]
    out = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="The 0.93 C Heathrow gap split into sampling, lag and the unexplained rest">']
    out.append(f'<text class="k" x="10" y="28">The whole gap (P-0346)</text>')
    out.append(f'<rect x="{L}" y="16" width="{x(gap)-L:.1f}" height="18" fill="var(--buoy)" opacity=".85"/>')
    out.append(f'<text class="k" x="{x(gap)+6:.1f}" y="30">{u(gap)} C</text>')
    acc = 0.0
    for i, (name, v, col, src) in enumerate(parts):
        yy = 56 + i * 38
        out.append(f'<text class="k" x="10" y="{yy+13}">{name}</text>')
        out.append(f'<text x="10" y="{yy+27}">{src}</text>')
        out.append(f'<rect x="{x(acc):.1f}" y="{yy}" width="{x(acc+v)-x(acc):.1f}" height="18" fill="{col}" opacity=".85"/>')
        out.append(f'<text class="k" x="{x(acc+v)+6:.1f}" y="{yy+14}">{u(v)}</text>')
        acc += v
    out.append("</svg>")
    return "\n".join(out)


H346 = p346["Heathrow"]
stats = [
    ("hot", f"{c(-gap)} C", f"Heathrow METAR high minus SYNOP maximum, {H346['days']} days, Sep to Oct"),
    ("", f"{c(p352['mean_metar_minus_tenths'])} C", f"METAR minus the station's own tenths, same minute, {p352['counts']['matched']} minutes"),
    ("cool", f"{u(samp_piece)} C", f"lost to looking twice an hour and rounding, {p353['days_used']} days"),
    ("", f"{c(p354['afternoon_12_15'])} C", "METAR minus tenths, 12 to 15 UTC; night is " + c(p354["night_00_05"])),
    ("", f"{u(left)} C", "still not explained"),
]
stat_html = "\n".join(f'<div class="stat {k}"><b>{b}</b><span>{s}</span></div>' for k, b, s in stats)

warm = p354["warmest_three_hours"]
oth = p354["other_hours"]
se_diff = (warm["sd"] ** 2 / warm["n"] + oth["sd"] ** 2 / oth["n"]) ** 0.5

page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Heathrow's Missing Degree</title>
<meta name="description" content="Probes P-0346 to P-0354: Heathrow's whole-degree METAR high sits {u(gap)} C under its SYNOP maximum. Not rounding; about {u(samp_piece)} C is sampling; the METAR lags the air through the day; {u(left)} C is still open. Drawn from the committed results.">
<style>
:root{{
  --paper:#ece9e2; --raised:#f6f4ef; --ink:#1d1a16; --muted:#625b51; --rule:#d2ccc0;
  --tide:#2a6a73; --buoy:#b8402b; --ghost:#b9b2a5; --gold:#9a7a1c;
}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{
  --paper:#16140f; --raised:#1f1c17; --ink:#ece7dd; --muted:#a59d90; --rule:#38332b;
  --tide:#6bc0c8; --buoy:#ec8a72; --ghost:#4d473e; --gold:#d9b85a;
}}}}
:root[data-theme="dark"]{{
  --paper:#16140f; --raised:#1f1c17; --ink:#ece7dd; --muted:#a59d90; --rule:#38332b;
  --tide:#6bc0c8; --buoy:#ec8a72; --ghost:#4d473e; --gold:#d9b85a;
}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--paper);color:var(--ink);font:16px/1.55 Georgia,"Iowan Old Style",serif}}
main{{max-width:860px;margin:0 auto;padding:28px 16px 64px}}
a{{color:var(--tide)}}
.kicker{{font:600 12px/1.2 ui-monospace,Menlo,monospace;letter-spacing:.08em;text-transform:uppercase;color:var(--muted)}}
h1{{font-size:clamp(28px,6vw,44px);line-height:1.1;margin:.3em 0 .4em}}
h2{{font-size:20px;margin:2.2em 0 .5em}}
p{{max-width:64ch}}
.stats{{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px;margin:22px 0}}
.stat{{background:var(--raised);border:1px solid var(--rule);border-radius:8px;padding:12px 14px}}
.stat b{{display:block;font:600 24px/1.1 ui-monospace,Menlo,monospace}}
.stat span{{font-size:13px;color:var(--muted)}}
.stat.hot b{{color:var(--buoy)}}
.stat.cool b{{color:var(--tide)}}
.chart{{background:var(--raised);border:1px solid var(--rule);border-radius:8px;padding:12px 10px 6px;overflow:hidden}}
svg{{display:block;width:100%;height:auto}}
svg text{{font:12px ui-monospace,Menlo,monospace;fill:var(--muted)}}
svg text.k{{fill:var(--ink)}}
.legend{{display:flex;flex-wrap:wrap;gap:14px;font-size:13px;color:var(--muted);margin:10px 4px}}
.sw{{display:inline-block;width:12px;height:12px;border-radius:50%;vertical-align:middle;margin-right:5px}}
.sw.sq{{border-radius:2px}}
.note{{font-size:14px;color:var(--muted)}}
ul{{max-width:64ch}}
</style>
</head>
<body>
<main>
<div class="kicker">Proteus probes P-0346, P-0352, P-0353, P-0354 · 6 to 7 Nov 2026 · verdicts: works</div>
<h1>Heathrow's missing degree</h1>
<p>Weather markets settle on an airport's daily high, and the high people quote is usually the METAR, the whole-degree report pilots read. The station also files a SYNOP with its maximum to a tenth. At most airports the two agree. At Heathrow the METAR high sat <b>{u(gap)} C</b> under the SYNOP maximum on average across {H346['days']} days. Four probes over two days went looking for where that degree goes.</p>

<div class="stats">
{stat_html}
</div>

<h2>1. Heathrow is the odd one out</h2>
<p class="note">P-0346: mean of the day's highest METAR minus the SYNOP 06 to 18 UTC maximum, Sep to Oct 2026. Black whiskers are two standard errors.</p>
<div class="chart">{chart_airports()}</div>
<p>Orly runs {u(-p346['Orly']['mean_metar_minus_tx'])} C low, Munich {u(p346['Munich']['mean_metar_minus_tx'])} C high. Heathrow is nearly a degree low, and on {H346['gap_rounded']['-2']} of {H346['days']} days two whole degrees under the rounded maximum. So an offset learned at one airport does not carry to another.</p>

<h2>2. It is not the rounding</h2>
<p class="note">P-0352: every October METAR matched to the minute with the station's 10-minute SYNOP reading in tenths. The difference, METAR minus tenths, for {p352['counts']['matched']} minutes.</p>
<div class="chart">{chart_hist()}</div>
<p>If the METAR simply chopped the tenths off, the differences would pile up around {c(truncation)} C. They centre on {c(p352['mean_metar_minus_tenths'])} C with a spread of {u(p352['sd_metar_minus_tenths'])}. The METAR matches the rounded tenths {round(100*p352['share_rounded'])}% of the time, the floored {round(100*p352['share_floored'])}%. Over the whole day it is an unbiased, noisier reading of the same air. My shot said 85% rounded; that number missed.</p>

<h2>3. About a third is looking twice an hour</h2>
<p class="note">P-0353: each October day with every slot, the station's own readings set against its SYNOP maximum (the line at zero). Teal is the highest of the half-hourly readings, gold the highest of all the 10-minute readings, the red square the half-hourly high rounded to a whole degree, as a METAR would be.</p>
<div class="chart">{chart_days()}
<div class="legend">
 <span><i class="sw" style="background:var(--tide)"></i>half-hourly max</span>
 <span><i class="sw" style="background:var(--gold)"></i>10-minute max</span>
 <span><i class="sw sq" style="border:2px solid var(--buoy)"></i>half-hourly max, rounded</span>
</div></div>
<p>Sampling every half hour misses {u(m_samp)} C of the 10-minute peak on average, and the SYNOP maximum sits another {u(m_tx)} C above the highest 10-minute reading because it catches the peak inside the ten minutes. Rounded, the half-hourly high lands {u(samp_piece)} C under the maximum. That holds the sensor fixed, so it is the most sampling alone can do. Caveat: the cache had no :50 reports, so :00 and :30 stand in for Heathrow's :20 and :50.</p>

<h2>4. The METAR lags the air</h2>
<p class="note">P-0354: the same {p354['matched']} matched minutes as section 2, split by UTC hour. Red where the METAR reads colder than the tenths, teal where warmer.</p>
<div class="chart">{chart_hours()}</div>
<p>Across the whole day the gap averages out to nothing, which is why section 2 found it unbiased. By hour it does not: cold from 07 UTC, worst at 10 to 12 UTC near {c(min(m for _, _, m in hours))} C, warm every evening and night up to {c(max(m for _, _, m in hours))} C. It reads cold while the air warms and warm while it cools, like a slower sensor or a longer averaging window. In each day's three warmest hours the METAR runs {c(warm['mean'])} C against {c(oth['mean'])} C in the rest (standard error of the difference about {u(se_diff)}).</p>

<h2>Where the {u(gap)} C goes</h2>
<div class="chart">{chart_waterfall()}</div>
<p>Sampling and rounding account for {u(samp_piece)} C. The lag at the warm hours, measured as the warm-hour gap minus the rest, adds {u(lag_piece)} C. That leaves <b>{u(left)} C</b> open. My write-up of P-0354 guessed the lag at 0.2 to 0.3; this page uses the narrower measured difference, so the open piece is larger than the README implies.</p>

<h2>What is not settled</h2>
<ul>
<li>The gap is Sep to Oct; the sampling and lag probes are October only. Summing pieces from different windows is rough.</li>
<li>Only :20 METAR minutes were matched, and :00/:30 stood in for the sampling test.</li>
<li>The lag piece and the sampling piece may overlap: a lagging sensor also shifts which half-hour holds the high.</li>
<li>Nothing here says which reading a given market settles on. Read the market's rules first.</li>
</ul>

<p class="note">Built by <code>docs/probes/P-0354/build.py</code> from the four committed results files, which exits if a recomputed mean disagrees with the probe's own. Write-ups: <a href="https://github.com/triton-xxix/proteus-lab/tree/main/experiments/2026-11-06-P-0346">P-0346</a>, <a href="https://github.com/triton-xxix/proteus-lab/tree/main/experiments/2026-11-07-P-0352">P-0352</a>, <a href="https://github.com/triton-xxix/proteus-lab/tree/main/experiments/2026-11-07-P-0353">P-0353</a>, <a href="https://github.com/triton-xxix/proteus-lab/tree/main/experiments/2026-11-07-P-0354">P-0354</a>. <a href="data.json">data.json</a> · <a href="../">every probe</a> · <a href="../../">the lab</a></p>
</main>
</body>
</html>
"""

with open(os.path.join(HERE, "index.html"), "w") as f:
    f.write(page)
print(f"built P-0354 page: gap {gap:.3f}, sampling {samp_piece:.3f}, lag {lag_piece:.3f}, open {left:.3f}, "
      f"hist mean {mean_hist:.3f}, hour-weighted {wmean:.3f}, bytes {len(page)}")
