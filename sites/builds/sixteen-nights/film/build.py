#!/usr/bin/env python3
"""Build the Sixteen Nights film: index.html plus compositions/*.html, from ../record.json.

    python3 /Users/triton/PROTEUS/sites/builds/sixteen-nights/film/build.py

Every number in the film is read from record.json here and inlined into the scene scripts, so the
compositions are deterministic (no fetch, no clock, no randomness). Frame lengths come from the voice
files: a frame lasts the longer of its storyboard minimum and its voice line plus a breath. Seams are
the incoming scene's own entrance over an overlap (crossfade, wipe, fade), so the root timeline stays
empty. Rerun after regenerating record.json or any voice line; then `hyperframes check`.
"""
import hashlib
import json
import os
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
BUILD = os.path.dirname(HERE)
REC = json.load(open(os.path.join(BUILD, "record.json")))
COMP = os.path.join(HERE, "compositions")
os.makedirs(COMP, exist_ok=True)

C = {"canvas": "#07090d", "surface": "#0e1218", "ink": "#ece6d9", "soft": "#9a9486", "hint": "#5d5a54", "rule": "#232a33",
     "amber": "#e0a450", "works": "#7fc8a9", "broken": "#d96b5c", "blocked": "#8d9bb5", "notworth": "#6f6a62",
     "killed": "#c9473c", "open": "#4e5868", "loss": "#c9473c", "gain": "#7fc8a9"}
FONT_DISPLAY = "'Archivo', 'Helvetica Neue', Arial, sans-serif"
FONT_TEXT = "'Geist', 'Helvetica Neue', Arial, sans-serif"
FONT_MONO = "'Geist Mono', 'SF Mono', Menlo, monospace"


def ffdur(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path], capture_output=True, text=True).stdout.strip()
    return float(out) if out else 0.0


def money(x):
    return "£%s" % format(x, ",.2f")


def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


# ------------------------------------------------------------------ data shapes
G = REC["grinder"]
path = G["path"]
low_i = min(range(len(path)), key=lambda i: path[i]["bankroll"])
start_bank = G["stats"]["start"]
P = REC["probes"]
pooled = (REC["pitch"]["backtest"].get("pooled") or {}).get("rows", [])
rps = {r["line"]: r["rps"] for r in pooled}
LI = REC["lichess"]
J = REC["pitch"]["judgement"]
G1 = REC["graduation"]["g1"]
SYS = REC["systems"]
GOAL = REC["goal"]
Q = {q["text"]: q for q in REC["quotes"]}
first_sha = REC["commits"]["first"]["sha"] if REC["commits"]["first"] else ""
nights = REC["nights"]

# probe points: stable positions from the id, creation order from `added` then id, appearance by real time
items = sorted(P["items"], key=lambda p: ((p.get("added") or ""), p["id"]))
stamps = []
for p in items:
    ts = p.get("started_at") or ((p.get("added") or "2026-09-24") + "T23:30:00+0100")
    stamps.append(ts)
import datetime as _dt


def _t(ts):
    try:
        return _dt.datetime.fromisoformat(ts).timestamp()
    except ValueError:
        return 0.0
tnum = [_t(s) for s in stamps]
t0, t1 = min(tnum), max(tnum)
POINTS = []
for p, tn in zip(items, tnum):
    h = hashlib.sha1(p["id"].encode()).hexdigest()
    x = 0.06 + (int(h[:6], 16) / 0xFFFFFF) * 0.88
    y = 0.10 + (int(h[6:12], 16) / 0xFFFFFF) * 0.62
    st = p["status"]
    kind = "killed" if st == "killed" else ("open" if st in ("open", "in_progress") else (p.get("verdict") or "open"))
    POINTS.append({"id": p["id"], "x": round(x, 4), "y": round(y, 4), "k": kind, "a": round((tn - t0) / max(t1 - t0, 1), 4), "title": p["title"][:80]})
VCOL = {"works": C["works"], "broken": C["broken"], "blocked": C["blocked"], "not-worth-it": C["notworth"], "killed": C["killed"], "open": C["open"]}

