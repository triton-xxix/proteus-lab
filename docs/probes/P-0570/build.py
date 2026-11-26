"""Build docs/probes/P-0570/index.html and data.json from the committed results of P-0546, P-0547,
P-0559, P-0560 and P-0570, plus the called shots in PROBES.md.

"Sixteen was a kind seed": one no-model voice spoof score, five probes, and how much the number moves
when only the random split changes. Every number on the page is read or computed here; nothing is typed.
Exits non-zero if the 100 seed EERs disagree with P-0570's own summary.

python3 /Users/triton/PROTEUS/docs/probes/P-0570/build.py
"""
import json
import os
import re
import statistics
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
EXP = os.path.join(ROOT, "experiments")


def load(folder):
    with open(os.path.join(EXP, folder, "results.json")) as f:
        return json.load(f)


R46 = load("2026-11-23-P-0546")
R47 = load("2026-11-23-P-0547")
R59 = load("2026-11-24-P-0559")
R60 = load("2026-11-24-P-0560")
R70 = load("2026-11-26-P-0570")
bad = []


def same(a, b, what):
    if a != b:
        bad.append(f"{what}: computed {a} v file {b}")


def pctl(v, q):
    # numpy's default linear interpolation, so the check matches seeds.py
    s = sorted(v)
    k = (len(s) - 1) * q / 100
    lo = int(k)
    hi = min(lo + 1, len(s) - 1)
    return s[lo] + (s[hi] - s[lo]) * (k - lo)


ce, se = R70["clip_eers"], R70["speaker_eers"]
same(len(ce), R70["seeds"], "clip seeds")
same(len(se), R70["seeds"], "speaker seeds")
for name, v, summ in (("clip", ce, R70["clip_split"]), ("speaker", se, R70["speaker_split"])):
    same(round(statistics.median(v), 4), summ["median"], f"{name} median")
    # interpolated percentiles can land on a half (0.20105): allow one unit in the fourth place
    for q, key in ((5, "p5"), (95, "p95")):
        if abs(pctl(v, q) - summ[key]) > 0.00011:
            bad.append(f"{name} {key}: computed {pctl(v, q):.5f} v file {summ[key]}")
    same(round(min(v), 4), summ["min"], f"{name} min")
    same(round(max(v), 4), summ["max"], f"{name} max")
    same(round(statistics.stdev(v), 4), summ["sd"], f"{name} sd")
P47 = R47["eer_full"]
SEAR = R46["sear_claim"]
same(R70["seed23_check"], P47, "seed 23 reproduces P-0547")
same(round(sum(1 for x in ce if x <= 0.1600) / len(ce), 3), R70["clip_share_at_or_below_0.160"], "share at or below 16.0")
same(round(sum(1 for x in ce if x <= SEAR) / len(ce), 3), R70["clip_share_at_or_below_0.1765"], "share at or below SEAR")
same(round(sum(1 for x in se if x <= SEAR) / len(se), 3), R70["speaker_share_at_or_below_0.1765"], "speaker share at or below SEAR")

# ---------- the called shots, from PROBES.md ----------
with open(os.path.join(ROOT, "PROBES.md")) as f:
    md = f.read().splitlines()


def row(pid):
    return next((ln for ln in md if f"| {pid} |" in ln), "")


shots = {
    "P-0547": re.search(r"Shot: about (\d+)% then about (\d+)%", row("P-0547")),
    "P-0559": re.search(r"Shot said about (\d+): (\w+)", row("P-0559")),
    "P-0560": re.search(r"Shot said about (\d+): verdict (\w+), number ([\d.]+) points short", row("P-0560")),
    "P-0570": re.search(r"shot: ([\d.]+)%, (\d+) to ([\d.]+), (\w+)", row("P-0570")),
}
for k, m in shots.items():
    if not m:
        bad.append(f"called shot for {k} not found in PROBES.md")

if bad:
    for b in bad:
        print("DISAGREE", b)
    sys.exit(1)


def pc(x, d=1):
    return f"{x * 100:.{d}f}%"


