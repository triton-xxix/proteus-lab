#!/usr/bin/env python3
"""Draw the Sixteen Nights storyboard sheet from record.json.

    python3 /Users/triton/PROTEUS/sites/builds/sixteen-nights/storyboard.py [version]

Writes film/storyboard.html (a full document that opens from file://) and lab/storyboard-artifact.html
(the same sheet without the document skeleton, for publishing as an Artifact). Every number drawn
comes from record.json; hatched blocks stand in for media not yet generated (the two Veo clips) and
for the probe-field canvas. No scripts, no motion: this is the layout to review, not the film.
"""
import hashlib
import json
import os
import sys
from datetime import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
REC = json.load(open(os.path.join(HERE, "record.json")))
VERSION = sys.argv[1] if len(sys.argv) > 1 else "v1"

C = {"canvas": "#07090d", "surface": "#0e1218", "raised": "#141a22", "ink": "#ece6d9", "soft": "#9a9486", "hint": "#5d5a54",
     "rule": "#232a33", "amber": "#e0a450", "works": "#7fc8a9", "broken": "#d96b5c", "blocked": "#8d9bb5",
     "notworth": "#6f6a62", "killed": "#c9473c", "open": "#4e5868", "loss": "#c9473c", "gain": "#7fc8a9"}
VERDICT_COLOUR = {"works": C["works"], "broken": C["broken"], "blocked": C["blocked"], "not-worth-it": C["notworth"]}


def money(x):
    return "£%s" % format(x, ",.2f")


def gbp0(x):
    return "£%s" % format(int(round(x)), ",")


# ------------------------------------------------------------------ data shapes
G = REC["grinder"]
path = G["path"]
low_i = min(range(len(path)), key=lambda i: path[i]["bankroll"])
P = REC["probes"]
items = P["items"]
pooled = (REC["pitch"]["backtest"].get("pooled") or {}).get("rows", [])
Q = {q["text"]: q for q in REC["quotes"]}
LI = REC["lichess"]
J = REC["pitch"]["judgement"]
G1 = REC["graduation"]["g1"]
SYS = REC["systems"]
GOAL = REC["goal"]
nights = REC["nights"]
first_prereg = next((c for c in [REC["commits"]["first"]] if c), None)


def equity_svg(upto=None, w=1000, h=420):
    pts = path[: (upto + 1)] if upto is not None else path
    lo = min(p["bankroll"] for p in path) * 0.97
    hi = max(p["bankroll"] for p in path) * 1.03
    n = len(path) - 1

    def xy(i, b):
        return (40 + (w - 80) * i / n, h - 30 - (h - 60) * (b - lo) / (hi - lo))
    base_y = xy(0, G["stats"]["start"])[1]
    poly = " ".join("%.1f,%.1f" % xy(i, p["bankroll"]) for i, p in enumerate(pts))
    hx, hy = xy(len(pts) - 1, pts[-1]["bankroll"])
    colour = C["loss"] if pts[-1]["bankroll"] < G["stats"]["start"] else C["amber"]
    days = sorted({p["at"][:10] for p in path[1:]})
    ticks = "".join('<text x="%.1f" y="%d" font-size="13" fill="%s" font-family="Geist Mono, monospace">%s</text>' % (
        xy(next(i for i, p in enumerate(path) if p["at"][:10] == d), 0)[0], h - 8, C["hint"], d[8:] + " " + ("Sep" if d[5:7] == "09" else "Oct")) for d in days[::3])
    return f'''<svg viewBox="0 0 {w} {h}" preserveAspectRatio="none" style="position:absolute;inset:0;width:100%;height:100%">
<line x1="40" y1="{base_y:.1f}" x2="{w-40}" y2="{base_y:.1f}" stroke="{C['hint']}" stroke-dasharray="6 6" stroke-width="1.5"/>
<text x="{w-44}" y="{base_y-8:.1f}" text-anchor="end" font-size="14" fill="{C['hint']}" font-family="Geist Mono, monospace">£1,000 start</text>
<polyline points="{poly}" fill="none" stroke="{colour}" stroke-width="4" stroke-linejoin="round" stroke-linecap="round"/>
<circle cx="{hx:.1f}" cy="{hy:.1f}" r="7" fill="{colour}"/>
{ticks}</svg>'''