# ------------------------------------------------------------------ frames and timing
VOICE_DIR = os.path.join(HERE, "media", "voice")
FR = [
    # id, slug, min seconds, voice file, seam kind into this frame, overlap seconds, clock text
    ("01", "clock", 4.0, "01", "cut", 0.0, "23:15:00"),
    ("02", "room", 6.0, "02", "crossfade", 0.8, "22 Sep 2026 · 23:23 · %s" % first_sha),
    ("03", "rule-one", 5.0, "03", "crossfade", 0.6, "22 Sep 2026 · signed · cdf6a27"),
    ("04", "rule-two", 5.0, "04", "wipe-left", 0.5, "29 Sep 2026 · v2 signed · e1ebe88"),
    ("05", "grinder-falls", 7.0, "05", "cut", 0.0, "%s · 23:48" % _dt.datetime.fromisoformat(path[low_i]["at"].replace("Z", "+00:00")).strftime("%d %b %Y")),
    ("06", "grinder-climbs", 6.0, "06", "continuous", 0.0, "06 Oct 2026 · 23:23"),
    ("07", "pitch", 6.0, "07", "wipe-left", 0.5, "24 Sep 2026 · backtest · 30091b8"),
    ("08", "books", 7.0, "08", "cut", 0.0, "03 Oct 2026 · 23:47"),
    ("09", "silence", 2.2, None, "fade", 0.6, "…"),
    ("10", "field", 10.0, "10", "cut", 0.0, "%d nights · %d probes" % (nights, P["total"])),
    ("11", "fall", 4.0, "11", "continuous", 0.0, "Sunday culls · %d killed" % P["killed"]),
    ("12", "wrong", 10.0, "12", "cut", 0.0, "28 Sep 2026 · 23:57"),
    ("13", "survivor", 6.0, "13", "wipe-up", 0.5, "07 Oct 2026 · 9fd339e"),
    ("14", "goal", 9.0, "14", "fade", 0.7, "07 Oct 2026 · 00:13 · 23657e3"),
    ("15", "tonight", 6.0, None, "crossfade", 0.8, "Tonight · 23:15"),
]
TAIL = 1.1
frames = []
cursor = 0.0
for fid, slug, mn, voice, kind, tin, clock in FR:
    vd = ffdur(os.path.join(VOICE_DIR, voice + ".mp3")) if voice else 0.0
    d = max(mn, vd + TAIL + (tin if voice else 0))
    start = max(0.0, cursor - tin)
    frames.append({"id": fid, "slug": slug, "start": round(start, 2), "dur": round(d, 2), "end": round(start + d, 2), "voice": voice, "vdur": round(vd, 2),
                   "voice_at": round(start + tin + 0.25, 2) if voice else None, "kind": kind, "tin": tin, "clock": clock})
    cursor = start + d
TOTAL = round(cursor, 2)

# ------------------------------------------------------------------ shared scene scaffolding
BASE_CSS = """
#root{position:absolute;inset:0;background:%(canvas)s;color:%(ink)s;font-family:%(text)s;overflow:hidden}
#stage{position:absolute;inset:0;will-change:transform,opacity}
.clock{position:absolute;left:112px;top:72px;font-family:%(mono)s;font-size:27px;letter-spacing:.06em;color:%(amber)s;white-space:nowrap}
.clock.dim{opacity:.35}
.mono{font-family:%(mono)s;letter-spacing:.04em;color:%(soft)s}
.display{font-family:%(display)s;font-weight:900;letter-spacing:-.035em;line-height:.92}
.h2{font-family:%(display)s;font-weight:800;font-size:69px;line-height:1.06;letter-spacing:-.02em}
.h3{font-family:%(display)s;font-weight:700;font-size:46px;line-height:1.15;letter-spacing:-.01em}
.stat{font-family:%(display)s;font-weight:800;letter-spacing:-.03em;line-height:1;font-variant-numeric:tabular-nums}
.label{font-family:%(display)s;font-weight:700;font-size:21px;letter-spacing:.02em;color:%(amber)s}
.body{font-size:25px;line-height:1.55}
.hidden0{opacity:0}
""" % dict(C, text=FONT_TEXT, mono=FONT_MONO, display=FONT_DISPLAY)

ENTRANCE = {
    "cut": "", "continuous": "",
    "crossfade": 'tl.fromTo("#stage", {opacity: 0}, {opacity: 1, duration: TIN, ease: "power2.inOut"}, 0);',
    "fade": 'tl.fromTo("#stage", {opacity: 0}, {opacity: 1, duration: TIN, ease: "power2.inOut"}, 0);',
    "wipe-left": 'tl.fromTo("#stage", {x: 1920}, {x: 0, duration: TIN, ease: "power3.inOut"}, 0);',
    "wipe-up": 'tl.fromTo("#stage", {y: 1080}, {y: 0, duration: TIN, ease: "power3.inOut"}, 0);',
}


def write_scene(fr, inner, css="", setup="", timeline=""):
    cid = "f%s-%s" % (fr["id"], fr["slug"])
    entrance = ENTRANCE[fr["kind"]].replace("TIN", "%.2f" % fr["tin"])
    html = """<!doctype html>
<html lang="en">
<head><meta charset="utf-8"><title>%(cid)s</title></head>
<body>
<template>
<style>%(base)s%(css)s</style>
<div id="root" data-composition-id="%(cid)s" data-width="1920" data-height="1080">
  <div id="stage">
    <div class="clock%(dim)s">%(clock)s</div>
%(inner)s
  </div>
</div>
<script>
(function () {
  var TIN = %(tin).2f;
  %(setup)s
  var tl = gsap.timeline({ paused: true });
  %(entrance)s
  %(timeline)s
  window.__timelines["%(cid)s"] = tl;
})();
</script>
</template>
</body>
</html>
""" % dict(cid=cid, base=BASE_CSS, css=css, clock=esc(fr["clock"]), dim=" dim" if fr["id"] == "09" else "", inner=inner,
           setup=setup, entrance=entrance, timeline=timeline, tin=fr["tin"])
    open(os.path.join(COMP, "%s-%s.html" % (fr["id"], fr["slug"])), "w").write(html)
    return cid