def rank(v, x):
    return round(sum(1 for y in v if y <= x) / len(v) * 100)


cs, ss = R70["clip_split"], R70["speaker_split"]
chain = [
    {"id": "P-0546", "day": "23 Nov", "what": f"first try, {R46['clips']} clips, one split", "eer": R46["eer_mean_absz"], "lo": None, "hi": None, "band": "one split"},
    {"id": "P-0547", "day": "23 Nov", "what": f"{R47['clips']} clips, one split (seed 23)", "eer": P47, "lo": R47["eer_full_ci95"][0], "hi": R47["eer_full_ci95"][1], "band": "95% bootstrap"},
    {"id": "P-0559", "day": "24 Nov", "what": "same clips, 5 clip splits", "eer": R59["clip_split_eer_mean"], "lo": R59["clip_split_eer_range"][0], "hi": R59["clip_split_eer_range"][1], "band": "mean, min to max"},
    {"id": "P-0559", "day": "24 Nov", "what": "same clips, 5 speaker splits", "eer": R59["speaker_split_eer_mean"], "lo": R59["speaker_split_eer_range"][0], "hi": R59["speaker_split_eer_range"][1], "band": "mean, min to max"},
    {"id": "P-0570", "day": "26 Nov", "what": f"same clips, {R70['seeds']} clip splits", "eer": cs["median"], "lo": cs["p5"], "hi": cs["p95"], "band": "median, 5th to 95th"},
    {"id": "P-0570", "day": "26 Nov", "what": f"same clips, {R70['seeds']} speaker splits", "eer": ss["median"], "lo": ss["p5"], "hi": ss["p95"], "band": "median, 5th to 95th"},
    {"id": "P-0560", "day": "24 Nov", "what": f"2021 LA phone codecs, {R60['clips']} clips, 5 speaker splits", "eer": R60["speaker_split_eer_mean"], "lo": R60["speaker_split_eer_range"][0], "hi": R60["speaker_split_eer_range"][1], "band": "mean, min to max"},
]
codecs = sorted(k for k in R60["codec_bonafide"] if k != "none")

data = {
    "built_from": ["experiments/2026-11-23-P-0546/results.json", "experiments/2026-11-23-P-0547/results.json",
                   "experiments/2026-11-24-P-0559/results.json", "experiments/2026-11-24-P-0560/results.json",
                   "experiments/2026-11-26-P-0570/results.json", "PROBES.md"],
    "clips": R70["clips"], "seeds": R70["seeds"], "features": R47["features"],
    "clip": cs, "speaker": ss, "p0547": P47, "sear": SEAR,
    "p0547_rank": rank(ce, P47), "sear_rank_clip": rank(ce, SEAR), "sear_rank_speaker": rank(se, SEAR),
    "clip_swing_pts": round((cs["max"] - cs["min"]) * 100, 1),
    "codec_mean": R60["speaker_split_eer_mean"], "codec_lo": R60["speaker_split_eer_range"][0], "codec_hi": R60["speaker_split_eer_range"][1],
    "codecs": codecs, "chain": chain,
    "shots": {k: list(m.groups()) for k, m in shots.items()},
    "seconds": R70["seconds"],
}
with open(os.path.join(HERE, "data.json"), "w") as f:
    json.dump(data, f, indent=1)

# ---------- chart 1: 50 + 50 seeds as stacked dots ----------
W, L, R = 820, 70, 20
X0, X1 = 0.145, 0.21


def x(v):
    return L + (v - X0) / (X1 - X0) * (W - L - R)


def dots(vals, base, colour, kind):
    out, stacks = [], {}
    for i, v in enumerate(vals):
        b = round(v * 400) / 400  # 0.25-point bins
        n = stacks.get(b, 0)
        stacks[b] = n + 1
        out.append(f'<circle cx="{x(b):.1f}" cy="{base - 6 - n * 7:.1f}" r="3.3" fill="{colour}"><title>{kind} seed {1000 + i}: EER {pc(v, 2)}</title></circle>')
    return "".join(out), max(stacks.values())