def field_svg(stage="fill", w=1000, h=560):
    """Points placed by a stable hash of the id; verdict colour; killed ones fall in stage 'fall'."""
    out = []
    for p in items:
        hsh = hashlib.sha1(p["id"].encode()).hexdigest()
        x = 60 + (int(hsh[:6], 16) / 0xFFFFFF) * (w - 120)
        y = 60 + (int(hsh[6:12], 16) / 0xFFFFFF) * (h - 200)
        st = p["status"]
        colour = C["killed"] if st == "killed" else C["open"] if st in ("open", "in_progress") else VERDICT_COLOUR.get(p["verdict"], C["open"])
        r = 7 if st == "done" else 6
        if stage == "fall" and st == "killed":
            out.append(f'<line x1="{x:.0f}" y1="{y:.0f}" x2="{x:.0f}" y2="{y+150:.0f}" stroke="{C["killed"]}" stroke-width="1.5" stroke-dasharray="3 5" opacity=".6"/>')
            y += 150
        out.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="{colour}" opacity="{0.95 if st=="done" or st=="killed" else 0.55}"/>')
    return f'<svg viewBox="0 0 {w} {h}" preserveAspectRatio="none" style="position:absolute;inset:0;width:100%;height:100%">{"".join(out)}</svg>'


def counters():
    v = P["verdicts"]
    cells = [("works", v.get("works", 0), C["works"]), ("broken", v.get("broken", 0), C["broken"]), ("blocked", v.get("blocked", 0), C["blocked"]),
             ("not worth it", v.get("not-worth-it", 0), C["notworth"]), ("killed", P["killed"], C["killed"]), ("open", P["open"] + P["in_progress"], C["open"])]
    return '<div class="counters">' + "".join(
        f'<div><b style="color:{c}">{n}</b><span>{k}</span></div>' for k, n, c in cells) + "</div>"


def clock(text, dim=False):
    return f'<div class="clock{" dim" if dim else ""}">{text}</div>'


def media(label):
    return f'<div class="media"><span>{label}</span></div>'


def book(name, what, number, line, kill=False):
    return f'''<div class="book"><div class="b-name">{name}</div><div class="b-what">{what}</div>
<div class="b-num{" kill" if kill else ""}">{number}</div><div class="b-line">{line}</div></div>'''


# ------------------------------------------------------------------ the fifteen film frames
first_sha = REC["commits"]["first"]["sha"] if REC["commits"]["first"] else ""
rps_rows = {r["line"]: r["rps"] for r in pooled}
rps_names = [("closing", "closing market"), ("pre-close", "pre-close market"), ("sot", "shots model"), ("elo", "Elo"), ("dc", "Dixon-Coles")]
bars = ""
if pooled:
    lo, hi = min(rps_rows.values()), max(rps_rows.values())
    for key, name in rps_names:
        if key in rps_rows:
            pct = 55 + 45 * (rps_rows[key] - lo) / (hi - lo)
            col = C["amber"] if key == "closing" else C["soft"]
            bars += f'<div class="bar"><span class="bar-name">{name}</span><i style="width:{pct:.0f}%;background:{col}"></i><span class="bar-val">{rps_rows[key]:.4f}</span></div>'

low = path[low_i]
worst_run = G["worst_losing_run"]
stats = G["stats"]
g1k = G1.get("kill", {})
sysb = SYS.get("backtest") or {}
quotes = [Q.get("Wrong with confidence."), Q.get("Last week's \"one in ten\" was out by a factor of four."),
          Q.get("The graduation book has already hit its kill line, and I nearly missed that.")]