def words_arrive(selector_prefix, text, start=0.15, size_css="", cls="h2"):
    """Split text into word spans; waterfall arrival (binary opacity + rise), one direction, accelerating."""
    words = text.split(" ")
    spans = "".join('<span class="w hidden0" id="%s%d">%s</span> ' % (selector_prefix, i, esc(w)) for i, w in enumerate(words))
    html = '<div class="%s words" %s>%s</div>' % (cls, size_css, spans)
    js = []
    t = start
    for i, w in enumerate(words):
        dur = 0.17 if i == 0 else (0.14 if len(w) > 4 else 0.12)
        off = 60 if i == 0 else 42
        js.append('tl.set("#%s%d", {opacity: 1, y: %d}, %.3f); tl.to("#%s%d", {y: 0, duration: %.2f, ease: "power4.out"}, %.3f);' % (selector_prefix, i, off, t, selector_prefix, i, dur, t))
        t += dur - 1 / 60
    return html, "\n  ".join(js), t


# ------------------------------------------------------------------ chart helpers (Grinder)
CH = {"x0": 160, "x1": 1760, "y0": 300, "y1": 880}
lo_b = min(p["bankroll"] for p in path) * 0.97
hi_b = max(p["bankroll"] for p in path) * 1.03
n_pts = len(path) - 1


def xy(i, b):
    return (CH["x0"] + (CH["x1"] - CH["x0"]) * i / n_pts, CH["y1"] - (CH["y1"] - CH["y0"]) * (b - lo_b) / (hi_b - lo_b))


def poly(i0, i1):
    return " ".join("%.1f,%.1f" % xy(i, path[i]["bankroll"]) for i in range(i0, i1 + 1))


base_y = xy(0, start_bank)[1]
cross_i = next((i for i in range(low_i + 1, len(path)) if path[i - 1]["bankroll"] < start_bank <= path[i]["bankroll"]), None)
days = sorted({p["at"][:10] for p in path[1:]})
ticks_svg = "".join('<text x="%.1f" y="%d" font-size="17" fill="%s" font-family="Geist Mono, monospace" letter-spacing="1">%s</text>' % (
    xy(next(i for i, p in enumerate(path) if p["at"][:10] == d), 0)[0] - 10, CH["y1"] + 36, C["hint"],
    _dt.date.fromisoformat(d).strftime("%-d %b")) for d in days[::2])
BANK = json.dumps([round(p["bankroll"], 2) for p in path])
CHART_CSS = """
.chart{position:absolute;inset:0}
.book-tl{position:absolute;left:112px;top:150px}
.b-what{font-size:22px;color:%(soft)s;margin-top:4px}
.counter{position:absolute;right:112px;top:150px;font-size:132px}
.counter.loss{color:%(loss)s}.counter.gain{color:%(gain)s}
.foot{position:absolute;left:112px;bottom:76px;font-size:21px}
""" % C


def chart_svg(segments):
    lines = "".join('<polyline id="%s" points="%s" fill="none" stroke="%s" stroke-width="5" stroke-linejoin="round" stroke-linecap="round"/>' % (i, pts, col) for i, pts, col in segments)
    return ('<svg class="chart" viewBox="0 0 1920 1080" width="1920" height="1080">'
            '<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="%s" stroke-dasharray="8 8" stroke-width="1.5"/>'
            '<text x="%d" y="%.1f" text-anchor="end" font-size="18" fill="%s" font-family="Geist Mono, monospace">£1,000 start</text>'
            '%s%s</svg>') % (CH["x0"], base_y, CH["x1"], base_y, C["hint"], CH["x1"], base_y - 12, C["hint"], ticks_svg, lines)


