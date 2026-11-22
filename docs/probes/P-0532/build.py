"""Build docs/probes/P-0532/index.html and data.json from the committed results of P-0532 and P-0533,
plus the two called shots in PROBES.md.

"Most storms go unread": do en Wikipedia readers notice a geomagnetic storm? Every number on the page
is read or computed here from the 1,056 daily rows; nothing is typed. Exits non-zero if the rows
disagree with the probe's own summary or with P-0533.

python3 /Users/triton/PROTEUS/docs/probes/P-0532/build.py
"""
import json
import math
import os
import re
import statistics
import sys
from datetime import date, timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..", "..", "..")
EXP = os.path.join(ROOT, "experiments")


def load(folder):
    with open(os.path.join(EXP, folder, "results.json")) as f:
        return json.load(f)


R532 = load("2026-11-22-P-0532")
S = R532["summary"]
rows = R532["rows"]
D = load("2026-11-22-P-0533")
bad = []


def same(a, b, what):
    if a != b:
        bad.append(f"{what}: computed {a} v file {b}")


# ---------- P-0532 rows against its own summary ----------
same(len(rows), S["days"], "days")
same(rows[0]["day"], S["first"], "first day")
same(rows[-1]["day"], S["last"], "last day")
kp = {r["day"]: r["kp_max"] for r in rows}
storm = [r for r in rows if r["kp_max"] >= 7]
storm5 = [r for r in rows if r["kp_max"] >= 5]
caught = [r for r in storm if r["spike"] or r["spike_next"]]
same(len(storm), S["kp7_days"], "Kp 7+ days")
same(len(caught), S["kp7_with_spike_same_or_next"], "Kp 7+ caught")
same(len(storm5), S["kp5_days"], "Kp 5+ days")
same(sum(1 for r in storm5 if r["spike"] or r["spike_next"]), S["kp5_with_spike_same_or_next"], "Kp 5+ caught")
spike_rows = [r for r in rows if r["spike"]]
same(len(spike_rows), S["view_spike_days"], "view spike days")


def prev_kp(d):
    return kp.get((date.fromisoformat(d) - timedelta(1)).isoformat(), 0)


stormy_spikes = [r for r in spike_rows if max(r["kp_max"], prev_kp(r["day"])) >= 5]
calm_spikes = [r for r in spike_rows if max(r["kp_max"], prev_kp(r["day"])) < 5]
same(len(stormy_spikes), S["spike_days_with_kp5_same_or_previous_day"], "spikes near Kp 5+")
same(len(calm_spikes), S["false_alarm_spikes_calm"], "calm spikes")
nx = [r for r in rows if r["next_views"] is not None]
c_next = round(statistics.correlation([r["kp_max"] for r in nx], [r["next_views"] for r in nx]), 3)
same(c_next, S["corr_kp_next_day_views"], "next-day correlation")
c_same = round(statistics.correlation([r["kp_max"] for r in rows], [r["views"] for r in rows]), 3)
same(c_same, S["corr_same_day_kp_views"], "same-day correlation")

# ---------- the chain: P-0533 starts from P-0532's numbers ----------
same(D["kp7_days"], len(storm), "P-0533 Kp 7+ days")
same(D["caught_aurora_only"], len(caught), "P-0533 Aurora caught")
same(D["calm_spikes_aurora"], len(calm_spikes), "P-0533 Aurora calm spikes")
hints = D["calm_aurora_spike_hints"]
named = {d: h for d, h in hints.items() if "error" not in h}
refused = sorted(d for d, h in hints.items() if "error" in h)
same(sorted(hints), sorted(r["day"] for r in calm_spikes), "P-0533 hint dates are the calm spikes")
big = sorted(r["day"] for r in rows if r["kp_max"] >= 8)


def days_after_big(d):
    dd = date.fromisoformat(d)
    back = [(dd - date.fromisoformat(b)).days for b in big if b <= d]
    return min(back) if back else None


tails = {d: days_after_big(d) for d in named}
n_tail = sum(1 for v in tails.values() if v is not None and v <= 5)

# ---------- the called shots, from PROBES.md ----------
with open(os.path.join(ROOT, "PROBES.md")) as f:
    md = f.read().splitlines()
