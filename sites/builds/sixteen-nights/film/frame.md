---
version: alpha
name: Sixteen Nights — Frame (video / frame layer)
description: >
  The frame-scale design system for the Sixteen Nights film and its companion scroll page. The unit
  is the frame (1920×1080). Atoms are sacred: a blue-black night canvas, bone ink, one sodium-amber
  accent, Archivo display at heavy weight, Geist text, Geist Mono for real data only (hashes, times,
  ids). Verdict colours are semantic and appear only on the probe field and its counters. Flat
  planes, hairline rules, film grain at 4 percent, no glow, no gradients as decoration. Motion out
  of scope here (hyperframes-animation owns it).
unit: the frame — 1920×1080 primary; the scroll page reuses the same tokens at viewport scale
principle: atoms are sacred · composition is free · numbers come from record.json

colors:
  canvas: "#07090d"
  surface: "#0e1218"
  surface-raised: "#141a22"
  ink: "#ece6d9"
  ink-soft: "#9a9486"
  ink-hint: "#5d5a54"
  rule: "#232a33"
  amber: "#e0a450"
  amber-ink: "#120d05"
  verdict-works: "#7fc8a9"
  verdict-broken: "#d96b5c"
  verdict-blocked: "#8d9bb5"
  verdict-notworth: "#6f6a62"
  verdict-killed: "#c9473c"
  verdict-open: "#4e5868"
  loss: "#c9473c"
  gain: "#7fc8a9"

typography:
  # — data ramp (Geist Mono, only for things that are really data) —
  mono-xs:  { fontFamily: "Geist Mono", cqw: 0.72, weight: 500, tracking: "0.08em", upper: true }
  mono-sm:  { fontFamily: "Geist Mono", cqw: 0.95, weight: 500, tracking: "0.04em" }
  clock:    { fontFamily: "Geist Mono", cqw: 1.4, weight: 500, tracking: "0.06em" }
  # — reading ramp (Geist) —
  caption:  { fontFamily: "Geist", cqw: 0.95, weight: 400, lineHeight: 1.5 }
  body:     { fontFamily: "Geist", cqw: 1.3, weight: 400, lineHeight: 1.55 }
  lead:     { fontFamily: "Geist", cqw: 1.8, weight: 400, lineHeight: 1.45 }
  # — display ramp (Archivo, heavy, tight) —
  label:    { fontFamily: "Archivo", cqw: 1.1, weight: 700, tracking: "0.02em" }
  h3:       { fontFamily: "Archivo", cqw: 2.4, weight: 700, lineHeight: 1.15, tracking: "-0.01em" }
  h2:       { fontFamily: "Archivo", cqw: 3.6, weight: 800, lineHeight: 1.05, tracking: "-0.02em" }
  stat:     { fontFamily: "Archivo", cqw: 6.0, weight: 800, lineHeight: 1.0, tracking: "-0.03em", tabular: true }
  h1:       { fontFamily: "Archivo", cqw: 7.5, weight: 900, lineHeight: 0.92, tracking: "-0.035em" }
  display:  { fontFamily: "Archivo", cqw: 11.0, weight: 900, lineHeight: 0.88, tracking: "-0.04em" }

spacing:
  pad-x: "6cqw"
  pad-y: "6cqw"
  gap-lg: "3cqw"
  gap-md: "1.6cqw"
  gap-sm: "0.8cqw"

components:
  register:
    night: "ground {colors.canvas}, text {colors.ink}, soft {colors.ink-soft}, accent {colors.amber}"
    description: "One register. The film never leaves the night. Grain overlay at 4 percent on every frame."
  run-clock:
    typography: "{typography.clock}"
    color: "{colors.amber}"
    placement: "top-left at pad-x / pad-y on every frame; the one persistent prop"
    description: "A real timestamp from the record (night, run time, commit hash). It advances through the sixteen nights across the film and ends on Tonight, 23:15."
  charter-line:
    typography: "{typography.h2}"
    color: "{colors.ink}"
    sub: "{typography.mono-sm} in {colors.ink-soft}: commit hash and time beneath"
    description: "One sentence per frame, left-anchored, measure under 24 words."
  book-label:
    layout: "name ({typography.label}, amber) / what it is ({typography.caption}, ink-soft) / the number ({typography.stat}, ink) / the honest line ({typography.body}, ink)"
    rule: "1px {colors.rule} above; no box, no shadow"
    description: "Museum label. The same four rows on every book, no exceptions."
  equity-line:
    stroke: "{colors.amber} 3px; falls below the start line turn {colors.loss}"
    baseline: "1px dashed {colors.ink-hint} at the £1,000 start"
    axis: "{typography.mono-xs} dates along the bottom, pounds on the right"
    description: "Drawn from grinder.path in record.json, one point per closed trade."
  probe-field:
    points: "6px discs; verdict colours; killed points fall out of the frame"
    counters: "six, {typography.stat} values with {typography.mono-xs} labels along the bottom"
    description: "Canvas 2D, shared with the page. Order of appearance is creation order from the registry."
  quote-plate:
    typography: "{typography.h3} in {colors.ink}; source in {typography.mono-xs} {colors.ink-soft}"
    description: "Three lines, still. The held frame of the film."
  three-columns:
    layout: "one row per strategy, three cells: makes money / beats holding / beats luck"
    marks: "{colors.gain} tick, {colors.loss} cross, {colors.ink-hint} dash for not tested"
    description: "Luke's lens, verbatim headings."
  end-plate:
    typography: "{typography.h1} line + {typography.mono-sm} address"
    description: "Tonight, 23:15. and the lab address. It holds; nothing fades to empty."
---

## Overview

Sixteen Nights is Proteus telling Luke what it did with its first sixteen nights, in its own voice.
The look is a dark London room at 23:15: one lit screen, rain on glass, sodium light outside. Every
number on screen comes from `../record.json`, which `bin/record-data.py` computes from the repo.

## The frame

The frame is a page of the record. Type sits left or in a bottom band, never centred by default,
with a measure under 24 words for any display line. The run clock sits top-left on every frame and
is the only persistent chrome. Media (the two Veo clips) grounds two frames only; the rest is drawn
from data on the night canvas.

## Composition rules

- One idea per frame. If a frame needs a second idea, it is two frames.
- The accent owns one role: the clock, the equity line, and the amber mark on the HALT glyph. Nothing
  else is amber.
- Verdict colours appear only on the probe field and its counters.
- Grain at 4 percent on every frame, no vignette heavier than 12 percent, no glow, no gradient text.
- Real data in mono; prose in Geist; declarations in Archivo. Never mono as a costume.
- No em dashes anywhere on screen. No invented numbers. Nothing fades to an empty frame.

## Do and do not

- Do let a number stand alone at stat scale when the voice says it.
- Do keep the losing number first in every pair.
- Do not centre everything; vary the anchor across frames.
- Do not put text in a generated image; the clips carry no words.
- Do not use any colour outside the tokens above.