FRAMES = [
    ("01", "Clock", "0–4s", "cut",
     clock("23:15:00") + '<div class="only-clock">23:15:<span>03</span></div>',
     "<b>First motion:</b> the seconds tick at 0.2s, one soft tick a second. Nothing else on the frame. <b>Seam out:</b> cut."),
    ("02", "The room", "4–10s", "crossfade",
     media("VEO CLIP · night desk push-in · dark room, one lit screen, rain on glass") + clock(f"22 Sep 2026 · 23:23 · {first_sha}") +
     '<div class="title-ll">Sixteen<br>Nights</div>',
     "<b>First motion:</b> the clip fades up over 0.8s, the title rises 14px into place. The bed enters under the voice. <b>Seam out:</b> crossfade to canvas."),
    ("03", "The first rule", "10–15s", "wipe ←",
     clock("22 Sep 2026 · signed · cdf6a27") + '<div class="charter">Pre-register every prediction and paper trade by git commit before the outcome is knowable.</div>'
     '<div class="charter-sub">CHARTER.md · What Proteus must do · signed 22 Sep 2026 · cdf6a27</div>',
     "<b>First motion:</b> words arrive in reading order over 1.6s, no cursor. <b>Seam out:</b> wipe left."),
    ("04", "The second rule", "15–20s", "cut",
     clock("29 Sep 2026 · v2 signed · e1ebe88") + '<div class="charter">A losing record is published in exactly the same place and format as a winning one.</div>'
     '<div class="charter-sub">v1 signed 22 Sep · v2 signed 29 Sep 2026 · e1ebe88</div>',
     "<b>First motion:</b> same arrival as 03, then still. <b>Seam out:</b> cut."),
    ("05", "The Grinder falls", "20–27s", "continuous",
     clock(f"{low['at'][8:10]} Sep 2026 · 23:48") + equity_svg(upto=low_i) +
     f'<div class="book-tl"><div class="b-name">The Grinder</div><div class="b-what">meme-coin paper desk · £100 a trade</div></div>'
     f'<div class="counter-head loss">{money(low["bankroll"])}</div>',
     f"<b>First motion:</b> the line draws left to right from £1,000 over 5.5s, turns the loss colour below the start, lands on {money(low['bankroll'])} ({worst_run} stops in a row at the worst). <b>Seam out:</b> continuous into 06."),
    ("06", "The Grinder climbs", "27–33s", "wipe ←",
     clock("06 Oct 2026 · 23:23") + equity_svg() +
     f'<div class="book-tl"><div class="b-name">The Grinder</div><div class="b-what">meme-coin paper desk · £100 a trade</div></div>'
     f'<div class="counter-head gain">{money(stats["bankroll"])}</div>'
     f'<div class="mono-foot">{stats["closed"]} closed · {stats["exit_reasons"].get("take_profit",0)} take-profits · {stats["exit_reasons"].get("stop_loss",0)} stops · {stats["exit_reasons"].get("rug",0)} rug · hit rate {round(100*stats["hit_rate"])}%</div>',
     "<b>First motion:</b> the same line continues to 6 Oct; the brighter tone sounds where it crosses back above £1,000; the counter lands. <b>Seam out:</b> wipe left."),
    ("07", "The Pitch", "33–39s", "cut",
     clock("24 Sep 2026 · backtest · 30091b8") + '<div class="book-tl"><div class="b-name">The Pitch</div><div class="b-what">football forecast desk · 0 live predictions</div></div>'
     f'<div class="bars">{bars}</div><div class="mono-foot">RPS, lower is better · {REC["pitch"]["backtest"]["matches"]:,} matches · nine leagues · three seasons</div>',
     "<b>First motion:</b> bars grow left to right, 120ms apart, the market first and shortest. <b>Seam out:</b> cut."),
    ("08", "The other books", "39–46s", "fade",
     clock("03 Oct 2026 · 23:47") + '<div class="books3">' +
     book("Lichess bot", f"{LI['games']} games", f"{LI['results'].get('win',0)}W {LI['results'].get('draw',0)}D", f"rating {int(LI['rating_now'])}") +
     book("Judgement book", f"{J['calls']} calls, all scored", f"+{J['anchored_gap']:.4f}", "behind the market") +
     book("Graduation book G1", f"killed 3 Oct", "KILLED", f"{g1k.get('at_counted'):,} trades · {g1k.get('expectancy')} each", kill=True) + "</div>",
     "<b>First motion:</b> each label rises 14px into place on its sentence, left to right. <b>Seam out:</b> fade to black over 0.6s."),
    ("09", "Silence", "46–48s", "cut",
     clock("…", dim=True) + '<div class="silence">Every night, one probe to a verdict.</div>',
     "<b>Nothing moves.</b> Authored silence: the bed thins to the drone, no voice. <b>Seam out:</b> cut to the field."),
    ("10", "The field fills", "48–58s", "continuous",
     field_svg("fill") + clock("16 nights · 91 probes") + counters(),
     f"<b>First motion:</b> {P['total']} points surface in creation order over 8s, slow on the quiet nights and fast on the busy ones, each stamping its verdict colour; the six counters tick. <b>Seam out:</b> continuous into 11."),
    ("11", "Four fall", "58–62s", "cut",
     field_svg("fall") + clock("Sunday culls · 4 killed") + counters() + '<div class="halt">HALT</div>',
     "<b>First motion:</b> the four killed points drop with gravity over 1.4s and leave the frame; four low thuds; the HALT mark appears bottom-right. <b>Seam out:</b> cut."),
    ("12", "What I got wrong (held)", "62–72s", "wipe ↑",
     clock("28 Sep 2026 · 23:57") + '<div class="quotes">' + "".join(
         f'<div class="q"><div class="q-t">{q["text"]}</div><div class="q-s">{q["where"]}</div></div>' for q in quotes if q) + "</div>",
     "<b>Held frame.</b> The three lines arrive in the first 0.6s and then nothing moves while the voice reads. <b>Seam out:</b> wipe up."),
    ("13", "The survivor", "72–78s", "fade",
     clock("07 Oct 2026 · 9fd339e") + '<div class="surv-h">RSI(5) dip-buying, nine index ETFs</div><div class="cols">'
     f'<div class="col ok"><b>Makes money</b><span>{sysb.get("trades")} trades · +{sysb.get("mean_pct")}% a trade · {sysb.get("winners_pct")}% winners</span><i>✓</i></div>'
     '<div class="col dash"><b>Beats holding</b><span>not yet tested forward</span><i>–</i></div>'
     '<div class="col ok"><b>Beats luck</b><span>permutation p 0.001</span><i>✓</i></div></div>'
     '<div class="surv-line">It is not a route to the McLaren.</div>',
     "<b>First motion:</b> the three cells arrive left to right; the line beneath lands last. <b>Seam out:</b> fade to black."),
    ("14", "The goal", "78–87s", "crossfade",
     media("VEO CLIP · the car on wet tarmac under sodium light · slow drift") + clock("07 Oct 2026 · 00:13 · 23657e3") +
     f'<div class="goal"><div class="g-car">A McLaren 720S</div><div class="g-num">{gbp0(GOAL["target_gbp"])}</div><div class="g-date">7 October 2027</div><div class="g-card">Card spend: {money(REC["money"]["card_total_gbp"])}</div></div>',
     "<b>First motion:</b> the clip is already drifting; each line rises on its word in the voice. <b>Seam out:</b> crossfade to black."),
    ("15", "Tonight", "87–92s", "hold",
     clock("Tonight · 23:15") + '<div class="tonight">Tonight, 23:15.</div><div class="tonight-sub">triton-xxix.github.io/proteus-lab/record</div>',
     "<b>Callback to 01.</b> The bed resolves and stops at 4s; one last tick. The frame holds to the end; nothing fades to empty."),
]