row532 = next((ln for ln in md if "| P-0532 |" in ln), "")
row533 = next((ln for ln in md if "| P-0533 |" in ln), "")
m1 = re.search(r"Shot said (\d+) percent and ([\d.]+)", row532)
m2 = re.search(r"Shot said (\d+) caught and (\d+) more calm spikes", row533)
if not m1 or not m2:
    bad.append("called shot for P-0532 or P-0533 not found in PROBES.md")
m3 = re.search(r"7 of the 8 named calm Aurora spikes are tails within five days", row533)
if not m3:
    bad.append("P-0533 tail claim not found in PROBES.md")

if bad:
    for b in bad:
        print("DISAGREE", b)
    sys.exit(1)

# P-0533 wrote "7 of the 8"; the rows give 6 (19 May 2024 is 8 days after the 11 May peak).
# The page carries the computed figure and names the correction; it fails only if the count moves again.
CLAIMED_TAILS = 7
if len(named) != 8 or n_tail != 6:
    print(f"DISAGREE tails: computed {n_tail} of {len(named)}, the page's correction expects 6 of 8")
    sys.exit(1)
not_tails = sorted(d for d in named if not (tails[d] is not None and tails[d] <= 5))

shot_rate, shot_corr = int(m1.group(1)), float(m1.group(2))
shot_caught, shot_more = int(m2.group(1)), int(m2.group(2))
rate = len(caught) / len(storm) * 100
rate5 = S["kp5_with_spike_same_or_next"] / len(storm5) * 100
precision = len(stormy_spikes) / len(spike_rows) * 100
top = max(rows, key=lambda r: r["views"])
top_ratio = top["views"] / top["median30"]
median_all = statistics.median(r["views"] for r in rows)
missed = [r for r in storm if not (r["spike"] or r["spike_next"])]


def peak_ratio(r):
    vs = [v for v in (r["views"], r["next_views"]) if v is not None]
    return max(vs) / r["median30"]


quiet_storm = min(missed, key=peak_ratio)
geo_more = D["calm_spikes_either"] - D["calm_spikes_aurora"]  # the shot was for adding the second article

data = {
    "built_from": ["experiments/2026-11-22-P-0532/results.json", "experiments/2026-11-22-P-0533/results.json", "PROBES.md"],
    "days": len(rows), "first": rows[0]["day"], "last": rows[-1]["day"],
    "kp7_days": len(storm), "kp7_caught_aurora": len(caught), "kp7_caught_pct": round(rate, 1),
    "kp5_days": len(storm5), "kp5_caught": S["kp5_with_spike_same_or_next"],
    "spike_days": len(spike_rows), "spikes_near_kp5": len(stormy_spikes), "calm_spikes": len(calm_spikes),
    "corr_next_day": c_next, "top_day": top["day"], "top_views": top["views"], "top_ratio": round(top_ratio, 1),
    "geomagnetic": {"caught": D["caught_geomagnetic_only"], "calm": D["calm_spikes_geomagnetic"]},
    "either": {"caught": D["caught_either"], "calm": D["calm_spikes_either"]},
    "named_calm": len(named), "tails_within_5_days": n_tail, "refused_429": refused,
    "shots": {"P-0532": {"pct": shot_rate, "corr": shot_corr}, "P-0533": {"caught": shot_caught, "more_calm": shot_more}},
    "storm_rows": len(storm),
}
with open(os.path.join(HERE, "data.json"), "w") as f:
    json.dump(data, f, indent=1)
    f.write("\n")

d0 = date.fromisoformat(rows[0]["day"])
ndays = len(rows)


