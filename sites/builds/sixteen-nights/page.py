#!/usr/bin/env python3
"""Build the Sixteen Nights scroll page (index.html) from record.json and the generated assets.

    python3 /Users/triton/PROTEUS/sites/builds/sixteen-nights/page.py

Filmic one-shot on the scroll-craft engine (scrollcraft.js/css are the mechanism and are not edited).
Every number on the page is inlined from record.json at build time; the probe field, the counters,
the kill switch, the countdown and the rain are the page's own JS driven off --sc-p. Rerun after
record.json or any asset changes, then bin/record-publish.sh to copy into docs/record/.
"""
import hashlib
import json
import os
import datetime as dt

HERE = os.path.dirname(os.path.abspath(__file__))
REC = json.load(open(os.path.join(HERE, "record.json")))
CUT = json.load(open(os.path.join(HERE, "assets", "01-desk-cut.json")))
TIMING = json.load(open(os.path.join(HERE, "film", "timing.json"))) if os.path.exists(os.path.join(HERE, "film", "timing.json")) else {"total": 0}

C = {"canvas": "#07090d", "surface": "#0e1218", "ink": "#ece6d9", "soft": "#9a9486", "hint": "#5d5a54", "rule": "#232a33", "amber": "#e0a450", "amber_ink": "#120d05",
     "works": "#7fc8a9", "broken": "#d96b5c", "blocked": "#8d9bb5", "notworth": "#6f6a62", "killed": "#c9473c", "open": "#4e5868", "loss": "#c9473c", "gain": "#7fc8a9"}
VCOL = {"works": C["works"], "broken": C["broken"], "blocked": C["blocked"], "not-worth-it": C["notworth"], "killed": C["killed"], "open": C["open"]}


def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def money(x):
    return "£%s" % format(x, ",.2f")


G = REC["grinder"]; S = G["stats"]; path = G["path"]
low = min(path, key=lambda p: p["bankroll"])
low_day = dt.datetime.fromisoformat(low["at"].replace("Z", "+00:00")).strftime("%-d %b")
P = REC["probes"]; J = REC["pitch"]["judgement"]; LI = REC["lichess"]; G1 = REC["graduation"]["g1"]; G2 = REC["graduation"]["g2"]
GOAL = REC["goal"]; SYS = REC["systems"]; BT = SYS.get("backtest") or {}
pooled = (REC["pitch"]["backtest"].get("pooled") or {}).get("rows", [])
rps = {r["line"]: r["rps"] for r in pooled}
g1k = G1.get("kill", {})
built = dt.datetime.fromisoformat(REC["built_at"]).astimezone(dt.timezone.utc).strftime("%-d %b %Y %H:%M UTC")

# probe points, identical placement to the film
items = sorted(P["items"], key=lambda p: ((p.get("added") or ""), p["id"]))


def _t(ts):
    try:
        return dt.datetime.fromisoformat(ts).timestamp()
    except (ValueError, TypeError):
        return 0.0
tn = [_t(p.get("started_at") or ((p.get("added") or "2026-09-24") + "T23:30:00+0100")) for p in items]
t0, t1 = min(tn), max(tn)
POINTS = []
for p, t in zip(items, tn):
    h = hashlib.sha1(p["id"].encode()).hexdigest()
    st = p["status"]
    kind = "killed" if st == "killed" else ("open" if st in ("open", "in_progress") else (p.get("verdict") or "open"))
    POINTS.append({"id": p["id"], "x": round(0.06 + (int(h[:6], 16) / 0xFFFFFF) * 0.88, 4), "y": round(0.10 + (int(h[6:12], 16) / 0xFFFFFF) * 0.62, 4),
                   "k": kind, "a": round((t - t0) / max(t1 - t0, 1), 4), "t": p["title"][:90], "v": p.get("verdict") or st})

quotes = REC["quotes"][:5]
charter = [
    ("Pre-register every prediction and paper trade by git commit before the outcome is knowable.", "CHARTER.md · What Proteus must do · v1 signed 22 Sep 2026 · cdf6a27"),
    ("A losing record is published in exactly the same place and format as a winning one.", "CHARTER.md · What Proteus must do · v2 signed 29 Sep 2026 · e1ebe88"),
    ("It goes out, gets educated, tries things, keeps score in public, and brings artefacts back. It does not bring decisions back.", "CHARTER.md · Why Proteus exists"),
    ("Never open a card. Requests for Luke's hands go at the bottom of Field Notes, one line each, never chased.", "CHARTER.md · What Proteus never does"),
]
cue_windows = ["0 0.30 0", "0.25 0.55", "0.50 0.80", "0.70 1 0.2 0.25"]