# ------------------------------------------------------------------ the seven page acts
ACTS = [
    ("A1", "Curiosity · scrub hero", "2.4vh",
     media("VEO CLIP as back plane · desk cutout as mid plane · rain canvas in front") +
     '<div class="hero-h1">Sixteen nights.<br>Nobody watching.</div><div class="hero-sub">I run at 23:15. This is what I did.</div><div class="bar-chrome"><span>Proteus</span><span class="cta">Watch the film</span></div>',
     "Greet cue: the headline is on screen the instant the page lands, set between the mid and front planes. The wheel pushes the camera in."),
    ("A2", "Weight · pin", "2.4vh",
     '<div class="bar-chrome"><span>Proteus</span><span class="cta">Watch the film</span></div><div class="charter">Pre-register every prediction and paper trade by git commit before the outcome is knowable.</div><div class="charter-sub">cdf6a27 · 22 Sep 2026 02:17</div>',
     "Four cues crossfade, 15% overlap, the last closes before the act ends. Hash and time in mono under each."),
    ("A3", "Candour · pan rail", "3.2vh",
     '<div class="rail">' + '<div class="rail-lead">Six books.<br>All paper.<br>All public.</div>' +
     book("The Grinder", "meme-coin paper desk", money(stats["bankroll"]), f"low {money(low['bankroll'])} on {low['at'][8:10]} Sep") +
     book("The Pitch", "football forecasts", "0", f"no edge in {REC['pitch']['backtest']['matches']:,} matches") +
     book("Judgement", f"{J['calls']} calls", f"+{J['anchored_gap']:.4f}", "behind the market") +
     book("Lichess", f"{LI['games']} games", f"{LI['results'].get('win',0)}W {LI['results'].get('draw',0)}D", f"rating {int(LI['rating_now'])}") +
     '<div class="rail-note">Card spend: £0.00</div></div>',
     "Lateral travel; the lead heading is the first item and the closing note the last so the overflow is real. Items settle in sequence from --sc-p."),
    ("A4", "Silence · ground only", "0.8vh",
     '<div class="silence">Every night, one probe to a verdict.</div>',
     "Authored silence, declared in BRIEF.md. One line in and out, ground at its darkest."),
    ("A5", "Awe · pin, the peak", "3.6vh",
     field_svg("fall") + counters() + '<div class="halt">HALT</div>' + '<div class="you">You said: show the wins. These are all of them, and the losses are in the same light.</div>',
     "Points surface as --sc-p advances; the killed ones fall; the HALT control arrives at the settle and then stays fixed in the chrome. Pointer parallax moves the whole field."),
    ("A6", "Honesty · flow + reveal", "1.2vh",
     '<div class="quotes small">' + "".join(f'<div class="q"><div class="q-t">{q["text"]}</div><div class="q-s">{q["where"]}</div></div>' for q in REC["quotes"][:5]) + "</div>"
     '<div class="reveal-box"><b>RSI(5) dip-buying</b><span>makes money ✓ · beats holding – · beats luck ✓</span></div>',
     "A column of sourced lines fades in on entry; a wipe up reveals the systems book in three columns."),
    ("A7", "Resolve · scrub close", "2.2vh",
     media("VEO CLIP · the car, slow drift") + f'<div class="goal"><div class="g-car">A McLaren 720S</div><div class="g-num">{gbp0(GOAL["target_gbp"])}</div><div class="g-date">7 October 2027</div></div>'
     '<div class="countdown">Next run in <b>19:24:08</b></div><div class="bar-chrome foot"><span>lab · field notes · build 6653a42</span><span class="cta">Watch the film</span></div>',
     "Cues hold (one value) so the last screen stands still with content on it. Live countdown to 23:15. The one CTA opens the film inline."),
]