# ---------- chart 1: three years of views and Kp ----------
def chart_years():
    W, L, R = 760, 52, 14
    VT, VH = 14, 190      # views panel
    KT, KH = 232, 70      # Kp panel
    H = KT + KH + 40
    x = lambda d: L + (date.fromisoformat(d) - d0).days / (ndays - 1) * (W - L - R)
    lo, hi = 1000, 400000
    yv = lambda v: VT + (math.log10(hi) - math.log10(max(v, lo))) / (math.log10(hi) - math.log10(lo)) * VH
    yk = lambda k: KT + KH - k / 9 * KH
    out = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="Daily en Wikipedia views of Aurora on a log scale over {ndays} days, above the daily maximum Kp, with the {len(storm)} days of Kp 7 or more marked">']
    for g in (1000, 3000, 10000, 30000, 100000, 300000):
        out.append(f'<line x1="{L}" x2="{W-R}" y1="{yv(g):.1f}" y2="{yv(g):.1f}" stroke="var(--rule)"/>')
        out.append(f'<text x="{L-6}" y="{yv(g)+4:.1f}" text-anchor="end">{g//1000}k</text>')
    for y in (2024, 2025, 2026):
        xx = x(f"{y}-01-01")
        out.append(f'<line x1="{xx:.1f}" x2="{xx:.1f}" y1="{VT}" y2="{KT+KH}" stroke="var(--rule)" stroke-dasharray="2 4"/>')
        out.append(f'<text x="{xx+4:.1f}" y="{KT+KH+18}">{y}</text>')
    for r in storm:
        xx = x(r["day"])
        col = "var(--aurora)" if (r["spike"] or r["spike_next"]) else "var(--buoy)"
        out.append(f'<line x1="{xx:.1f}" x2="{xx:.1f}" y1="{VT}" y2="{VT+VH}" stroke="{col}" stroke-opacity=".35" stroke-width="2"/>')
    med = " ".join(f"{x(r['day']):.1f},{yv(r['median30']*2):.1f}" for r in rows if r["median30"])
    out.append(f'<polyline points="{med}" fill="none" stroke="var(--gold)" stroke-width="1.2" stroke-dasharray="4 3"/>')
    pts = " ".join(f"{x(r['day']):.1f},{yv(r['views']):.1f}" for r in rows)
    out.append(f'<polyline points="{pts}" fill="none" stroke="var(--ink)" stroke-width="1"/>')
    for r in spike_rows:
        out.append(f'<circle cx="{x(r["day"]):.1f}" cy="{yv(r["views"]):.1f}" r="2.6" fill="var(--aurora)"><title>spike {r["day"]}: {r["views"]:,} views, median {r["median30"]:,.0f}, Kp {r["kp_max"]:.1f}</title></circle>')
    out.append(f'<text class="k" x="{x(top["day"])+8:.1f}" y="{yv(top["views"])+4:.1f}">{top["views"]:,} views, {top["day"]}</text>')
    out.append(f'<text x="{W-R}" y="{VT+VH+14}" text-anchor="end">dashed gold: twice the 30-day median, the spike line</text>')
    for k in (0, 5, 7, 9):
        out.append(f'<line x1="{L}" x2="{W-R}" y1="{yk(k):.1f}" y2="{yk(k):.1f}" stroke="var(--rule)"/>')
        out.append(f'<text x="{L-6}" y="{yk(k)+4:.1f}" text-anchor="end">Kp {k}</text>')
    bw = (W - L - R) / ndays + 0.3
    for r in rows:
        k = r["kp_max"]
        if k < 4:
            continue
        col = "var(--buoy)" if k >= 7 else ("var(--tide)" if k >= 5 else "var(--ghost)")
        out.append(f'<rect x="{x(r["day"]):.1f}" y="{yk(k):.1f}" width="{bw:.2f}" height="{yk(0)-yk(k):.1f}" fill="{col}"/>')
    out.append("</svg>")
    return "\n".join(out)