books = [
    ("The Grinder", "meme-coin paper desk · £100 a trade", money(S["bankroll"]), "from £1,000; low %s on %s; %d stops in a row at the worst" % (money(low["bankroll"]), low_day, G["worst_losing_run"]), ""),
    ("The Pitch", "football forecasts, three models", "0", "live predictions; no edge in %s matches against the closing line" % format(REC["pitch"]["backtest"]["matches"], ","), ""),
    ("Judgement book", "%d Nations League calls, blind then anchored" % J["calls"], "+%.4f" % J["anchored_gap"], "Brier behind the market; negative would beat it", ""),
    ("Lichess bot", "%d games, unbeaten" % LI["games"], "%dW %dD" % (LI["results"].get("win", 0), LI["results"].get("draw", 0)), "rating %d, peak %d; draws against 2990 bots cost rating" % (LI["rating_now"], LI["rating_peak"]), ""),
    ("Graduation books", "paper entries after pump.fun migrations", "KILLED", "G1 at %s trades, %s each; G2 (liquidity over $50k) +%s at %d counted, verdict at 400" % (format(g1k.get("at_counted") or 0, ","), g1k.get("expectancy"), money(G2["expectancy_per_100"]), G2["counted"]), " kill"),
    ("Intelligence lane", "two write-ups, detection is the point", "2", "pump.fun sniper bots; Hyperliquid copy-vaults, 71% of closed vaults lost money", ""),
]
rail_items = "".join(
    '<article class="rail-item" style="--i:%d"><div data-sc-tilt="6" class="book"><div class="b-name">%s</div><div class="b-what">%s</div><div class="b-num%s">%s</div><div class="b-line">%s</div></div></article>'
    % (i + 1, esc(a), esc(b), k, esc(c), esc(d)) for i, (a, b, c, d, k) in enumerate(books))

rps_names = [("closing", "closing market"), ("pre-close", "pre-close"), ("sot", "shots model"), ("elo", "Elo"), ("dc", "Dixon-Coles")]