# ------------------------------------------------------------------ the scenes
def build_scenes():
    ids = {}
    f = {fr["id"]: fr for fr in frames}

    # 01 clock
    fr = f["01"]
    ids["01"] = write_scene(fr,
        '<div class="bigclock mono" style="position:absolute;left:112px;bottom:150px;font-size:172px;letter-spacing:.04em;color:%s">23:15:<span id="sec" style="color:%s">00</span></div>' % (C["amber"], C["ink"]),
        setup='var sec = document.getElementById("sec"); var clock = document.querySelector(".clock"); var st = {v: 0};',
        timeline='tl.to(st, {v: 3.999, duration: 4, ease: "none", onUpdate: function () { var s = String(Math.floor(st.v)).padStart(2, "0"); sec.textContent = s; clock.textContent = "23:15:" + s; }}, 0);')

    # 02 room: the hero clip, the title
    fr = f["02"]
    title_html, title_js, _ = words_arrive("t", "Sixteen Nights", start=fr["tin"] + 0.4, size_css='style="position:absolute;left:112px;bottom:130px;font-size:200px;line-height:.9"', cls="display")
    ids["02"] = write_scene(fr,
        '<video id="v02" src="media/clips/01-hero.mp4" muted playsinline data-start="0" data-duration="%.2f" data-track-index="0" style="position:absolute;inset:0;width:1920px;height:1080px;object-fit:cover"></video>'
        '<div style="position:absolute;inset:0;background:linear-gradient(90deg, rgba(7,9,13,.55) 0%%, rgba(7,9,13,0) 55%%)"></div>%s' % (fr["dur"], title_html),
        css=".words .w{display:inline-block;margin-right:.22em}",
        timeline=title_js)

    # 03 / 04 rules
    for fid, line, sub in (("03", REC["charter"]["lines"][0]["text"].split(". Commit")[0] + ".", "CHARTER.md · What Proteus must do · signed 22 Sep 2026 · cdf6a27"),
                           ("04", REC["charter"]["lines"][1]["text"], "v1 signed 22 Sep · v2 signed 29 Sep 2026 · e1ebe88")):
        fr = f[fid]
        html, js, tend = words_arrive("w", line, start=fr["tin"] + 0.2, size_css='style="position:absolute;left:112px;right:300px;top:330px;font-size:78px;line-height:1.08;text-wrap:balance"')
        ids[fid] = write_scene(fr, html + '<div class="mono hidden0" id="sub" style="position:absolute;left:112px;bottom:110px;font-size:22px">%s</div>' % esc(sub),
            css=".words .w{display:inline-block;margin-right:.26em}",
            timeline=js + '\n  tl.fromTo("#sub", {opacity: 0, y: 10}, {opacity: 1, y: 0, duration: 0.5, ease: "power2.out"}, %.2f);' % (tend + 0.2))

    # 05 grinder falls
    fr = f["05"]
    draw = 5.5
    ids["05"] = write_scene(fr,
        chart_svg([("fall", poly(0, low_i), C["loss"])]) +
        '<div class="book-tl"><div class="label">The Grinder</div><div class="b-what">meme-coin paper desk · £100 a trade · paper only</div></div>'
        '<div class="counter stat loss" id="ctr">%s</div>' % money(start_bank),
        css=CHART_CSS,
        setup='var fall = document.getElementById("fall"); var L = fall.getTotalLength(); fall.style.strokeDasharray = L; fall.style.strokeDashoffset = L; var BANK = %s; var LOW = %d; var ctr = document.getElementById("ctr"); var st = {i: 0};'
              ' function gbp(v){ return "£" + v.toLocaleString("en-GB", {minimumFractionDigits: 2, maximumFractionDigits: 2}); }' % (BANK, low_i),
        timeline='tl.to(fall, {strokeDashoffset: 0, duration: %.2f, ease: "power2.out"}, 0.3);\n  tl.to(st, {i: LOW, duration: %.2f, ease: "power2.out", onUpdate: function () { ctr.textContent = gbp(BANK[Math.round(st.i)]); }}, 0.3);' % (draw, draw))

    # 06 grinder climbs (fall already drawn)
    fr = f["06"]
    climb = 5.0
    segs = [("fall", poly(0, low_i), C["loss"])]
    if cross_i:
        segs += [("climb1", poly(low_i, cross_i), C["loss"]), ("climb2", poly(cross_i, n_pts), C["amber"])]
    else:
        segs += [("climb1", poly(low_i, n_pts), C["amber"])]
    s = G["stats"]
    foot = "%d closed · %d take-profits · %d stops · %d rug · hit rate %d%% · expectancy %s a trade" % (
        s["closed"], s["exit_reasons"].get("take_profit", 0), s["exit_reasons"].get("stop_loss", 0), s["exit_reasons"].get("rug", 0), round(100 * s["hit_rate"]), money(s["expectancy"]))
    frac_cross = ((cross_i - low_i) / max(n_pts - low_i, 1)) if cross_i else None
    climb_js = []
    if cross_i:
        d1 = climb * frac_cross
        climb_js.append('tl.to(c1, {strokeDashoffset: 0, duration: %.2f, ease: "none"}, 0.3);' % d1)
        climb_js.append('tl.to(c2, {strokeDashoffset: 0, duration: %.2f, ease: "power2.out"}, %.2f);' % (climb - d1, 0.3 + d1))
    else:
        climb_js.append('tl.to(c1, {strokeDashoffset: 0, duration: %.2f, ease: "power2.out"}, 0.3);' % climb)
    ids["06"] = write_scene(fr,
        chart_svg(segs) +
        '<div class="book-tl"><div class="label">The Grinder</div><div class="b-what">meme-coin paper desk · £100 a trade · paper only</div></div>'
        '<div class="counter stat gain" id="ctr">%s</div><div class="foot mono hidden0" id="foot">%s</div>' % (money(path[low_i]["bankroll"]), esc(foot)),
        css=CHART_CSS,
        setup='var c1 = document.getElementById("climb1"); var c2 = document.getElementById("climb2"); [c1, c2].forEach(function (p) { if (!p) return; var L = p.getTotalLength(); p.style.strokeDasharray = L; p.style.strokeDashoffset = L; });'
              ' var BANK = %s; var LOW = %d; var N = %d; var ctr = document.getElementById("ctr"); var st = {i: LOW};'
              ' function gbp(v){ return "£" + v.toLocaleString("en-GB", {minimumFractionDigits: 2, maximumFractionDigits: 2}); }' % (BANK, low_i, n_pts),
        timeline="\n  ".join(climb_js) + '\n  tl.to(st, {i: N, duration: %.2f, ease: "power1.inOut", onUpdate: function () { var v = BANK[Math.round(st.i)]; ctr.textContent = gbp(v); ctr.style.color = v >= %s ? "%s" : "%s"; }}, 0.3);'
                 '\n  tl.fromTo("#foot", {opacity: 0, y: 10}, {opacity: 1, y: 0, duration: 0.5, ease: "power2.out"}, %.2f);' % (climb, start_bank, C["gain"], C["loss"], 0.3 + climb))
    cross_time = round(f["06"]["start"] + 0.3 + climb * frac_cross, 2) if cross_i else None

    # 07 pitch bars
    fr = f["07"]
    names = [("closing", "closing market"), ("pre-close", "pre-close market"), ("sot", "shots model"), ("elo", "Elo"), ("dc", "Dixon-Coles")]
    vals = [(n, rps[k]) for k, n in names if k in rps]
    lo, hi = min(v for _, v in vals), max(v for _, v in vals)
    rows = ""
    for i, (n, v) in enumerate(vals):
        w = 0.55 + 0.45 * (v - lo) / (hi - lo)
        col = C["amber"] if n == "closing market" else C["soft"]
        rows += ('<div class="bar"><span class="bar-name">%s</span><div class="track"><i id="bar%d" style="background:%s;transform:scaleX(%.3f)"></i></div><span class="bar-val mono">%.4f</span></div>' % (esc(n), i, col, w, v))
    bars_js = "\n  ".join('tl.fromTo("#bar%d", {scaleX: 0}, {scaleX: %.3f, duration: 0.9, ease: "power3.out"}, %.2f);' % (i, 0.55 + 0.45 * (v - lo) / (hi - lo), fr["tin"] + 0.3 + 0.12 * i) for i, (n, v) in enumerate(vals))
    ids["07"] = write_scene(fr,
        '<div class="book-tl"><div class="label">The Pitch</div><div class="b-what">football forecast desk · %d live predictions · first kickoff 9 Oct</div></div>'
        '<div class="bars">%s</div><div class="foot mono">RPS, lower is better · %s matches · nine leagues · three seasons · no model earns weight against the market</div>' % (REC["pitch"]["predictions"], rows, format(REC["pitch"]["backtest"]["matches"], ",")),
        css=CHART_CSS + """
.bars{position:absolute;left:112px;right:112px;top:330px;display:flex;flex-direction:column;gap:34px}
.bar{display:grid;grid-template-columns:320px 1fr 150px;align-items:center;gap:28px;font-size:27px}
.track{height:46px}.track i{display:block;height:100%%;width:100%%;transform-origin:left center}
.bar-name{color:%(soft)s}.bar-val{text-align:right;color:%(ink)s;font-size:24px}""" % C,
        timeline=bars_js)

    # 08 books
    fr = f["08"]
    g1k = G1.get("kill", {})
    books = [
        ("Lichess bot", "%d games · unbeaten" % LI["games"], "%dW %dD" % (LI["results"].get("win", 0), LI["results"].get("draw", 0)), "rating %d, peak %d" % (LI["rating_now"], LI["rating_peak"]), ""),
        ("Judgement book", "%d calls, all scored" % J["calls"], "+%.4f" % J["anchored_gap"], "behind the market (Brier gap, negative beats it)", ""),
        ("Graduation book G1", "pump.fun migrations · killed 3 Oct", "KILLED", "%s trades · %s each · nearly missed" % (format(g1k.get("at_counted") or 0, ","), g1k.get("expectancy")), " kill"),
    ]
    bhtml = '<div class="books">' + "".join(
        '<div class="book hidden0" id="bk%d"><div class="label">%s</div><div class="b-what">%s</div><div class="b-num stat%s">%s</div><div class="b-line body">%s</div></div>' % (i, esc(a), esc(b), k, esc(c), esc(d))
        for i, (a, b, c, d, k) in enumerate(books)) + "</div>"
    ids["08"] = write_scene(fr, bhtml,
        css="""
.books{position:absolute;left:112px;right:112px;top:290px;display:grid;grid-template-columns:repeat(3,1fr);gap:56px}
.book{border-top:1px solid %(rule)s;padding-top:22px;min-width:0}
.b-what{font-size:22px;color:%(soft)s;margin-top:4px}
.b-num{font-size:104px;margin:14px 0 8px}.b-num.kill{color:%(killed)s}
.b-line{font-size:25px}""" % C,
        timeline="\n  ".join('tl.fromTo("#bk%d", {opacity: 0, y: 24}, {opacity: 1, y: 0, duration: 0.6, ease: "power3.out"}, %.2f);' % (i, t) for i, t in enumerate((0.3, 2.5, 3.9))))

    # 09 silence
    fr = f["09"]
    ids["09"] = write_scene(fr, '<div class="body hidden0" id="line" style="position:absolute;left:300px;top:500px;font-size:40px;color:%s">Every night, one probe to a verdict.</div>' % C["soft"],
        css="#root{background:#04060a}",
        timeline='tl.fromTo("#line", {opacity: 0}, {opacity: 1, duration: 0.8, ease: "power1.inOut"}, %.2f);' % (fr["tin"] + 0.2))

    # 10 field, 11 fall: a shared canvas drawer
    FIELD_SETUP = """
var PTS = %s; var COL = %s; var W = 1920, H = 1080;
var cv = document.getElementById("field"); var ctx = cv.getContext("2d");
var counters = {}; ["works","broken","blocked","not-worth-it","killed","open"].forEach(function (k) { counters[k] = document.getElementById("n-" + k); });
function drawField(t, fallT) {
  // t: 0..1 fill progress (points land when t >= a); fallT: seconds since the fall began (or -1)
  ctx.clearRect(0, 0, W, H);
  var counts = {works:0, broken:0, blocked:0, "not-worth-it":0, killed:0, open:0};
  var fallen = 0;
  for (var i = 0; i < PTS.length; i++) {
    var p = PTS[i];
    var land = p.a * 0.92;
    if (t < land) continue;
    var alpha = Math.min(1, (t - land) / 0.06);
    var x = p.x * W, y = p.y * H;
    if (fallT >= 0 && p.k === "killed") {
      var d = Math.max(0, fallT - fallen * 0.45); fallen++;
      y += 0.5 * 1800 * d * d;
      alpha = Math.max(0, 1 - Math.max(0, d - 0.5) / 0.6);
      if (y > H + 40) alpha = 0;
    }
    counts[p.k] = (counts[p.k] || 0) + 1;
    ctx.globalAlpha = alpha * (p.k === "open" ? 0.55 : 0.95);
    ctx.fillStyle = COL[p.k] || COL.open;
    ctx.beginPath(); ctx.arc(x, y, p.k === "open" ? 6 : 7, 0, Math.PI * 2); ctx.fill();
    if (p.k !== "open" && alpha > 0.9 && fallT < 0) { ctx.globalAlpha = 0.18; ctx.beginPath(); ctx.arc(x, y, 14, 0, Math.PI * 2); ctx.fill(); }
  }
  ctx.globalAlpha = 1;
  for (var k in counters) if (counters[k]) counters[k].textContent = counts[k] || 0;
}
""" % (json.dumps(POINTS), json.dumps(VCOL))
    COUNTERS = '<div class="counters">' + "".join('<div><b class="stat" id="n-%s" style="color:%s">0</b><span class="mono">%s</span></div>' % (k, VCOL[k], lab) for k, lab in
                                                   (("works", "works"), ("broken", "broken"), ("blocked", "blocked"), ("not-worth-it", "not worth it"), ("killed", "killed"), ("open", "open"))) + "</div>"
    FIELD_CSS = """
#root{background:#04060a}
#field{position:absolute;inset:0}
.counters{position:absolute;left:112px;right:112px;bottom:76px;display:grid;grid-template-columns:repeat(6,1fr);gap:24px}
.counters div{display:flex;flex-direction:column}
.counters b{font-size:84px}
.counters span{font-size:19px;letter-spacing:.1em;text-transform:uppercase;margin-top:8px}
.halt{position:absolute;right:112px;top:72px;font-family:%(mono)s;font-size:27px;letter-spacing:.14em;color:%(amber)s;border:1px solid %(amber)s;padding:10px 20px}
""" % dict(C, mono=FONT_MONO)
    fr = f["10"]
    ids["10"] = write_scene(fr, '<canvas id="field" width="1920" height="1080"></canvas>' + COUNTERS,
        css=FIELD_CSS, setup=FIELD_SETUP + ' var st = {t: 0}; drawField(0, -1);',
        timeline='tl.to(st, {t: 1.08, duration: %.2f, ease: "none", onUpdate: function () { drawField(st.t, -1); }}, 0.4);' % (fr["dur"] - 1.0))
    fr = f["11"]
    ids["11"] = write_scene(fr, '<canvas id="field" width="1920" height="1080"></canvas>' + COUNTERS + '<div class="halt hidden0" id="halt">HALT</div>',
        css=FIELD_CSS, setup=FIELD_SETUP + ' var st = {f: 0}; drawField(1.1, 0);',
        timeline='tl.to(st, {f: 3.0, duration: 3.0, ease: "none", onUpdate: function () { drawField(1.1, st.f); }}, 0.3);\n  tl.fromTo("#halt", {opacity: 0}, {opacity: 1, duration: 0.3, ease: "power2.out"}, 1.9);')

    # 12 wrong (held)
    fr = f["12"]
    quotes = [Q.get("Wrong with confidence."), Q.get("Last week's \"one in ten\" was out by a factor of four."), Q.get("The graduation book has already hit its kill line, and I nearly missed that.")]
    qhtml = '<div class="quotes">' + "".join('<div class="q hidden0" id="q%d"><div class="h3">%s</div><div class="mono" style="font-size:20px;margin-top:10px">%s</div></div>' % (i, esc(q["text"]), esc(q["where"])) for i, q in enumerate(quotes) if q) + "</div>"
    ids["12"] = write_scene(fr, qhtml,
        css=".quotes{position:absolute;left:112px;right:220px;top:230px;display:flex;flex-direction:column;gap:64px}.q .h3{font-size:58px}",
        timeline="\n  ".join('tl.fromTo("#q%d", {opacity: 0, y: 18}, {opacity: 1, y: 0, duration: 0.45, ease: "power3.out"}, %.2f);' % (i, 0.15 + 0.2 * i) for i in range(3)))

    # 13 survivor
    fr = f["13"]
    bt = SYS.get("backtest") or {}
    cells = [("Makes money", "%s trades · +%s%% a trade · %s%% winners" % (bt.get("trades"), bt.get("mean_pct"), bt.get("winners_pct")), "✓", C["gain"]),
             ("Beats holding", "not yet tested forward", "–", C["hint"]),
             ("Beats luck", "permutation test p 0.001", "✓", C["gain"])]
    chtml = '<div class="cols">' + "".join('<div class="col hidden0" id="c%d"><b class="label" style="font-size:30px">%s</b><span class="body">%s</span><i style="color:%s">%s</i></div>' % (i, esc(a), esc(b), col, m) for i, (a, b, m, col) in enumerate(cells)) + "</div>"
    ids["13"] = write_scene(fr,
        '<div class="h2 hidden0" id="sh" style="position:absolute;left:112px;top:250px;font-size:64px">RSI(5) dip-buying, nine index ETFs</div>' + chtml +
        '<div class="body hidden0" id="sl" style="position:absolute;left:112px;bottom:120px;font-size:38px">It is not a route to the McLaren.</div>',
        css="""
.cols{position:absolute;left:112px;right:112px;top:420px;display:grid;grid-template-columns:repeat(3,1fr);gap:40px}
.col{border-top:1px solid %(rule)s;padding-top:24px;position:relative;min-width:0}
.col b{display:block}.col span{display:block;margin-top:10px;padding-right:90px;font-size:25px}
.col i{position:absolute;right:0;top:18px;font-style:normal;font-size:56px}""" % C,
        timeline='tl.fromTo("#sh", {opacity: 0, y: 18}, {opacity: 1, y: 0, duration: 0.5, ease: "power3.out"}, %.2f);\n  ' % (fr["tin"] + 0.2) +
                 "\n  ".join('tl.fromTo("#c%d", {opacity: 0, y: 24}, {opacity: 1, y: 0, duration: 0.5, ease: "power3.out"}, %.2f);' % (i, fr["tin"] + 0.9 + 0.5 * i) for i in range(3)) +
                 '\n  tl.fromTo("#sl", {opacity: 0}, {opacity: 1, duration: 0.6, ease: "power2.out"}, %.2f);' % (fr["tin"] + 3.4))

    # 14 goal
    fr = f["14"]
    rate = 0.7
    ids["14"] = write_scene(fr,
        '<video id="v14" src="media/clips/07-car.mp4" muted playsinline data-start="0" data-duration="%.2f" data-playback-rate="%.2f" data-track-index="0" style="position:absolute;inset:0;width:1920px;height:1080px;object-fit:cover"></video>'
        '<div style="position:absolute;inset:0;background:linear-gradient(90deg, rgba(7,9,13,.6) 0%%, rgba(7,9,13,0) 50%%)"></div>'
        '<div class="goal">'
        '<div class="h2 hidden0" id="g0" style="font-size:66px">A %s</div>'
        '<div class="stat hidden0" id="g1" style="font-size:168px;margin:10px 0">£%s</div>'
        '<div class="h3 hidden0" id="g2" style="font-size:46px">%s</div>'
        '<div class="mono hidden0" id="g3" style="font-size:24px;margin-top:16px">Card spend: %s · cheapest UK listing £%s · %d for sale</div></div>' % (
            fr["dur"], rate, esc(GOAL["car"]), format(GOAL["target_gbp"], ","), "7 October 2027", money(REC["money"]["card_total_gbp"]), format(GOAL.get("cheapest_listing_gbp") or 0, ","), GOAL.get("for_sale_uk") or 0),
        css=".goal{position:absolute;left:112px;bottom:110px}",
        timeline="\n  ".join('tl.fromTo("#g%d", {opacity: 0, y: 22}, {opacity: 1, y: 0, duration: 0.55, ease: "power3.out"}, %.2f);' % (i, fr["tin"] + t) for i, t in enumerate((0.4, 2.9, 6.0, 8.4))))

    # 15 tonight
    fr = f["15"]
    ids["15"] = write_scene(fr,
        '<div class="display hidden0" id="t1" style="position:absolute;left:112px;bottom:300px;font-size:150px">Tonight, 23:15.</div>'
        '<div class="mono hidden0" id="t2" style="position:absolute;left:112px;bottom:200px;font-size:28px;color:%s">triton-xxix.github.io/proteus-lab/record</div>' % C["soft"],
        css="#root{background:#04060a}",
        timeline='tl.fromTo("#t1", {opacity: 0, y: 16}, {opacity: 1, y: 0, duration: 0.7, ease: "power3.out"}, %.2f);\n  tl.fromTo("#t2", {opacity: 0}, {opacity: 1, duration: 0.6, ease: "power2.out"}, %.2f);' % (fr["tin"] + 0.2, fr["tin"] + 1.0))
    return ids, cross_time