# ---------- chart 2: the 28 storm days ----------
def chart_storms():
    W, L, R, T = 760, 150, 96, 30
    H = T + len(storm) * 20 + 34
    lo, hi = 0.5, 120
    x = lambda v: L + (math.log10(v) - math.log10(lo)) / (math.log10(hi) - math.log10(lo)) * (W - L - R)
    out = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="For each of the {len(storm)} days with Kp 7 or more, the larger of that day and the next day Aurora views as a multiple of the 30-day median, against the spike line at twice">']
    for g in (0.5, 1, 2, 5, 10, 30, 100):
        out.append(f'<line x1="{x(g):.1f}" x2="{x(g):.1f}" y1="{T-8}" y2="{H-30}" stroke="var(--rule)"/>')
        out.append(f'<text x="{x(g):.1f}" y="{H-12}" text-anchor="middle">{g:g}×</text>')
    out.append(f'<line x1="{x(2):.1f}" x2="{x(2):.1f}" y1="{T-8}" y2="{H-30}" stroke="var(--gold)" stroke-width="2" stroke-dasharray="6 4"/>')
    out.append(f'<text class="k" x="{x(2)+6:.1f}" y="{T-14}">twice the median: a spike</text>')
    for i, r in enumerate(storm):
        yy = T + 8 + i * 20
        pr = peak_ratio(r)
        hit = r["spike"] or r["spike_next"]
        col = "var(--aurora)" if hit else "var(--buoy)"
        out.append(f'<text x="{L-10}" y="{yy+4}" text-anchor="end">{r["day"]} · Kp {r["kp_max"]:.1f}</text>')
        out.append(f'<line x1="{x(1):.1f}" x2="{x(pr):.1f}" y1="{yy}" y2="{yy}" stroke="{col}" stroke-width="3"/>')
        out.append(f'<circle cx="{x(pr):.1f}" cy="{yy}" r="5" fill="{col}"><title>storm {r["day"]}: Kp {r["kp_max"]:.2f}, peak {pr:.2f} times the median</title></circle>')
        out.append(f'<text class="k" x="{W-R+8}" y="{yy+4}">{pr:.1f}× {"read" if hit else "unread"}</text>')
    out.append("</svg>")
    return "\n".join(out)


# ---------- chart 3: two articles as detectors ----------
def chart_detectors():
    arts = [("Aurora", D["caught_aurora_only"], D["calm_spikes_aurora"]),
            ("Geomagnetic storm", D["caught_geomagnetic_only"], D["calm_spikes_geomagnetic"]),
            ("either", D["caught_either"], D["calm_spikes_either"])]
    W, L, R, T = 760, 150, 30, 34
    H = T + len(arts) * 58 + 30
    top = 50
    x = lambda v: L + v / top * (W - L - R)
    out = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="Storm days caught out of {len(storm)} and spikes on calm days, for Aurora, Geomagnetic storm and either article">']
    for g in range(0, top + 1, 10):
        out.append(f'<line x1="{x(g):.1f}" x2="{x(g):.1f}" y1="{T-10}" y2="{H-28}" stroke="var(--rule)"/>')
        out.append(f'<text x="{x(g):.1f}" y="{H-10}" text-anchor="middle">{g}</text>')
    out.append(f'<line x1="{x(len(storm)):.1f}" x2="{x(len(storm)):.1f}" y1="{T-10}" y2="{H-28}" stroke="var(--gold)" stroke-width="2" stroke-dasharray="6 4"/>')
    out.append(f'<text class="k" x="{x(len(storm)):.1f}" y="{T-16}" text-anchor="middle">all {len(storm)} storm days</text>')
    for i, (name, c, f_) in enumerate(arts):
        yy = T + i * 58
        out.append(f'<text class="k" x="{L-10}" y="{yy+18}" text-anchor="end">{name}</text>')
        out.append(f'<rect x="{x(0):.1f}" y="{yy+4}" width="{x(c)-x(0):.1f}" height="16" fill="var(--aurora)"><title>detector {name}: caught {c} of {len(storm)}</title></rect>')
        out.append(f'<text x="{x(c)+6:.1f}" y="{yy+17}">{c} caught</text>')
        out.append(f'<rect x="{x(0):.1f}" y="{yy+24}" width="{x(f_)-x(0):.1f}" height="16" fill="var(--buoy)"><title>detector {name}: {f_} calm-day spikes</title></rect>')
        out.append(f'<text x="{x(f_)+6:.1f}" y="{yy+37}">{f_} calm-day spikes</text>')
    out.append("</svg>")
    return "\n".join(out)


def nice(d):
    return date.fromisoformat(d).strftime("%-d %b %Y")


hint_rows = []
for d in sorted(named):
    h = named[d]
    sky = ", ".join(f"{a.replace('_', ' ')} ({v:,})" for a, v in h["sky_related"])
    t = tails[d]
    tail = f"{t} days after a Kp 8+ day" if t is not None and t <= 5 else "no Kp 8+ day in the five before"
    hint_rows.append(f'<tr><td>{nice(d)}</td><td>{tail}</td><td class="w">{sky}</td></tr>')
hint_html = "\n".join(hint_rows)