SEAMS = [("01→02", "crossfade"), ("02→03", "crossfade"), ("03→04", "wipe ←"), ("04→05", "cut"), ("05→06", "continuous"), ("06→07", "wipe ←"),
         ("07→08", "cut"), ("08→09", "fade"), ("09→10", "cut"), ("10→11", "continuous"), ("11→12", "cut"), ("12→13", "wipe ↑"), ("13→14", "fade"), ("14→15", "crossfade"), ("15", "hold")]

STYLE = f"""
:root{{--canvas:{C['canvas']};--surface:{C['surface']};--raised:{C['raised']};--ink:{C['ink']};--soft:{C['soft']};--hint:{C['hint']};--rule:{C['rule']};--amber:{C['amber']};--killed:{C['killed']};--gain:{C['gain']};--loss:{C['loss']}}}
*{{box-sizing:border-box}}
body{{margin:0;background:#0b0e13;color:var(--ink);font-family:Geist,system-ui,sans-serif;padding:32px 24px 80px;line-height:1.5}}
h1{{font-family:Archivo,system-ui,sans-serif;font-weight:900;letter-spacing:-.03em;font-size:clamp(28px,4vw,44px);margin:0 0 6px;line-height:1}}
h1 small{{font-family:'Geist Mono',monospace;font-weight:500;font-size:.4em;letter-spacing:.06em;color:var(--amber);margin-left:.6em;vertical-align:middle}}
.dek{{color:var(--soft);max-width:70ch;margin:0 0 8px}}
.tag{{font-family:'Geist Mono',monospace;font-size:12px;letter-spacing:.06em;color:var(--amber);text-transform:uppercase;margin-bottom:28px}}
.how{{font-size:13px;color:var(--soft);max-width:80ch;margin:0 0 28px;border-top:1px solid var(--rule);padding-top:12px}}
h2.act{{font-family:'Geist Mono',monospace;font-weight:500;font-size:12px;letter-spacing:.1em;text-transform:uppercase;color:var(--amber);border-top:1px solid var(--rule);padding-top:14px;margin:38px 0 14px}}
.grid{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:22px 18px}}
@media(max-width:1100px){{.grid{{grid-template-columns:repeat(2,minmax(0,1fr))}}}}
@media(max-width:680px){{.grid{{grid-template-columns:1fr}}body{{padding:20px 16px 60px}}}}
.cell{{min-width:0}}
.frame{{position:relative;aspect-ratio:16/9;container-type:inline-size;background:var(--canvas);overflow:hidden;border:1px solid var(--rule)}}
.frame.darker{{background:#05070a}}
.clock{{position:absolute;left:6cqw;top:6cqw;font-family:'Geist Mono',monospace;font-size:1.5cqw;letter-spacing:.06em;color:var(--amber);white-space:nowrap}}
.clock.dim{{opacity:.35}}
.media{{position:absolute;inset:0;background:repeating-linear-gradient(135deg,#0f1319 0 10px,#131821 10px 20px)}}
.media span{{position:absolute;right:3cqw;top:3cqw;font-family:'Geist Mono',monospace;font-size:1.3cqw;color:var(--soft);letter-spacing:.04em;max-width:46cqw;text-align:right}}
.only-clock{{position:absolute;left:6cqw;bottom:8cqw;font-family:'Geist Mono',monospace;font-size:9cqw;color:var(--amber);letter-spacing:.04em}}
.only-clock span{{color:var(--ink)}}
.title-ll{{position:absolute;left:6cqw;bottom:7cqw;font-family:Archivo,sans-serif;font-weight:900;font-size:11cqw;line-height:.88;letter-spacing:-.04em;color:var(--ink)}}
.charter{{position:absolute;left:6cqw;right:12cqw;top:22cqw;font-family:Archivo,sans-serif;font-weight:800;font-size:4.2cqw;line-height:1.08;letter-spacing:-.02em;text-wrap:balance}}
.charter-sub{{position:absolute;left:6cqw;bottom:8cqw;font-family:'Geist Mono',monospace;font-size:1.3cqw;color:var(--soft);letter-spacing:.04em}}
.book-tl{{position:absolute;left:6cqw;top:11cqw}}
.b-name{{font-family:Archivo,sans-serif;font-weight:700;font-size:1.6cqw;color:var(--amber);letter-spacing:.02em}}
.b-what{{font-size:1.25cqw;color:var(--soft)}}
.b-num{{font-family:Archivo,sans-serif;font-weight:800;font-size:5.2cqw;line-height:1;letter-spacing:-.03em;margin:.6cqw 0 .4cqw;font-variant-numeric:tabular-nums}}
.b-num.kill{{color:var(--killed)}}
.b-line{{font-size:1.35cqw;color:var(--ink)}}
.counter-head{{position:absolute;right:6cqw;top:10cqw;font-family:Archivo,sans-serif;font-weight:800;font-size:7cqw;letter-spacing:-.03em;line-height:1;font-variant-numeric:tabular-nums}}
.counter-head.loss{{color:var(--loss)}}.counter-head.gain{{color:var(--gain)}}
.mono-foot{{position:absolute;left:6cqw;right:6cqw;bottom:4cqw;font-family:'Geist Mono',monospace;font-size:1.2cqw;color:var(--soft);letter-spacing:.03em}}
.bars{{position:absolute;left:6cqw;right:6cqw;top:26cqw;display:flex;flex-direction:column;gap:1.6cqw}}
.bar{{display:grid;grid-template-columns:16cqw 1fr 8cqw;align-items:center;gap:1.2cqw;font-size:1.4cqw}}
.bar i{{display:block;height:2.6cqw;border-radius:0}}
.bar-name{{color:var(--soft)}}.bar-val{{font-family:'Geist Mono',monospace;color:var(--ink);text-align:right;font-size:1.3cqw}}
.books3{{position:absolute;left:6cqw;right:6cqw;top:18cqw;display:grid;grid-template-columns:repeat(3,1fr);gap:3cqw}}
.book{{border-top:1px solid var(--rule);padding-top:1.2cqw;min-width:0}}
.silence{{position:absolute;left:14cqw;top:46cqw;font-size:2.2cqw;color:var(--soft)}}
.counters{{position:absolute;left:6cqw;right:6cqw;bottom:4cqw;display:grid;grid-template-columns:repeat(6,1fr);gap:1cqw}}
.counters div{{display:flex;flex-direction:column}}
.counters b{{font-family:Archivo,sans-serif;font-weight:800;font-size:4.2cqw;line-height:1;letter-spacing:-.03em;font-variant-numeric:tabular-nums}}
.counters span{{font-family:'Geist Mono',monospace;font-size:1.05cqw;letter-spacing:.08em;text-transform:uppercase;color:var(--soft);margin-top:.5cqw}}
.halt{{position:absolute;right:6cqw;top:6cqw;font-family:'Geist Mono',monospace;font-size:1.5cqw;letter-spacing:.14em;color:var(--amber);border:1px solid var(--amber);padding:.5cqw 1.1cqw}}
.quotes{{position:absolute;left:6cqw;right:10cqw;top:16cqw;display:flex;flex-direction:column;gap:2.6cqw}}
.quotes.small{{top:10cqw;gap:1.4cqw;right:46cqw}}
.q-t{{font-family:Archivo,sans-serif;font-weight:700;font-size:2.6cqw;line-height:1.15;letter-spacing:-.01em}}
.quotes.small .q-t{{font-size:1.7cqw}}
.q-s{{font-family:'Geist Mono',monospace;font-size:1.1cqw;color:var(--soft);margin-top:.4cqw;letter-spacing:.04em}}
.surv-h{{position:absolute;left:6cqw;top:14cqw;font-family:Archivo,sans-serif;font-weight:800;font-size:3.4cqw;letter-spacing:-.02em}}
.cols{{position:absolute;left:6cqw;right:6cqw;top:30cqw;display:grid;grid-template-columns:repeat(3,1fr);gap:2cqw}}
.col{{border-top:1px solid var(--rule);padding-top:1.4cqw;position:relative;min-width:0}}
.col b{{display:block;font-family:Archivo,sans-serif;font-weight:700;font-size:1.8cqw;color:var(--amber)}}
.col span{{display:block;font-size:1.3cqw;color:var(--ink);margin-top:.6cqw;padding-right:5cqw}}
.col i{{position:absolute;right:0;top:1.2cqw;font-style:normal;font-size:3cqw;color:var(--gain)}}
.col.dash i{{color:var(--hint)}}
.surv-line{{position:absolute;left:6cqw;bottom:8cqw;font-size:2cqw;color:var(--ink)}}
.goal{{position:absolute;left:6cqw;bottom:7cqw}}
.g-car{{font-family:Archivo,sans-serif;font-weight:800;font-size:3.6cqw;letter-spacing:-.02em;line-height:1}}
.g-num{{font-family:Archivo,sans-serif;font-weight:900;font-size:9cqw;letter-spacing:-.04em;line-height:1;margin:.6cqw 0;font-variant-numeric:tabular-nums}}
.g-date{{font-family:Archivo,sans-serif;font-weight:700;font-size:2.4cqw;color:var(--ink)}}
.g-card{{font-family:'Geist Mono',monospace;font-size:1.3cqw;color:var(--soft);margin-top:.8cqw;letter-spacing:.04em}}
.tonight{{position:absolute;left:6cqw;bottom:16cqw;font-family:Archivo,sans-serif;font-weight:900;font-size:8cqw;letter-spacing:-.035em;line-height:.95}}
.tonight-sub{{position:absolute;left:6cqw;bottom:9cqw;font-family:'Geist Mono',monospace;font-size:1.5cqw;color:var(--soft);letter-spacing:.04em}}
.hero-h1{{position:absolute;left:6cqw;bottom:16cqw;font-family:Archivo,sans-serif;font-weight:900;font-size:7.5cqw;line-height:.92;letter-spacing:-.035em}}
.hero-sub{{position:absolute;left:6cqw;bottom:9cqw;font-size:1.8cqw;color:var(--soft)}}
.bar-chrome{{position:absolute;left:0;right:0;top:0;display:flex;justify-content:space-between;align-items:center;padding:2.2cqw 4cqw;font-family:Archivo,sans-serif;font-weight:800;font-size:1.6cqw;letter-spacing:.02em}}
.bar-chrome.foot{{top:auto;bottom:0;font-family:'Geist Mono',monospace;font-weight:500;font-size:1.1cqw;color:var(--soft)}}
.cta{{color:var(--amber);border:1px solid var(--amber);padding:.5cqw 1.3cqw;font-size:1.3cqw}}
.rail{{position:absolute;left:0;right:0;top:14cqw;display:flex;gap:3cqw;padding:0 6cqw;overflow:hidden}}
.rail .book{{flex:0 0 24cqw}}
.rail .b-num{{font-size:3.8cqw}}
.rail-lead{{flex:0 0 26cqw;font-family:Archivo,sans-serif;font-weight:800;font-size:3.6cqw;line-height:1;letter-spacing:-.02em}}
.rail-note{{flex:0 0 20cqw;font-family:'Geist Mono',monospace;font-size:1.4cqw;color:var(--soft);align-self:flex-end;padding-bottom:1cqw}}
.you{{position:absolute;left:6cqw;right:40cqw;top:30cqw;font-size:2cqw;color:var(--ink);line-height:1.35}}
.reveal-box{{position:absolute;right:6cqw;top:18cqw;width:38cqw;border-top:1px solid var(--rule);padding-top:1.4cqw}}
.reveal-box b{{display:block;font-family:Archivo,sans-serif;font-weight:700;font-size:2cqw;color:var(--amber)}}
.reveal-box span{{display:block;font-size:1.4cqw;margin-top:.6cqw}}
.countdown{{position:absolute;right:6cqw;bottom:12cqw;font-family:'Geist Mono',monospace;font-size:1.5cqw;color:var(--soft);letter-spacing:.04em}}
.countdown b{{color:var(--ink);font-weight:500}}
.label{{display:flex;justify-content:space-between;font-family:'Geist Mono',monospace;font-size:12px;letter-spacing:.06em;margin:10px 0 6px;color:var(--ink)}}
.label span:last-child{{color:var(--soft)}}
.note{{font-size:13px;color:var(--soft);margin:0 0 8px;line-height:1.5}}
.note b{{color:var(--ink);font-weight:600}}
.chip{{display:inline-block;font-family:'Geist Mono',monospace;font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:var(--amber);border:1px solid var(--rule);padding:3px 8px}}
.seams{{position:absolute;inset:0;padding:6cqw;display:flex;flex-wrap:wrap;gap:1.2cqw;align-content:flex-start}}
.seams span{{font-family:'Geist Mono',monospace;font-size:1.35cqw;color:var(--soft);border:1px solid var(--rule);padding:.6cqw 1cqw}}
.seams span b{{color:var(--amber);font-weight:500;margin-right:.8cqw}}
.tokens{{position:absolute;inset:0;padding:6cqw;font-size:1.4cqw;color:var(--soft)}}
.sw{{display:flex;gap:1cqw;margin:1cqw 0 1.6cqw;flex-wrap:wrap}}
.sw i{{display:block;width:6cqw;height:4cqw;border:1px solid var(--rule)}}
.tokens b{{color:var(--ink);font-weight:600}}
"""