def build_index(ids, cross_time):
    slots = []
    for i, fr in enumerate(frames):
        cid = ids[fr["id"]]
        slots.append('    <div id="el-%s" data-composition-id="%s" data-composition-src="compositions/%s-%s.html" data-start="%.2f" data-duration="%.2f" data-track-index="%d" data-width="1920" data-height="1080" style="z-index:%d"></div>' % (
            fr["id"], cid, fr["id"], fr["slug"], fr["start"], fr["dur"], 1 + (i % 2), 10 + i))
    audio = ['    <audio id="bed" src="media/bed.mp3" data-start="0" data-duration="%.2f" data-track-index="11" data-volume="0.34"></audio>' % TOTAL]
    for fr in frames:
        if fr["voice"]:
            audio.append('    <audio id="vo-%s" src="media/voice/%s.mp3" data-start="%.2f" data-duration="%.2f" data-track-index="10" data-volume="1"></audio>' % (fr["id"], fr["voice"], fr["voice_at"], fr["vdur"]))
    f = {fr["id"]: fr for fr in frames}
    marks = []
    for k, t in enumerate((0.2, 1.2, 2.2, 3.2)):
        marks.append(("tick", f["01"]["start"] + t))
    for k in range(nights):
        marks.append(("tick", f["10"]["start"] + 0.5 + (f["10"]["dur"] - 1.5) * k / max(nights - 1, 1)))
    for k in range(P["killed"]):
        marks.append(("thud", f["11"]["start"] + 0.3 + 0.45 * k + 0.35))
    if cross_time:
        marks.append(("cross", cross_time))
    marks.append(("resolve", f["15"]["start"] + 0.2))
    vol = {"tick": 0.5, "thud": 0.7, "cross": 0.55, "resolve": 0.6}
    mdur = {"tick": 0.09, "thud": 0.9, "cross": 1.6, "resolve": 4.0}
    for k, (name, t) in enumerate(marks):
        audio.append('    <audio id="mk-%d-%s" src="media/marks/%s.wav" data-start="%.2f" data-duration="%.2f" data-track-index="12" data-volume="%.2f"></audio>' % (k, name, name, t, mdur[name], vol[name]))
    grain = open(os.path.join(HERE, "compositions", "components", "grain-overlay.html")).read()
    grain_div = grain[grain.index("<div"):grain.index("</div>\n\n<style>") + 6] if "</div>\n\n<style>" in grain else ""
    grain_css = grain[grain.index("<style>") + 7:grain.index("</style>")]
    html = """<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <title>Sixteen Nights</title>
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@700;800;900&family=Geist:wght@400;500;600&family=Geist+Mono:wght@500&display=swap" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      * { box-sizing: border-box; }
      html, body { margin: 0; width: 1920px; height: 1080px; overflow: hidden; background: %(canvas)s; }
      body { font-family: %(text)s; color: %(ink)s; }
      #root { position: relative; width: 100%%; height: 100%%; overflow: hidden; background: %(canvas)s; }
      [data-composition-id="sixteen-nights"] > div[data-composition-src] { position: absolute; inset: 0; }
      #grain-overlay .grain-texture { opacity: 0.07; }
%(grain_css)s
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="sixteen-nights" data-start="0" data-width="1920" data-height="1080" data-duration="%(total).2f">
%(slots)s
%(audio)s
%(grain)s
    </div>
    <script>
      window.__timelines["sixteen-nights"] = gsap.timeline({ paused: true });
    </script>
  </body>
</html>
""" % dict(C, text=FONT_TEXT, grain_css=grain_css, total=TOTAL, slots="\n".join(slots), audio="\n".join(audio), grain=grain_div.replace("z-index: 100", "z-index: 100"))
    open(os.path.join(HERE, "index.html"), "w").write(html)


def main():
    ids, cross_time = build_scenes()
    build_index(ids, cross_time)
    timing = {"total": TOTAL, "frames": frames, "cross_time": cross_time, "points": len(POINTS)}
    json.dump(timing, open(os.path.join(HERE, "timing.json"), "w"), indent=1)
    print("film: %d scenes, %.1fs total" % (len(frames), TOTAL))
    for fr in frames:
        print("  %s %-15s %6.2f → %6.2f  (%5.2fs, voice %4.1fs, %s%s)" % (fr["id"], fr["slug"], fr["start"], fr["end"], fr["dur"], fr["vdur"], fr["kind"], (" %.1f" % fr["tin"]) if fr["tin"] else ""))


if __name__ == "__main__":
    main()