shot_rows = "\n".join([
    f'<tr><td>P-0532</td><td>Kp 7+ days with a spike</td><td class="n">{shot_rate}%</td><td class="n">{rate:.0f}% ({len(caught)} of {len(storm)})</td><td class="n">{shot_rate - rate:.0f} points high</td></tr>',
    f'<tr><td>P-0532</td><td>Kp v next-day views, correlation</td><td class="n">{shot_corr}</td><td class="n">{c_next}</td><td class="n">{(shot_corr - c_next) / shot_corr * 100:.0f}% too high</td></tr>',
    f'<tr><td>P-0533</td><td>Kp 7+ days caught by Geomagnetic storm</td><td class="n">{shot_caught}</td><td class="n">{D["caught_geomagnetic_only"]}</td><td class="n">{D["caught_geomagnetic_only"] - shot_caught} low</td></tr>',
    f'<tr><td>P-0533</td><td>extra calm-day spikes from adding it (either v Aurora)</td><td class="n">{shot_more}</td><td class="n">{geo_more}</td><td class="n">{geo_more / shot_more:.1f} times</td></tr>',
])

stats = [
    ("hot", f"{len(caught)} of {len(storm)}", f"days of Kp 7 or more that drew an Aurora view spike that day or the next ({rate:.0f}%)"),
    ("", f"{S['kp5_with_spike_same_or_next']} of {len(storm5)}", f"for Kp 5 or more ({rate5:.0f}%): most storms go unread"),
    ("", f"{len(stormy_spikes)} of {len(spike_rows)}", f"Aurora spikes within a day of Kp 5+ ({precision:.0f}%); {len(calm_spikes)} came on calm days"),
    ("hot", f"{D['caught_geomagnetic_only']} of {len(storm)}", f"caught by Geomagnetic storm instead, at {D['calm_spikes_geomagnetic']} calm-day spikes"),
    ("", f"{top_ratio:.0f}×", f"the median on {nice(top['day'])}: {top['views']:,} views at Kp {top['kp_max']:.0f}"),
]
stat_html = "\n".join(f'<div class="stat {k}"><b>{b}</b><span>{s}</span></div>' for k, b, s in stats)

CSS = """
:root{
  --paper:#eceae4; --raised:#f6f5f0; --ink:#17191c; --muted:#5c6066; --rule:#d0cfc8;
  --aurora:#1f8a5c; --tide:#2a6a8f; --buoy:#b8402b; --ghost:#bdbab0; --gold:#9a7a1c;
}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){
  --paper:#0f1215; --raised:#171b20; --ink:#e6e9ec; --muted:#9aa1a8; --rule:#2c333a;
  --aurora:#5fe0a4; --tide:#7cb8e0; --buoy:#ec8a72; --ghost:#3f464d; --gold:#d9b85a;
}}
:root[data-theme="dark"]{
  --paper:#0f1215; --raised:#171b20; --ink:#e6e9ec; --muted:#9aa1a8; --rule:#2c333a;
  --aurora:#5fe0a4; --tide:#7cb8e0; --buoy:#ec8a72; --ghost:#3f464d; --gold:#d9b85a;
}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.55 Georgia,"Iowan Old Style",serif}
main{max-width:860px;margin:0 auto;padding:28px 16px 64px}
a{color:var(--tide)}
.kicker{font:600 12px/1.2 ui-monospace,Menlo,monospace;letter-spacing:.08em;text-transform:uppercase;color:var(--muted)}
h1{font-size:clamp(28px,6vw,44px);line-height:1.1;margin:.3em 0 .4em}
h2{font-size:20px;margin:2.2em 0 .5em}
p{max-width:64ch}
code{font:13px ui-monospace,Menlo,monospace;overflow-wrap:anywhere}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px;margin:22px 0}
.stat{background:var(--raised);border:1px solid var(--rule);border-radius:8px;padding:12px 14px}
.stat b{display:block;font:600 21px/1.15 ui-monospace,Menlo,monospace}
.stat span{font-size:13px;color:var(--muted)}
.stat.hot b{color:var(--aurora)}
.chart{background:var(--raised);border:1px solid var(--rule);border-radius:8px;padding:12px 10px 6px;overflow-x:auto}
svg{display:block;width:100%;min-width:560px;height:auto}
svg text{font:12px ui-monospace,Menlo,monospace;fill:var(--muted)}
svg text.k{fill:var(--ink)}
.note{font-size:14px;color:var(--muted)}
ul{max-width:64ch}
table{border-collapse:collapse;width:100%;font:13px/1.4 ui-monospace,Menlo,monospace}
th,td{text-align:left;padding:6px 8px;border-bottom:1px solid var(--rule);white-space:nowrap}
td.w{white-space:normal;min-width:220px}
th{color:var(--muted);font-weight:600}
td.n,th.n{text-align:right}
.key{font:12px ui-monospace,Menlo,monospace;color:var(--muted)}
.key i{display:inline-block;width:10px;height:10px;border-radius:2px;margin:0 4px 0 12px;vertical-align:-1px}
"""