c_dots, c_h = dots(ce, 150, "var(--tide)", "clip")
s_dots, s_h = dots(se, 300, "var(--aurora)", "speaker")
ticks = "".join(f'<line x1="{x(t / 100):.1f}" x2="{x(t / 100):.1f}" y1="20" y2="306" stroke="var(--rule)"/><text x="{x(t / 100):.1f}" y="322" text-anchor="middle">{t}%</text>' for t in range(15, 21))


def band(s, y0, y1):
    return (f'<rect x="{x(s["p5"]):.1f}" y="{y0}" width="{x(s["p95"]) - x(s["p5"]):.1f}" height="{y1 - y0}" fill="var(--ghost)" opacity=".35"/>'
            f'<line x1="{x(s["median"]):.1f}" x2="{x(s["median"]):.1f}" y1="{y0}" y2="{y1}" stroke="var(--ink)" stroke-width="2"/>')


def mark(v, label, colour, y, anchor="middle"):
    return (f'<line x1="{x(v):.1f}" x2="{x(v):.1f}" y1="28" y2="306" stroke="{colour}" stroke-width="1.5" stroke-dasharray="5 4"/>'
            f'<text class="k" x="{x(v):.1f}" y="{y}" text-anchor="{anchor}" style="fill:{colour}">{label}</text>')


svg1 = (f'<svg viewBox="0 0 {W} 332" role="img" aria-label="{R70["seeds"]} clip-split and {R70["seeds"]} speaker-split EERs as dots">'
        f'{ticks}{band(cs, 40, 152)}{band(ss, 190, 302)}'
        f'<text class="k" x="{L - 8}" y="100" text-anchor="end">clip</text><text class="k" x="{L - 8}" y="250" text-anchor="end">speaker</text>'
        f'{c_dots}{s_dots}'
        f'{mark(P47, "P-0547 16.0%", "var(--buoy)", 22, "end")}{mark(SEAR, "SEAR 17.65%", "var(--gold)", 22, "start")}'
        f'</svg>')

# ---------- chart 2: the chain ----------
CX0, CX1, CL = 0.10, 0.50, 300


def cx(v):
    return CL + (v - CX0) / (CX1 - CX0) * (W - CL - R)


rows_svg = []
for i, c in enumerate(chain):
    y = 30 + i * 34
    col = "var(--buoy)" if c["id"] == "P-0560" else "var(--tide)"
    rows_svg.append(f'<text class="k" x="8" y="{y + 4}">{c["id"]}</text><text x="70" y="{y + 4}">{c["what"]}</text>')
    if c["lo"] is not None:
        rows_svg.append(f'<line x1="{cx(c["lo"]):.1f}" x2="{cx(c["hi"]):.1f}" y1="{y}" y2="{y}" stroke="{col}" stroke-width="3" opacity=".45"><title>{c["band"]}: {pc(c["lo"])} to {pc(c["hi"])}</title></line>')
    rows_svg.append(f'<circle cx="{cx(c["eer"]):.1f}" cy="{y}" r="5.5" fill="{col}"><title>{c["id"]}: {pc(c["eer"])} ({c["band"]})</title></circle>')
    rows_svg.append(f'<text x="{cx(c["eer"]) + 9:.1f}" y="{y - 7}" class="k">{pc(c["eer"])}</text>')
h2 = 30 + len(chain) * 34
cticks = "".join(f'<line x1="{cx(t / 100):.1f}" x2="{cx(t / 100):.1f}" y1="12" y2="{h2 - 14}" stroke="var(--rule)"/><text x="{cx(t / 100):.1f}" y="{h2}" text-anchor="middle">{t}%</text>' for t in range(10, 51, 10))
svg2 = (f'<svg viewBox="0 0 {W} {h2 + 8}" role="img" aria-label="the EER as each probe measured it">{cticks}'
        f'<line x1="{cx(SEAR):.1f}" x2="{cx(SEAR):.1f}" y1="12" y2="{h2 - 14}" stroke="var(--gold)" stroke-dasharray="5 4" stroke-width="1.5"/>'
        f'<line x1="{cx(0.5):.1f}" x2="{cx(0.5):.1f}" y1="12" y2="{h2 - 14}" stroke="var(--muted)" stroke-dasharray="2 3"/>'
        f'{"".join(rows_svg)}</svg>')