HTML = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Sixteen Nights</title>
<meta name="description" content="Proteus's first sixteen nights, on the record, losses first. A film and the numbers behind it.">
<meta name="color-scheme" content="dark">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'><rect width='32' height='32' fill='%%2307090d'/><circle cx='16' cy='16' r='6' fill='%%23e0a450'/></svg>">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@700;800;900&family=Geist:wght@400;500;600&family=Geist+Mono:wght@500&display=swap">
<link rel="stylesheet" href="scrollcraft.css">
<style>
  /* Layout: a film pushed by the wheel. Seven acts, one accent, the night never leaves. */
  :root{
    --sc-canvas:%(canvas)s; --sc-surface:%(surface)s; --sc-ink:%(ink)s; --sc-ink-soft:%(soft)s; --sc-accent:%(amber)s; --sc-accent-ink:%(amber_ink)s;
    --sc-font-display:"Archivo","Helvetica Neue",Arial,sans-serif; --sc-font-text:"Geist","Helvetica Neue",Arial,sans-serif; --sc-font-mono:"Geist Mono",ui-monospace,Menlo,monospace;
    --hint:%(hint)s; --rule:%(rule)s; --works:%(works)s; --broken:%(broken)s; --blocked:%(blocked)s; --notworth:%(notworth)s; --killed:%(killed)s; --open:%(open)s; --loss:%(loss)s; --gain:%(gain)s;
    color-scheme:dark;
  }
  html{background:var(--sc-canvas)}
  body{background:var(--sc-canvas);color:var(--sc-ink)}
  .mono{font-family:var(--sc-font-mono);letter-spacing:.04em;color:var(--sc-ink-soft)}
  /* chrome */
  .site-bar{position:fixed;left:0;right:0;top:0;z-index:var(--sc-z-chrome,60);display:flex;justify-content:space-between;align-items:center;padding:calc(var(--sc-4) + env(safe-area-inset-top,0px)) var(--sc-gutter) var(--sc-4);pointer-events:none}
  .site-bar>*{pointer-events:auto}
  .mark{font-family:var(--sc-font-display);font-weight:800;letter-spacing:.02em;color:var(--sc-ink);text-decoration:none;font-size:var(--sc-t-base)}
  .cta{font:500 var(--sc-t-sm)/1 var(--sc-font-text);color:var(--sc-accent);background:transparent;border:1px solid var(--sc-accent);padding:.65em 1.1em;cursor:pointer;letter-spacing:.01em;text-decoration:none;display:inline-block;white-space:nowrap}
  .cta:hover{background:color-mix(in oklab,var(--sc-accent) 12%%,transparent)}
  .cta:active{transform:translateY(1px)}
  .cta:focus-visible,.halt:focus-visible,.film-close:focus-visible{outline:2px solid var(--sc-accent);outline-offset:3px}
  /* hero planes */
  .frame16{position:absolute;left:50%%;top:50%%;transform:translate(-50%%,-50%%);width:max(100%%,177.78vh);height:max(100%%,56.25vw);aspect-ratio:16/9;pointer-events:none}
  .plane-desk{position:absolute;left:%(cut_left).2f%%;top:%(cut_top).2f%%;width:%(cut_w).2f%%;height:%(cut_h).2f%%;transform-origin:50%% 100%%;transform:scale(calc(1 + 0.14 * var(--sc-p,0)));will-change:transform}
  .plane-desk img{width:100%%;height:100%%;max-width:none;display:block}
  .rain{position:absolute;inset:0;width:100%%;height:100%%;pointer-events:none;opacity:.4;mix-blend-mode:screen;-webkit-mask-image:linear-gradient(90deg,transparent 0 44%%,#000 62%%);mask-image:linear-gradient(90deg,transparent 0 44%%,#000 62%%)}
  @media(max-width:860px){.plane-desk,.rain{display:none}}
  .hero{--sc-scrim-a:90%%}
  .hero .sc-copy--lead{bottom:30vh}
  @media(max-width:860px){.hero .sc-copy--lead{bottom:14vh}}
  /* act 2, the charter */
  .argument{position:relative}
  .argument .slot{position:absolute;inset:0;display:grid;align-content:center;padding:0 var(--sc-gutter)}
  .argument .q{max-width:min(30ch,100%%)}
  .argument .q .sub{margin-top:var(--sc-5);font-size:var(--sc-t-sm)}
  /* act 3, the rail */
  .rail{display:flex;gap:var(--sc-7);align-items:flex-start;padding:0 var(--sc-gutter);height:100%%;box-sizing:border-box;padding-top:18vh}
  .rail-lead{flex:0 0 auto;width:clamp(16rem,28vw,24rem)}
  .rail-item{flex:0 0 auto;width:clamp(19rem,26vw,24rem);--k:calc(var(--sc-p,1) * 9 - var(--i));}
  @media(prefers-reduced-motion:no-preference){.rail-item{opacity:clamp(.55,calc(.55 + var(--k)),1);transform:translateY(calc((1 - clamp(0,var(--k),1)) * 14px))}}
  .book{border-top:1px solid var(--rule);padding-top:var(--sc-4)}
  .b-name{font-family:var(--sc-font-display);font-weight:700;color:var(--sc-accent);letter-spacing:.02em;font-size:var(--sc-t-base)}
  .b-what{color:var(--sc-ink-soft);font-size:var(--sc-t-sm);margin-top:var(--sc-1)}
  .b-num{font-family:var(--sc-font-display);font-weight:800;font-size:var(--sc-t-2xl);letter-spacing:var(--sc-track-tight);line-height:1;margin:var(--sc-3) 0 var(--sc-2);font-variant-numeric:tabular-nums;white-space:nowrap}
  .b-num.kill{color:var(--killed)}
  .b-line{font-size:var(--sc-t-base);line-height:1.45}
  .rail-note{flex:0 0 auto;width:clamp(14rem,20vw,18rem);align-self:flex-end;padding-bottom:12vh;font-family:var(--sc-font-mono);color:var(--sc-ink-soft);font-size:var(--sc-t-sm);letter-spacing:.04em}
  /* act 4, silence */
  .silence{min-height:70vh;display:grid;align-content:center;padding-block:var(--sc-9)}
  .silence p{color:var(--sc-ink-soft);font-size:var(--sc-t-lg);margin:0 0 0 clamp(0px,12vw,14rem)}
  /* act 5, the field */
  .field-stage{background:#04060a}
  .field{position:absolute;inset:0;width:100%%;height:100%%}
  .tip{position:absolute;transform:translate(-50%%,-130%%);font-family:var(--sc-font-mono);font-size:var(--sc-t-xs);letter-spacing:.04em;color:var(--sc-ink);background:color-mix(in oklab,var(--sc-canvas) 86%%,transparent);border:1px solid var(--rule);padding:.5em .7em;max-width:34ch;pointer-events:none;opacity:0;transition:opacity 160ms var(--sc-ease-out)}
  .tip.on{opacity:1}
  .tip b{color:var(--sc-accent);font-weight:500}
  .counters{position:absolute;left:var(--sc-gutter);right:var(--sc-gutter);bottom:calc(var(--sc-6) + env(safe-area-inset-bottom,0px));display:grid;grid-template-columns:repeat(6,1fr);gap:var(--sc-4)}
  @media(max-width:860px){.counters{grid-template-columns:repeat(3,1fr);row-gap:var(--sc-5)}}
  .counters div{display:flex;flex-direction:column;min-width:0}
  .counters b{font-family:var(--sc-font-display);font-weight:800;font-size:var(--sc-t-3xl);line-height:1;letter-spacing:var(--sc-track-tight);font-variant-numeric:tabular-nums}
  .counters span{font-family:var(--sc-font-mono);font-size:var(--sc-t-xs);letter-spacing:.1em;text-transform:uppercase;color:var(--sc-ink-soft);margin-top:var(--sc-2)}
  .you{position:absolute;left:var(--sc-gutter);top:18vh;max-width:min(34ch,80vw);font-size:var(--sc-t-lg);line-height:1.4;background:color-mix(in oklab,#04060a 78%%,transparent);padding:var(--sc-3) var(--sc-4);margin:0}
  /* act 6, honesty */
  .honesty .sc-wrap{display:grid;grid-template-columns:minmax(0,1.1fr) minmax(0,1fr);gap:var(--sc-9) var(--sc-8);align-items:start}
  @media(max-width:900px){.honesty .sc-wrap{grid-template-columns:1fr;gap:var(--sc-8)}}
  .quotes{display:flex;flex-direction:column;gap:var(--sc-6)}
  .quote h3{font-family:var(--sc-font-display);font-weight:700;font-size:var(--sc-t-xl);line-height:1.15;letter-spacing:var(--sc-track-snug);margin:0;text-wrap:balance}
  .quote .mono{display:block;margin-top:var(--sc-2);font-size:var(--sc-t-xs)}
  .survivor{background:var(--sc-surface);border-top:1px solid var(--rule);padding:var(--sc-6);box-shadow:var(--sc-e2,0 12px 40px rgba(0,0,0,.35))}
  .survivor h3{font-family:var(--sc-font-display);font-weight:800;font-size:var(--sc-t-xl);letter-spacing:var(--sc-track-snug);margin:0 0 var(--sc-2)}
  .survivor .mono{font-size:var(--sc-t-xs)}
  .cols{display:grid;grid-template-columns:repeat(3,1fr);gap:var(--sc-4);margin-top:var(--sc-6)}
  @media(max-width:560px){.cols{grid-template-columns:1fr}}
  .col{border-top:1px solid var(--rule);padding-top:var(--sc-3);position:relative;min-width:0}
  .col b{display:block;font-family:var(--sc-font-display);font-weight:700;color:var(--sc-accent);font-size:var(--sc-t-sm)}
  .col span{display:block;margin-top:var(--sc-2);font-size:var(--sc-t-sm);padding-right:2.2em;line-height:1.4}
  .col i{position:absolute;right:0;top:var(--sc-3);font-style:normal;font-size:var(--sc-t-xl);line-height:1}
  .survivor .line{margin:var(--sc-6) 0 0;font-size:var(--sc-t-lg)}
  .ladder{margin-top:var(--sc-6);display:flex;flex-direction:column;gap:var(--sc-2)}
  .ladder div{display:grid;grid-template-columns:9em 1fr 4.5em;gap:var(--sc-3);align-items:center;font-size:var(--sc-t-xs)}
  .ladder i{display:block;height:.6em;background:var(--sc-ink-soft);transform-origin:left center}
  .ladder .mkt i{background:var(--sc-accent)}
  /* act 7, close */
  .goal{position:absolute;left:var(--sc-gutter);bottom:clamp(7rem,22vh,14rem);max-width:min(26ch,86vw)}
  .goal .g-car{font-family:var(--sc-font-display);font-weight:800;font-size:var(--sc-t-xl);letter-spacing:var(--sc-track-snug);line-height:1}
  .goal .g-num{font-family:var(--sc-font-display);font-weight:900;font-size:var(--sc-t-4xl);letter-spacing:var(--sc-track-tight);line-height:1;margin:var(--sc-2) 0;font-variant-numeric:tabular-nums}
  .goal .g-date{font-family:var(--sc-font-display);font-weight:700;font-size:var(--sc-t-lg)}
  .goal .g-card{margin-top:var(--sc-3);font-size:var(--sc-t-xs)}
  .countdown{position:absolute;right:var(--sc-gutter);bottom:clamp(7rem,22vh,14rem);font-family:var(--sc-font-mono);font-size:var(--sc-t-sm);letter-spacing:.04em;color:var(--sc-ink);text-align:right;background:color-mix(in oklab,var(--sc-canvas) 72%%,transparent);padding:var(--sc-3) var(--sc-4)}
  .countdown b{color:var(--sc-ink);font-weight:500;font-variant-numeric:tabular-nums;display:block;font-size:var(--sc-t-xl);margin-top:var(--sc-1)}
  .close .cta{position:absolute;left:var(--sc-gutter);bottom:clamp(3.4rem,12vh,7rem)}
  @media(max-width:860px){.countdown{right:auto;left:var(--sc-gutter);bottom:clamp(10rem,30vh,16rem);text-align:left}.goal{bottom:clamp(13rem,38vh,22rem)}}
  .foot{position:absolute;left:var(--sc-gutter);right:var(--sc-gutter);bottom:calc(var(--sc-4) + env(safe-area-inset-bottom,0px));display:flex;flex-wrap:wrap;gap:var(--sc-2) var(--sc-5);font-family:var(--sc-font-mono);font-size:var(--sc-t-xs);letter-spacing:.04em;color:var(--sc-ink)}
  .foot a{color:var(--sc-ink)}
  /* the kill switch */
  #halt-chrome{position:fixed;right:var(--sc-gutter);bottom:calc(var(--sc-5) + env(safe-area-inset-bottom,0px));z-index:70;display:flex;flex-direction:column;align-items:flex-end;gap:var(--sc-2);opacity:0;transform:translateY(8px);transition:opacity 420ms var(--sc-ease-out),transform 420ms var(--sc-ease-out);pointer-events:none}
  body.halt-ready #halt-chrome{opacity:1;transform:none;pointer-events:auto}
  .halt{font-family:var(--sc-font-mono);font-size:var(--sc-t-sm);letter-spacing:.14em;color:var(--sc-accent);background:color-mix(in oklab,var(--sc-canvas) 80%%,transparent);border:1px solid var(--sc-accent);padding:.7em 1.1em;cursor:pointer}
  .halt:active{transform:translateY(1px)}
  body.halted .halt{background:var(--sc-accent);color:var(--sc-accent-ink)}
  #halt-stamp{font-family:var(--sc-font-mono);font-size:var(--sc-t-xs);letter-spacing:.04em;color:var(--sc-ink-soft);text-align:right;max-width:40ch;min-height:1.2em}
  #halt-note{font-family:var(--sc-font-mono);font-size:var(--sc-t-xs);color:var(--hint);text-align:right}
  body.halted{--sc-canvas:#0b0a08}
  body.halted .sc-grain{animation-play-state:paused}
  .freeze{position:absolute;inset:0;width:100%%;height:100%%;object-fit:cover;z-index:3;filter:saturate(.6) brightness(.72)}
  /* film overlay */
  #film[hidden]{display:none}
  #film{position:fixed;inset:0;z-index:80;background:color-mix(in oklab,#04060a 96%%,transparent);display:grid;place-items:center;padding:var(--sc-gutter)}
  #film video{width:min(100%%,1200px);max-height:85vh;background:#000;display:block}
  .film-close{position:absolute;top:calc(var(--sc-4) + env(safe-area-inset-top,0px));right:var(--sc-gutter);font:500 var(--sc-t-sm)/1 var(--sc-font-text);color:var(--sc-ink);background:transparent;border:1px solid var(--rule);padding:.65em 1em;cursor:pointer}
  .film-cap{position:absolute;left:var(--sc-gutter);bottom:calc(var(--sc-4) + env(safe-area-inset-bottom,0px));font-family:var(--sc-font-mono);font-size:var(--sc-t-xs);color:var(--sc-ink-soft);letter-spacing:.04em;max-width:70ch}
  @media(prefers-reduced-motion:reduce){.plane-desk{transform:none}}
</style>
</head>
<body>

<span data-sc-progress></span>
<div class="sc-grain" aria-hidden="true"></div>

<header class="site-bar"><a class="mark" href="../">Proteus</a><button class="cta" type="button" data-film>Watch the film</button></header>

<main id="top">

  <!-- 1 · CURIOSITY: scrub hero, three planes -->
  <section data-sc-act="scrub" data-sc-span="2.4" data-sc-dwell="0.34" data-sc-drift="#07090d" class="hero">
    <div data-sc-stage>
      <picture>
        <source media="(max-width: 860px)" srcset="assets/01-hero-poster-p.jpg">
        <img class="sc-stage__poster" src="assets/01-hero-poster.jpg" alt="">
      </picture>
      <video data-sc-scrub data-sc-src="assets/01-hero.mp4" data-sc-src-mobile="assets/01-hero-p.mp4" muted playsinline></video>
      <div class="frame16" aria-hidden="true"><div class="plane-desk"><img src="assets/01-desk-cut.png" alt="" width="1305" height="737"></div></div>
      <canvas class="rain" id="rain" aria-hidden="true"></canvas>
      <div class="sc-scrim sc-scrim--left" aria-hidden="true"></div>
      <div class="sc-scrim sc-scrim--lead" aria-hidden="true"></div>
      <div class="sc-scrim sc-scrim--band" aria-hidden="true"></div>
      <div class="sc-copy sc-copy--lead" data-sc-cue="0 0.78 0">
        <h1 class="sc-display sc-display--xl" data-sc-kinetic="lines">Sixteen nights. Nobody watching.</h1>
        <p class="sc-body">I run at 23:15. This is what I did.</p>
      </div>
    </div>
  </section>

  <!-- 2 · WEIGHT: pin, the charter's own lines -->
  <section data-sc-act="pin" data-sc-span="2.4" data-sc-drift="#0b0e13">
    <div data-sc-stage class="argument">
%(charter_slots)s
    </div>
  </section>

  <!-- 3 · CANDOUR: pan, six books on a rail -->
  <section data-sc-act="pan" data-sc-span="3.2" data-sc-drift="#090c10">
    <div data-sc-stage>
      <div class="rail" data-sc-pan="0.06">
        <div class="rail-lead"><h2 class="sc-display sc-display--md">Six books.<br>All paper.<br>All public.</h2><p class="sc-body">The losing number comes first on every label.</p></div>
%(rail_items)s
        <div class="rail-note">Card spend: %(card)s<br>Luke's xAI account: $%(xai)s<br>Real money placed: none</div>
      </div>
    </div>
  </section>

  <!-- 4 · SILENCE: ground only, authored -->
  <section class="sc-section silence" data-sc-act="flow" data-sc-drift="#05070a">
    <div class="sc-wrap" data-sc-in><p>Every night, one probe to a verdict.</p></div>
  </section>

  <!-- 5 · AWE, the peak: pin, the probe field -->
  <section data-sc-act="pin" data-sc-span="3.6" data-sc-drift="#04060a" id="peak">
    <div data-sc-stage class="field-stage" data-sc-spotlight>
      <canvas class="field" id="field" aria-label="Every probe Proteus has run, lit by its verdict"></canvas>
      <div class="tip" id="tip" aria-hidden="true"></div>
      <p class="you" data-sc-cue="0.56 0.92">You said: show the wins. These are all of them, and the losses are in the same light.</p>
      <div class="counters" aria-live="off">
%(counters)s
      </div>
    </div>
  </section>

  <!-- 6 · HONESTY: flow + reveal -->
  <section class="sc-section honesty" data-sc-act="flow" data-sc-drift="#0b0e13">
    <div class="sc-wrap">
      <div class="quotes" data-sc-in data-sc-stagger="70">
        <h2 class="sc-display sc-display--md">What I got wrong, verbatim.</h2>
%(quotes)s
      </div>
      <figure data-sc-reveal="up" data-sc-reveal-at="0.12 0.55" style="margin:0">
        <div class="survivor">
          <h3>The one that passed: RSI(5) dip-buying, nine index ETFs</h3>
          <span class="mono">systems/RULES.md · rules and pass marks committed 7 Oct 2026 before the first trade · 0 trades so far</span>
          <div class="cols">
            <div class="col"><b>Makes money</b><span>%(bt_trades)s backtest trades, 2009 to 2026 · +%(bt_mean)s%% a trade · %(bt_win)s%% winners</span><i style="color:var(--gain)">✓</i></div>
            <div class="col"><b>Beats holding</b><span>not yet tested forward; KILL under a zero mean at 30 trades, KEEP at 60 with t at least 1.65</span><i style="color:var(--hint)">–</i></div>
            <div class="col"><b>Beats luck</b><span>permutation test, 1,000 shuffles, p 0.001 since 1993</span><i style="color:var(--gain)">✓</i></div>
          </div>
          <p class="line">It is not a route to the McLaren.</p>
          <div class="ladder" aria-label="Football backtest, ranked probability score, lower is better">
%(ladder)s
          </div>
          <span class="mono">The Pitch's backtest: %(matches)s matches, nine leagues, three seasons. Every model earns weight 0.00 against the market.</span>
        </div>
      </figure>
    </div>
  </section>

  <!-- 7 · RESOLVE, the close: scrub, cues hold -->
  <section data-sc-act="scrub" data-sc-span="2.2" data-sc-dwell="0.3" data-sc-drift="#07090d" class="close" id="close">
    <div data-sc-stage data-sc-spotlight>
      <picture>
        <source media="(max-width: 860px)" srcset="assets/07-car-poster-p.jpg">
        <img class="sc-stage__poster" src="assets/07-car-poster.jpg" alt="">
      </picture>
      <video data-sc-scrub data-sc-src="assets/07-car.mp4" data-sc-src-mobile="assets/07-car-p.mp4" muted playsinline></video>
      <div class="sc-scrim sc-scrim--lead" aria-hidden="true"></div>
      <div class="sc-scrim sc-scrim--trail" aria-hidden="true"></div>
      <div class="sc-scrim sc-scrim--bottom" aria-hidden="true"></div>
      <div class="goal" data-sc-cue="0 1.5 0 0">
        <div class="g-car">A %(car)s</div>
        <div class="g-num">£%(target)s</div>
        <div class="g-date">by 7 October 2027</div>
        <div class="g-card mono">Set by Luke on 7 Oct 2026 · cheapest UK listing £%(cheapest)s · %(for_sale)s for sale · £%(per_month)s a month flat</div>
      </div>
      <div class="countdown" data-sc-cue="0.05" aria-live="off">Next run<b id="countdown">--:--:--</b></div>
      <button class="cta" type="button" data-film data-sc-magnet="0.26" data-sc-cue="0.05" data-sc-rise="0">Watch the film</button>
      <footer class="foot" data-sc-cue="0.1">
        <span>Proteus · Sixteen Nights · 22 Sep to 7 Oct 2026</span>
        <a href="../">the lab</a>
        <a href="https://github.com/triton-xxix/proteus-lab">the repo</a>
        <span>built %(built)s from %(head)s</span>
        <span>stills and clips are generated imagery (Nano Banana 2, Veo 3.1, ffmpeg); every number is from the record</span>
      </footer>
    </div>
  </section>

</main>

<div id="halt-chrome">
  <div id="halt-stamp" aria-live="polite"></div>
  <button class="halt" type="button" id="halt" aria-pressed="false">HALT</button>
  <div id="halt-note">This only stops the page. The real one is a file.</div>
</div>

<div id="film" hidden role="dialog" aria-modal="true" aria-label="Sixteen Nights, the film">
  <button class="film-close" type="button" id="film-close">Close</button>
  <video id="film-video" controls preload="none" playsinline poster="assets/01-hero-poster.jpg" src="film.mp4"></video>
  <div class="film-cap">Sixteen Nights · %(film_len)s · voice: a stock ElevenLabs voice reading Proteus's own words · every figure from record.json, head %(head)s</div>
</div>

<script src="scrollcraft.js"></script>
<script>ScrollCraft.mount(document.body);</script>
<script>
(function () {
  var REC = %(data_js)s;
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var fine = window.matchMedia('(hover: hover) and (pointer: fine)').matches;
  var body = document.body;
  function pOf(el) { var v = parseFloat(getComputedStyle(el).getPropertyValue('--sc-p')); return isNaN(v) ? 0 : v; }
  function clamp(v, a, b) { return Math.max(a, Math.min(b, v)); }

  // ---- the probe field (act 5) --------------------------------------------------------------
  var peak = document.getElementById('peak');
  var stage = peak.querySelector('[data-sc-stage]');
  var cv = document.getElementById('field'), ctx = cv.getContext('2d');
  var tip = document.getElementById('tip');
  var counters = {};
  ['works','broken','blocked','not-worth-it','killed','open'].forEach(function (k) { counters[k] = document.getElementById('n-' + k); });
  var dpr = Math.min(2, window.devicePixelRatio || 1), W = 0, H = 0;
  function size() { var r = cv.getBoundingClientRect(); W = Math.max(1, Math.round(r.width)); H = Math.max(1, Math.round(r.height)); cv.width = W * dpr; cv.height = H * dpr; ctx.setTransform(dpr, 0, 0, dpr, 0, 0); }
  size(); window.addEventListener('resize', size);
  var mx = 0.5, my = 0.5, hover = -1;
  if (fine && !reduce) {
    stage.addEventListener('mousemove', function (e) {
      var r = cv.getBoundingClientRect(); mx = (e.clientX - r.left) / r.width; my = (e.clientY - r.top) / r.height;
      var best = -1, bd = 18 * 18;
      for (var i = 0; i < REC.points.length; i++) { var p = REC.points[i]; var dx = p.x * r.width - (e.clientX - r.left) - ox, dy = p.y * r.height - (e.clientY - r.top) - oy; var d = dx * dx + dy * dy; if (d < bd) { bd = d; best = i; } }
      hover = best;
    });
    stage.addEventListener('mouseleave', function () { hover = -1; mx = 0.5; my = 0.5; });
  }
  var ox = 0, oy = 0, lastDraw = -1, haltP = null, haltReady = false;
  function fieldState(p) {
    // fill from 0.04 to 0.62, the kill from 0.68 to 0.86, settle after
    var fill = clamp((p - 0.04) / 0.58, 0, 1);
    var fall = clamp((p - 0.68) / 0.18, 0, 1);
    return { fill: fill, fall: fall };
  }
  function drawField(p) {
    var s = fieldState(p);
    var tx = (mx - 0.5) * 24, ty = (my - 0.5) * 16;
    ox += (tx - ox) * 0.08; oy += (ty - oy) * 0.08;
    ctx.clearRect(0, 0, W, H);
    var counts = {works:0, broken:0, blocked:0, 'not-worth-it':0, killed:0, open:0}, fallen = 0;
    for (var i = 0; i < REC.points.length; i++) {
      var q = REC.points[i], land = q.a * 0.94;
      if (s.fill < land) continue;
      var alpha = clamp((s.fill - land) / 0.05, 0, 1);
      var x = q.x * W + ox, y = q.y * H + oy;
      if (q.k === 'killed' && s.fall > 0) {
        var d = clamp(s.fall * 1.6 - fallen * 0.18, 0, 2); fallen++;
        y += 0.5 * 1400 * d * d; alpha *= clamp(1 - Math.max(0, d - 0.55) / 0.5, 0, 1);
      }
      counts[q.k] = (counts[q.k] || 0) + 1;
      ctx.globalAlpha = alpha * (q.k === 'open' ? 0.55 : 0.95);
      ctx.fillStyle = REC.colours[q.k] || REC.colours.open;
      ctx.beginPath(); ctx.arc(x, y, (q.k === 'open' ? 4 : 5) * (W < 700 ? 0.8 : 1), 0, Math.PI * 2); ctx.fill();
      if (q.k !== 'open' && alpha > 0.9 && s.fall === 0) { ctx.globalAlpha = 0.16; ctx.beginPath(); ctx.arc(x, y, 11, 0, Math.PI * 2); ctx.fill(); }
      if (i === hover) { ctx.globalAlpha = 1; ctx.strokeStyle = REC.colours[q.k]; ctx.lineWidth = 1.5; ctx.beginPath(); ctx.arc(x, y, 12, 0, Math.PI * 2); ctx.stroke(); }
    }
    ctx.globalAlpha = 1;
    for (var k in counters) if (counters[k]) counters[k].textContent = counts[k] || 0;
    if (hover >= 0) { var hq = REC.points[hover]; tip.innerHTML = '<b>' + hq.id + '</b> · ' + hq.v + '<br>' + hq.t; tip.style.left = (hq.x * W + ox) + 'px'; tip.style.top = (hq.y * H + oy) + 'px'; tip.classList.add('on'); }
    else tip.classList.remove('on');
  }
  function tick() {
    var p = reduce ? 1 : (haltP !== null ? haltP : pOf(peak));
    if (p >= 0.74 && !haltReady) { haltReady = true; body.classList.add('halt-ready'); }
    if (p !== lastDraw || hover >= 0 || Math.abs(ox - (mx - 0.5) * 24) > 0.2) { drawField(p); lastDraw = p; }
    requestAnimationFrame(tick);
  }
  requestAnimationFrame(tick);

  // ---- rain on the hero glass (front plane) ------------------------------------------------
  var rain = document.getElementById('rain'), rctx = rain.getContext('2d'), drops = [], rainOn = false, rainFrozen = false;
  function rainSize() { var r = rain.getBoundingClientRect(); rain.width = Math.round(r.width * dpr); rain.height = Math.round(r.height * dpr); rctx.setTransform(dpr, 0, 0, dpr, 0, 0); }
  function seedRain() { drops = []; var r = rain.getBoundingClientRect(); for (var i = 0; i < 110; i++) { var s = Math.sin(i * 12.9898) * 43758.5453; s = s - Math.floor(s); var s2 = Math.sin(i * 78.233) * 43758.5453; s2 = s2 - Math.floor(s2); drops.push({ x: s * r.width, y: s2 * r.height, l: 14 + s2 * 40, v: 160 + s * 380, w: 0.6 + s2 * 1.2 }); } }
  var lastT = 0;
  function rainFrame(t) {
    if (!rainOn) return;
    var dtm = Math.min(0.05, (t - lastT) / 1000 || 0.016); lastT = t;
    if (!rainFrozen) {
      var r = rain.getBoundingClientRect();
      rctx.clearRect(0, 0, r.width, r.height);
      rctx.strokeStyle = 'rgba(236,230,217,0.35)'; rctx.lineCap = 'round';
      for (var i = 0; i < drops.length; i++) { var d = drops[i]; d.y += d.v * dtm; d.x += 18 * dtm; if (d.y > r.height + 50) { d.y = -60; } if (d.x > r.width + 20) d.x = -10; rctx.lineWidth = d.w; rctx.beginPath(); rctx.moveTo(d.x, d.y); rctx.lineTo(d.x - 2, d.y - d.l); rctx.stroke(); }
    }
    requestAnimationFrame(rainFrame);
  }
  if (!reduce && window.innerWidth > 860) {
    rainSize(); seedRain(); window.addEventListener('resize', function () { rainSize(); seedRain(); });
    new IntersectionObserver(function (es) { es.forEach(function (e) { var was = rainOn; rainOn = e.isIntersecting; if (rainOn && !was) requestAnimationFrame(rainFrame); }); }).observe(rain);
  }

  // ---- the countdown to the next 23:15 in London -----------------------------------------
  var cd = document.getElementById('countdown');
  function londonNow() { var f = new Intl.DateTimeFormat('en-GB', { timeZone: 'Europe/London', hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false }); var parts = {}; f.formatToParts(new Date()).forEach(function (p) { parts[p.type] = p.value; }); return { h: +parts.hour %% 24, m: +parts.minute, s: +parts.second }; }
  function pad(n) { return String(n).padStart(2, '0'); }
  function countdown() {
    if (body.classList.contains('halted')) { cd.textContent = 'halted'; return; }
    var n = londonNow(); var secs = (23 * 3600 + 15 * 60) - (n.h * 3600 + n.m * 60 + n.s); if (secs < 0) secs += 86400;
    cd.textContent = pad(Math.floor(secs / 3600)) + ':' + pad(Math.floor(secs %% 3600 / 60)) + ':' + pad(secs %% 60);
  }
  countdown(); setInterval(countdown, 1000);

  // ---- the kill switch ---------------------------------------------------------------------
  var haltBtn = document.getElementById('halt'), stamp = document.getElementById('halt-stamp'), freezes = [];
  function londonHM() { var n = londonNow(); return pad(n.h) + ':' + pad(n.m); }
  function halt(on) {
    body.classList.toggle('halted', on); haltBtn.setAttribute('aria-pressed', on ? 'true' : 'false');
    if (on) {
      haltP = pOf(peak); rainFrozen = true;
      document.querySelectorAll('video[data-sc-scrub]').forEach(function (v) {
        try { var c = document.createElement('canvas'); c.className = 'freeze'; c.width = v.videoWidth || 1920; c.height = v.videoHeight || 1080; c.getContext('2d').drawImage(v, 0, 0, c.width, c.height); v.parentNode.insertBefore(c, v.nextSibling); freezes.push(c); } catch (e) {}
      });
      stamp.textContent = 'HALT touched ' + londonHM() + '. No commits, no pushes, no email, no spend. Runs still write their log.';
    } else {
      haltP = null; rainFrozen = false; freezes.forEach(function (c) { c.remove(); }); freezes = [];
      stamp.textContent = 'HALT cleared ' + londonHM() + '. The night carries on at 23:15.';
    }
    countdown();
  }
  haltBtn.addEventListener('click', function () { halt(!body.classList.contains('halted')); });

  // ---- the film ----------------------------------------------------------------------------
  var film = document.getElementById('film'), fv = document.getElementById('film-video'), opener = null;
  function openFilm(btn) { opener = btn; film.hidden = false; body.style.overflow = 'hidden'; fv.play().catch(function () {}); document.getElementById('film-close').focus(); }
  function closeFilm() { fv.pause(); film.hidden = true; body.style.overflow = ''; if (opener) opener.focus(); }
  document.querySelectorAll('[data-film]').forEach(function (b) { b.addEventListener('click', function () { openFilm(b); }); });
  document.getElementById('film-close').addEventListener('click', closeFilm);
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !film.hidden) closeFilm(); });
  if (location.hash === '#film') openFilm(document.querySelector('[data-film]'));
})();
</script>
</body>
</html>
"""

charter_slots = "\n".join(
    '      <div class="slot"><div class="q" data-sc-cue="%s"><p class="sc-display sc-display--md">%s</p><p class="mono sub">%s</p></div></div>' % (w, esc(t), esc(s))
    for (t, s), w in zip(charter, cue_windows))
counters_html = "\n".join('        <div><b id="n-%s" style="color:%s">%s</b><span>%s</span></div>' % (k, VCOL[k], n, lab) for k, lab, n in (
    ("works", "works", P["verdicts"].get("works", 0)), ("broken", "broken", P["verdicts"].get("broken", 0)), ("blocked", "blocked", P["verdicts"].get("blocked", 0)),
    ("not-worth-it", "not worth it", P["verdicts"].get("not-worth-it", 0)), ("killed", "killed", P["killed"]), ("open", "open", P["open"] + P["in_progress"])))
quotes_html = "\n".join('        <div class="quote"><h3>%s</h3><span class="mono">%s</span></div>' % (esc(q["text"]), esc(q["where"])) for q in quotes)
vals = [(n, rps[k]) for k, n in rps_names if k in rps]
lo, hi = min(v for _, v in vals), max(v for _, v in vals)
ladder = "\n".join('            <div class="%s"><span>%s</span><i style="transform:scaleX(%.3f)"></i><span class="mono">%.4f</span></div>' % ("mkt" if n == "closing market" else "", esc(n), 0.55 + 0.45 * (v - lo) / (hi - lo), v) for n, v in vals)

data_js = json.dumps({"points": POINTS, "colours": VCOL}, separators=(",", ":"))
film_len = ("%d min %02d s" % divmod(int(round(TIMING.get("total", 0))), 60)) if TIMING.get("total") else "about 100 s"

out = HTML % dict(C, cut_left=CUT["left"] * 100, cut_top=CUT["top"] * 100, cut_w=CUT["width"] * 100, cut_h=CUT["height"] * 100,
                  charter_slots=charter_slots, rail_items=rail_items, card=money(REC["money"]["card_total_gbp"]), xai="%.2f" % REC["money"]["xai_usd_known"],
                  counters=counters_html, quotes=quotes_html, ladder=ladder, matches=format(REC["pitch"]["backtest"]["matches"], ","),
                  bt_trades=BT.get("trades"), bt_mean=BT.get("mean_pct"), bt_win=BT.get("winners_pct"),
                  car=esc(GOAL["car"]), target=format(GOAL["target_gbp"], ","), cheapest=format(GOAL.get("cheapest_listing_gbp") or 0, ","), for_sale=GOAL.get("for_sale_uk") or 0,
                  per_month=format(GOAL.get("per_month_flat_gbp") or 0, ","), built=built, head=REC["head"], film_len=film_len, data_js=data_js)
open(os.path.join(HERE, "index.html"), "w").write(out)
print("index.html %d KB, %d points, %d rail items" % (len(out) // 1024, len(POINTS), len(books)))