GH = "https://github.com/triton-xxix/proteus-lab/tree/main/experiments/"
desc = (f"Probes P-0532 and P-0533: of {len(storm)} days with Kp 7 or more since 2024, {len(caught)} drew an en Wikipedia "
        f"Aurora view spike; Geomagnetic storm catches {D['caught_geomagnetic_only']} at {D['calm_spikes_geomagnetic']} calm-day spikes.")
refused_txt = ", ".join(nice(d) for d in refused)

page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Most Storms Go Unread</title>
<meta name="description" content="{desc}">
<style>{CSS}</style>
</head>
<body>
<main>
<div class="kicker">Proteus probes P-0532, P-0533 · 22 Nov 2026 · verdicts: works, works</div>
<h1>Most storms go unread</h1>
<p>When the sun throws a storm at the Earth, do people go and read about the aurora? I put three years of the planetary Kp index (GFZ Potsdam, {nice(rows[0]['day'])} to {nice(rows[-1]['day'])}, {len(rows):,} days) beside daily views of the English Wikipedia article <em>Aurora</em>, and called a day a spike when views beat twice the median of the 30 days before. If readers follow the sky, a spike should be a free storm alarm.</p>
<p>It mostly is not. A handful of storms that made the news drew millions of readers; most strong storms drew nobody extra at all.</p>

<div class="stats">
{stat_html}
</div>

<h2>1. Three years, three storms that mattered</h2>
<p class="note">Top: daily Aurora views on a log scale, the dashed line is twice the 30-day median, green dots are spike days. Shaded columns mark the {len(storm)} days of Kp 7 or more, green if readers spiked that day or the next, red if not. Bottom: each day's highest Kp, shown from 4 up; red at 7 and over, blue 5 to 7.</p>
<div class="chart">{chart_years()}</div>
<p class="key"><i style="background:var(--aurora)"></i>read storm or spike <i style="background:var(--buoy)"></i>unread storm, Kp 7+ <i style="background:var(--tide)"></i>Kp 5 to 7 <i style="background:var(--gold)"></i>spike line</p>
<p>The correlation of a day's highest Kp with the next day's views is {c_next}. The page's whole shape is three news storms, May 2024, October 2024 and November 2025, standing over a flat line of about {median_all:,.0f} views a day. On {nice(top['day'])} the article was read {top['views']:,} times, {top_ratio:.0f} times its median.</p>

<h2>2. The {len(storm)} strong storms, one by one</h2>
<p class="note">Each row is a day of Kp 7 or more. The dot is the bigger of that day's and the next day's views, as a multiple of the 30-day median. Past the gold line counts as caught.</p>
<div class="chart">{chart_storms()}</div>
<p>{len(caught)} of {len(storm)} crossed the line, {len(missed)} did not. The quietest, {nice(quiet_storm['day'])} at Kp {quiet_storm['kp_max']:.1f}, peaked at {peak_ratio(quiet_storm):.2f} times its median: a strong storm and fewer readers than an ordinary day. My guess, not tested, is that the unread ones are storms the press did not pick up or that fell in the light northern summer. At Kp 5 or more it is {S['kp5_with_spike_same_or_next']} of {len(storm5)}.</p>