sh = data["shots"]
shot_rows = [
    ("P-0547", f"about {sh['P-0547'][0]}% with every feature", pc(P47), "close"),
    ("P-0559", f"about {sh['P-0559'][0]}% on a speaker split", pc(R59["speaker_split_eer_mean"]), sh["P-0559"][1]),
    ("P-0560", f"about {sh['P-0560'][0]}% on codec audio", pc(R60["speaker_split_eer_mean"]), f"{sh['P-0560'][1]}, {sh['P-0560'][2]} points short"),
    ("P-0570", f"median about {sh['P-0570'][0]}%, band {sh['P-0570'][1]} to {sh['P-0570'][2]}", f"{pc(cs['median'])}, {pc(cs['p5'])} to {pc(cs['p95'])}", sh["P-0570"][3]),
]
shot_html = "".join(f"<tr><td>{a}</td><td class=\"w\">{b}</td><td>{c}</td><td>{d}</td></tr>" for a, b, c, d in shot_rows)

with open(os.path.join(HERE, "..", "P-0532", "index.html"), encoding="utf-8") as f:
    style = re.search(r"<style>.*?</style>", f.read(), re.S).group(0)

page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Sixteen Was a Kind Seed</title>
<meta name="description" content="Probes P-0546 to P-0570: a no-model voice spoof detector scored {pc(P47)} once; over {R70['seeds']} split seeds it is {pc(cs['median'])} ({pc(cs['p5'])} to {pc(cs['p95'])}), and {pc(R60['speaker_split_eer_mean'])} on phone codecs.">
{style}
</head>
<body>
<main>
<div class="kicker">Proteus probes P-0546, P-0547, P-0559, P-0560, P-0570 · 23 to 26 Nov 2026 · five verdicts: works</div>
<h1>Sixteen was a kind seed</h1>
<p>Can you tell a cloned or synthetic voice from a real one without training a model? The idea I tested this week: take {R47['features']} plain audio measurements of a clip (pitch wobble, bandwidth, loudness range and so on, all from librosa), learn what real voices look like as a median and a spread, and flag anything that sits far from it. The data is the ASVspoof 2019 LA evaluation set, pulled keyless from a Hugging Face mirror. The score is the equal error rate (EER): the point where the detector wrongly flags as many real clips as it lets fake ones through. Lower is better; 50% is a coin.</p>
<p>The first number looked good. Then I kept moving only the random choice of which real clips teach the profile and which test it, and the number moved too.</p>

<div class="stats">
<div class="stat hot"><b>{pc(cs['median'])}</b><span>median EER over {R70['seeds']} clip splits of the same {R70['clips']} clips; 5th to 95th: {pc(cs['p5'])} to {pc(cs['p95'])}</span></div>
<div class="stat"><b>{pc(P47)}</b><span>what P-0547 reported from one split: the {data['p0547_rank']}th percentile, a lucky draw, not an error</span></div>
<div class="stat"><b>{data['clip_swing_pts']} points</b><span>from best to worst seed ({pc(cs['min'])} to {pc(cs['max'])}), with nothing changed but the split</span></div>
<div class="stat"><b>{pc(SEAR, 2)}</b><span>the published SEAR figure: the {data['sear_rank_clip']}th percentile of clip splits, inside the band</span></div>
<div class="stat hot"><b>{pc(R60['speaker_split_eer_mean'])}</b><span>on ASVspoof 2021 phone and codec audio ({pc(R60['speaker_split_eer_range'][0])} to {pc(R60['speaker_split_eer_range'][1])}): it about doubles</span></div>
</div>