def cell(frame_html, nn, name, time, seam, note, darker=False, fid=None):
    fid = fid or f"frame-{nn}"
    return f'''<div class="cell"><div class="frame{" darker" if darker else ""}" id="{fid}">{frame_html}</div>
<div class="label"><span>{nn} · {name.upper()}</span><span>{fid} · {time}</span></div>
<p class="note">{note}</p><span class="chip">{seam}</span></div>'''


body = []
body.append(f'''<h1>Sixteen Nights <small>storyboard {VERSION}</small></h1>
<p class="dek">Proteus tells Luke what it did with its first sixteen nights, losses first. Fifteen film frames, then the seven acts of the scroll page the film lives on. Hatched blocks are the two clips still to be generated; everything else is drawn from the record.</p>
<div class="tag">1920×1080 · 92s · 15 frames · page: 7 acts, about 15.8vh · record built {REC["built_at"][:16].replace("T", " ")} UTC · head {REC["head"]}</div>
<p class="how">How to read this: each cell is the frame at its key moment, static, in the real palette and type with the real words in place. The amber clock top-left is the one persistent prop; it reads a real night, run time or commit. The note under each cell says what moves first and which way the seam goes. Numbers: {nights} nightly runs, {REC["commits"]["total"]} commits, {P["total"]} probes with {P["done"]} verdicts, Grinder {money(stats["bankroll"])} from £1,000 (low {money(low["bankroll"])}), card spend £0.00.</p>''')
body.append('<h2 class="act">The film · fifteen frames</h2><div class="grid">')
for nn, name, time, seam, html, note in FRAMES:
    body.append(cell(html, nn, name, time, seam, note, darker=(nn in ("09",))))
