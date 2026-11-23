#!/usr/bin/env python3
"""Build docs/tools/trade-finder/index.html from a committed trade_finder run.

Exits unless the run's summary is recomputed from its rows by the tool's own summarise(), and
unless the called numbers match RULE.md. The page shows counts and dots only: no firm names,
sites or phones (the rows stay in experiments/2026-11-23-lead-finder/).
"""
import html
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import trade_finder  # noqa: E402

EXP = os.path.join(HERE, "..", "..", "..", "experiments", "2026-11-23-lead-finder")
RUN = os.path.join(EXP, "run-2026-11-23.json")
RULE = os.path.join(EXP, "RULE.md")


def die(msg):
    sys.exit("build.py: " + msg)


run = json.load(open(RUN))
rows, s, meta = run["rows"], run["summary"], run["meta"]
if trade_finder.summarise(rows) != s:
    die("summary does not match summarise(rows)")
rule = open(RULE).read()
m = re.search(r"About (\d+) tagged firms, about (\d+)% with a website, so about (\d+) leads", rule)
if not m:
    die("called numbers not found in RULE.md")
call_firms, call_pct, call_leads = map(int, m.groups())
south, west, north, east = map(float, meta["area"].split(","))
if any(not (south <= r["lat"] <= north and west <= r["lon"] <= east) for r in rows):
    die("a row sits outside the box")

firms, leads, both = s["firms"], s["leads"], s["with_both"]
pct_web = round(100 * leads / firms)
sample = min(30, leads)
outside = sum(1 for r in rows if r["area"] and r["area"] not in {"M", "BL", "OL", "SK", "WN", "WA"})


def bar(label, n, top, cls=""):
    w = 0 if top == 0 else max(0.6, 100 * n / top)
    return (f'<div class="row"><span class="lab">{html.escape(label)}</span>'
            f'<span class="track"><span class="fill {cls}" style="width:{w:.1f}%"></span></span>'
            f'<span class="num">{n}</span></div>')


funnel = [
    ("tagged firms", firms, ""),
    ("with a name", s["with_name"], ""),
    ("with a postcode", s["with_postcode"], ""),
    ("with a website (a lead)", leads, "lead"),
    ("website and phone", both, "lead"),
]
funnel_html = "".join(bar(a, b, firms, c) for a, b, c in funnel)
called_html = (bar("firms, my call", call_firms, call_firms, "call") + bar("firms, found", firms, call_firms)
               + bar("leads, my call", call_leads, call_firms, "call") + bar("leads, found", leads, call_firms, "lead"))
craft_html = "".join(bar(k.replace("_", " "), v["firms"], firms) for k, v in s["by_craft"].items())
pc_html = "".join(bar(k if k != "none" else "no postcode", v, firms) for k, v in s["by_postcode_area"].items())

# dot map: equirectangular with cos(lat) correction, inside the pulled box
import math  # noqa: E402
k = math.cos(math.radians((south + north) / 2))
W = 640
H = round(W * (north - south) / ((east - west) * k))
dots = []
for r in rows:
    x = (r["lon"] - west) / (east - west) * W
    y = (north - r["lat"]) / (north - south) * H
    cls = "dot lead" if r["website"] else "dot"
    dots.append(f'<circle class="{cls}" cx="{x:.1f}" cy="{y:.1f}" r="{7 if r["website"] else 5}"/>')
# Manchester city centre for orientation
mx = (-2.2446 - west) / (east - west) * W
my = (north - 53.4794) / (north - south) * H
svg = (f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="{firms} firms as dots, {leads} with a website">'
       f'<rect class="frame" x="0.5" y="0.5" width="{W-1}" height="{H-1}"/>'
       f'<path class="cross" d="M{mx-8:.1f} {my:.1f}h16M{mx:.1f} {my-8:.1f}v16"/>'
       f'<text class="tag" x="{mx+10:.1f}" y="{my-8:.1f}">Manchester centre</text>'
       + "".join(dots) + "</svg>")

page = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Three Leads</title>
<meta name="description" content="OpenStreetMap's plumbing and heating firms around Greater Manchester, counted keyless: {firms} firms, {leads} with a website.">
<style>
:root{{--bg:#fbfaf7;--fg:#1d1d1b;--mute:#6b6a65;--line:#dcd9d0;--track:#ecebe5;--fill:#8a8a84;--lead:#c2410c;--call:#2563eb}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#151514;--fg:#ecebe6;--mute:#a09f98;--line:#3a3935;--track:#262624;--fill:#8d8c86;--lead:#fb923c;--call:#60a5fa}}}}
:root[data-theme="dark"]{{--bg:#151514;--fg:#ecebe6;--mute:#a09f98;--line:#3a3935;--track:#262624;--fill:#8d8c86;--lead:#fb923c;--call:#60a5fa}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--fg);font:16px/1.55 system-ui,-apple-system,Segoe UI,sans-serif}}
main{{max-width:760px;margin:0 auto;padding:32px 16px 64px}}
h1{{font-size:2.2rem;line-height:1.1;margin:.2em 0 .3em}}h2{{font-size:1.15rem;margin:2.2em 0 .6em}}
.kick{{color:var(--mute);font-size:.85rem;text-transform:uppercase;letter-spacing:.06em}}
.lede{{font-size:1.15rem}}.mute{{color:var(--mute)}}a{{color:inherit}}
.big{{display:flex;flex-wrap:wrap;gap:12px;margin:24px 0}}.big div{{flex:1 1 140px;border-top:2px solid var(--line);padding-top:8px}}
.big b{{display:block;font-size:2rem;font-variant-numeric:tabular-nums}}.big .lead b{{color:var(--lead)}}
.row{{display:grid;grid-template-columns:minmax(0,11rem) 1fr 3rem;gap:10px;align-items:center;margin:6px 0;font-size:.95rem}}
.lab{{overflow-wrap:anywhere}}.track{{height:14px;background:var(--track);border-radius:3px;overflow:hidden}}
.fill{{display:block;height:100%;background:var(--fill)}}.fill.lead{{background:var(--lead)}}.fill.call{{background:var(--call)}}
.num{{text-align:right;font-variant-numeric:tabular-nums}}
svg{{width:100%;height:auto;display:block}}.frame{{fill:none;stroke:var(--line)}}.cross{{stroke:var(--mute);stroke-width:1.5}}
.tag{{fill:var(--mute);font-size:13px}}.dot{{fill:var(--fill);fill-opacity:.75}}.dot.lead{{fill:var(--lead);fill-opacity:1}}
code{{font-size:.9em}}pre{{overflow-x:auto;background:var(--track);padding:10px;border-radius:4px;font-size:.85rem}}
@media (max-width:480px){{.row{{grid-template-columns:minmax(0,7.5rem) 1fr 2.5rem}}h1{{font-size:1.8rem}}}}
</style></head><body><main>
<p class="kick">Proteus lab · tool · lead finder step one · {meta['pulled_utc'][:10]}</p>
<h1>Three leads</h1>
<p class="lede">I asked OpenStreetMap for every plumber, heating engineer, gas fitter and HVAC firm in a box
around Greater Manchester. It knows {firms}. {leads} of them have a website, {both} has a website and a phone.
I had called about {call_firms} firms and {call_leads} leads before the pull.</p>
<div class="big"><div><b>{firms}</b>tagged firms</div><div class="lead"><b>{leads}</b>with a website ({pct_web}%)</div>
<div><b>{both}</b>website and phone</div><div><b>{call_leads}</b>leads I called</div></div>

<h2>Called before the pull, then found</h2>
{called_html}
<p class="mute">The call and the pass mark were committed before the first request
(<code>experiments/2026-11-23-lead-finder/RULE.md</code>). I called {call_pct}% with a website; it was {pct_web}%.
The count was the bigger miss: about six times fewer firms than I expected.</p>

<h2>From tag to lead</h2>
{funnel_html}

<h2>Where they are</h2>
{svg}
<p class="mute">Each dot is one tagged firm, orange where it has a website. The box is
{south}°N to {north}°N, {west}° to {east}°E, which is wider than the county: {outside} firm with a postcode outside
Greater Manchester's areas is inside it. So the county's own count is {firms} or fewer.</p>

<h2>By tag</h2>
{craft_html}
<h2>By postcode area</h2>
{pc_html}

<h2>What it means</h2>
<p>On these tags, OpenStreetMap is not a lead source for trades in Greater Manchester. Saturday's hand check
was meant to take 30 leads; there are {leads}, so the rule says all {sample} are checked and the verdict says
so. Even if all {sample} pass, {sample} firms is not a list anyone could work. Step two has to find firms another
way (the firms' own sites from search, public job ads, the free Companies House register), and OSM becomes
one column, not the spine.</p>
<p class="mute">Not tested: other tags a plumber might carry in OSM (shop, office), and whether the main
Overpass server's area lookup by county name works at all (it returned 0 rows at admin level 6 and timed out
on the second try, so I used the box). No firm was contacted. Names, sites and phones are not on this page.</p>

<h2>Run it</h2>
<pre>python3 trade_finder.py --area "{meta['area']}" --level bbox --out run.json
python3 trade_finder.py --from run.json --out run.json</pre>
<p><a href="trade_finder.py">trade_finder.py</a> · stdlib only, keyless, public Overpass API ·
<a href="README.md">README</a> · OSM data as of {meta['osm_timestamp']}, © OpenStreetMap contributors, ODbL ·
<a href="../../">Proteus lab</a></p>
</main></body></html>
"""
open(os.path.join(HERE, "index.html"), "w").write(page)
print(f"built index.html: {firms} firms, {leads} leads, {both} both, {len(page)} bytes")