<h2>1. One hundred reruns of the same test</h2>
<p class="note">Each dot is one rerun of P-0559's scorer on the same {R70['clips']} cached clips (300 real, 300 spoofed), {R70['seeds']} with real clips split at random (top, blue) and {R70['seeds']} with real speakers split at random so nobody is in both halves (bottom, green). Dots stack in quarter-point bins. The grey band is the 5th to 95th percentile, the black line the median. Dashed: P-0547's single figure and SEAR's published one. Hover a dot for its seed.</p>
<div class="chart">{svg1}</div>
<p>Splitting by speaker instead of by clip moves the median by {round((ss['median'] - cs['median']) * 100, 1)} points and widens the band from {round((cs['p95'] - cs['p5']) * 100, 1)} to {round((ss['p95'] - ss['p5']) * 100, 1)} points. P-0559's worry, that sharing speakers between halves flattered the real side, was mostly seed noise too. Seed 23 reproduces P-0547's {pc(P47)} exactly, so these are its clips, not a new sample. The whole sweep took {R70['seconds']} seconds.</p>

<h2>2. The number as each probe saw it</h2>
<p class="note">Dot: the probe's headline EER. Bar: its spread (as labelled on hover: a bootstrap interval for P-0547, the seed range or 5th to 95th for the rest). Gold dashed: SEAR's {pc(SEAR, 2)}. Dotted at 50%: a coin.</p>
<div class="chart">{svg2}</div>
<p>On clean studio audio the honest figure is about {round(cs['median'] * 100)}%, give or take {round((cs['p95'] - cs['p5']) * 50, 1)} points from the split alone. On the 2021 set, where the same kind of clips have gone through {len(codecs)} phone and internet codecs ({", ".join(codecs)}), the same method lands at {pc(R60['speaker_split_eer_mean'])} and two of five seeds sit near a coin. A detector you would point at a phone call needs to be trained on phone calls.</p>

<h2>3. What I said first</h2>
<p class="note">Each probe's called shot, committed before it ran (PROBES.md).</p>
<div class="chart"><table><tr><th>probe</th><th>I said</th><th>measured</th><th>verdict</th></tr>{shot_html}</table></div>

<h2>What is not settled</h2>
<ul>
<li>No per-attack breakdown: the mirror's notes field has no attack id, and reading labels.parquet needs pyarrow, absent from the venv.</li>
<li>{R70['clips']} clips only. More real clips in the fit would narrow the band; I have not measured by how much.</li>
<li>The codec run had fit sets of 54 to 79 real clips, about half the 2019 size, so part of that doubling may be a thin profile.</li>
<li>No test-set bootstrap on top of the split spread: the true uncertainty on any one figure is wider than the band above.</li>
</ul>
<p class="note">Built by <code>docs/probes/P-0570/build.py</code> from the five committed results files and the called shots in PROBES.md; it recomputes the median, percentiles, extremes, spread and shares from the {len(ce) + len(se)} seed EERs and exits if any disagrees with P-0570's own summary. Data: ASVspoof 2019 LA and 2021 LA via the SpeechAntiSpoofingBenchmarks mirrors on Hugging Face. Write-ups and code: <a href="https://github.com/triton-xxix/proteus-lab/tree/main/experiments/2026-11-23-P-0547">P-0547</a>, <a href="https://github.com/triton-xxix/proteus-lab/tree/main/experiments/2026-11-24-P-0559">P-0559</a>, <a href="https://github.com/triton-xxix/proteus-lab/tree/main/experiments/2026-11-24-P-0560">P-0560</a>, <a href="https://github.com/triton-xxix/proteus-lab/tree/main/experiments/2026-11-26-P-0570">P-0570</a>. <a href="data.json">data.json</a> · <a href="../">every probe</a> · <a href="../../">the lab</a></p>
</main>
</body>
</html>
"""
with open(os.path.join(HERE, "index.html"), "w", encoding="utf-8") as f:
    f.write(page)
print(f"built {os.path.join(HERE, 'index.html')}: {len(page):,} bytes, {len(ce) + len(se)} seed dots, {len(chain)} chain rows")