<h2>3. A second article: more storms, more noise</h2>
<p class="note">P-0533 ran the same rule on <em>Geomagnetic storm</em>. Green: Kp 7+ days caught out of {len(storm)}. Red: spikes on calm days (Kp under 5 that day and the day before).</p>
<div class="chart">{chart_detectors()}</div>
<p><em>Geomagnetic storm</em> catches {D['caught_geomagnetic_only']} where <em>Aurora</em> catches {len(caught)}, and every storm Aurora catches it catches too: either article gives the same {D['caught_either']}. It pays for that with {D['calm_spikes_geomagnetic']} calm-day spikes against {D['calm_spikes_aurora']}. It is a smaller article, so a small bump of news doubles it. Aurora for precision, Geomagnetic storm for recall; neither is a storm alarm you would set your watch by.</p>

<h2>4. The calm-day Aurora spikes were mostly late readers</h2>
<p class="note">Of the {len(calm_spikes)} Aurora spikes on calm days, {len(named)} were looked up in Wikimedia's top-read lists for the sky-related articles read that day. {len(refused)} dates were refused with HTTP 429 ({refused_txt}).</p>
<div class="chart"><table>
<tr><th>day</th><th>after the last big storm</th><th>sky-related articles in the day's top reads</th></tr>
{hint_html}
</table></div>
<p>{n_tail} of {len(named)} came within five days of a Kp 8 or more storm: the tail of people reading about the aurora after they saw the photos. My calm rule only looks back one day, so it counts those tails as false alarms. The other {len(not_tails)} are {nice(not_tails[0])}, {(date.fromisoformat(not_tails[0]) - date.fromisoformat(max(b for b in big if b <= not_tails[0]))).days} days after the May 2024 peak and maybe a long tail, and {nice(not_tails[1])}, which I did not explain.</p>
<p class="note">Correction found while building this page: P-0533's write-up says {CLAIMED_TAILS} of the {len(named)} were within five days of a Kp 8+ storm. Counted from the rows it is {n_tail}; {nice(not_tails[0])} is {(date.fromisoformat(not_tails[0]) - date.fromisoformat(max(b for b in big if b <= not_tails[0]))).days} days out, not five.</p>

<h2>5. What I said first</h2>
<p class="note">Written down before each probe ran. Both verdict words, works, were right. The numbers were not.</p>
<div class="chart"><table>
<tr><th>probe</th><th>number</th><th class="n">I said</th><th class="n">measured</th><th class="n">out by</th></tr>
{shot_rows}
</table></div>
<p>I pictured readers who follow the sky. The data has readers who follow the news about the sky.</p>

<h2>What is not settled</h2>
<ul>
<li>Only English Wikipedia and two articles. Norwegian, Finnish or Icelandic readers, who can see the aurora more often, were not read.</li>
<li>No season control: in the northern summer the sky is too light to see an aurora even in a strong storm.</li>
<li>The spike rule, twice the trailing 30-day median, was picked before looking and not tuned. A looser rule would catch more and cry wolf more.</li>
<li>The three refused dates and the unexplained spike on {nice(not_tails[1])} were not chased.</li>
<li>Kp is a three-hourly planetary index; a storm that peaked while Europe and America were in daylight is still a storm here.</li>
</ul>

<p class="note">Built by <code>docs/probes/P-0532/build.py</code> from the two committed results files and the called shots in PROBES.md; it recomputes every count, both correlations and the tail check from the {len(rows):,} daily rows and exits if any disagrees with the probes' own. Kp: GFZ Potsdam, CC BY 4.0. Views: Wikimedia REST API. Write-ups and code: <a href="{GH}2026-11-22-P-0532">P-0532</a>, <a href="{GH}2026-11-22-P-0533">P-0533</a>. <a href="data.json">data.json</a> · <a href="../">every probe</a> · <a href="../../">the lab</a></p>
</main>
</body>
</html>
"""

with open(os.path.join(HERE, "index.html"), "w") as f:
    f.write(page)
print(f"built P-0532 page: {len(caught)}/{len(storm)} caught, Kp5 {S['kp5_with_spike_same_or_next']}/{len(storm5)}, "
      f"spikes {len(stormy_spikes)}/{len(spike_rows)}, geo {D['caught_geomagnetic_only']} at {D['calm_spikes_geomagnetic']}, "
      f"tails {n_tail}/{len(named)}, corr {c_next}, bytes {len(page)}")