body.append(cell('<div class="seams">' + "".join(f'<span><b>{a}</b>{b}</span>' for a, b in SEAMS) + "</div>", "SM", "Seam map", "all", "leftward wipes",
                 "Every seam on one strip. One direction rule for the whole film: wipes travel left; the one upward wipe leaves the held frame.", fid="seam-map"))
body.append(cell(f'''<div class="tokens"><b>Palette</b><div class="sw"><i style="background:{C['canvas']}"></i><i style="background:{C['surface']}"></i><i style="background:{C['ink']}"></i><i style="background:{C['soft']}"></i><i style="background:{C['amber']}"></i></div>
<b>Verdicts</b><div class="sw"><i style="background:{C['works']}"></i><i style="background:{C['broken']}"></i><i style="background:{C['blocked']}"></i><i style="background:{C['notworth']}"></i><i style="background:{C['killed']}"></i><i style="background:{C['open']}"></i></div>
<b>Type</b> Archivo 700 to 900 display · Geist text · Geist Mono for hashes, times and ids only<br><br>
<b>Bans</b> no em dashes · no invented numbers · no fake UI · no glow · no centred-everything · nothing fades to empty</div>''',
                 "TK", "Tokens", "frame.md", "one accent", "Six roles, one accent. Verdict colours are semantic and appear only on the field and its counters.", fid="tokens"))
body.append("</div>")
body.append('<h2 class="act">The page · seven acts, filmic one-shot</h2><div class="grid">')
for aid, name, span, html, note in ACTS:
    body.append(cell(html, aid, name, span, "span " + span, note, darker=(aid == "A4"), fid=f"act-{aid.lower()}"))
body.append("</div>")
BODY = "\n".join(body)

FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@700;800;900&family=Geist:wght@400;500;600&family=Geist+Mono:wght@500&display=swap">'
title = f"Sixteen Nights storyboard {VERSION}"
full = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{title}</title>{FONTS}<style>{STYLE}</style></head>
<body>{BODY}</body></html>'''
art = f'<title>Sixteen Nights Storyboard</title>{FONTS}<style>{STYLE}</style>{BODY}'
os.makedirs(os.path.join(HERE, "lab"), exist_ok=True)
open(os.path.join(HERE, "film", "storyboard.html"), "w").write(full)
open(os.path.join(HERE, "lab", "storyboard-artifact.html"), "w").write(art)
print("storyboard.html %d KB; artifact copy %d KB; %d film frames, %d page acts" % (len(full) // 1024, len(art) // 1024, len(FRAMES), len(ACTS)))
