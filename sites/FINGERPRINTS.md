# Fingerprints

Every site you build with **scroll-craft** gets one row here, appended after it
ships. The registry exists so your next build can prove it is a different page
rather than a re-skin of one you already made.

This file is **yours**. It starts empty on purpose: the gate is about not
repeating *yourself*, so it has nothing to say until you have built something.

The rules and the gate live in the skill's
`references/uniqueness.md`. Short version:

**A new build must differ from EVERY row below on at least 4 of the 6
dimensions.** Four against each row individually, not four on average across the
table. If a planned build fails, change the plan. Never edit a row to make room
for it.

The six dimensions are: **grammar**, **nav treatment**, **hero device**,
**act-sequence shape**, **close pattern**, **signature move**.

Dimension 6 is free, because a signature move is unique by definition. So the
gate really asks for three more out of the remaining five, and a build that
changes only grammar and world will fail it.

---

## The registry

| Build | Grammar | Nav treatment | Hero device | Act-sequence shape | Close pattern | Signature move | World | Port |
|---|---|---|---|---|---|---|---|---|
| sixteen-nights (2026-10-07) | Filmic one-shot | Fixed minimal bar: wordmark + one CTA (Watch the film); HALT control joins the chrome at the peak | scrub, three planes (clip, desk cutout, rain) | scrub, pin, pan, flow(silence), pin(peak), flow+reveal, scrub close; 7 acts, about 15.8vh | Pinned-style scrub close with holding cues: car clip, live countdown to 23:15, CTA, footer inside the stage | The kill switch: a HALT control that freezes every clip and the probe field, dims the ground, stamps a log line; releasing resumes | Nocturne (night London room, wet street; Nano Banana 2 stills, one Veo clip, one ffmpeg push-in) | docs/record on GitHub Pages |

*(From the second build onwards, this table is the constraint.)*

---

## What is taken

Add a bullet here whenever a build claims something a later build should avoid
reusing: a grammar, a nav treatment, a close pattern, a signature move, an
act-count-and-length band. The shared columns are what the next build inherits
as a constraint, so writing them down is the whole point.

- sixteen-nights took: filmic one-shot; the fixed minimal bar with one CTA; a scrub hero with layered planes; a scrub close with holding cues and a live countdown; a probe-field canvas as the peak; the kill-switch signature move. The next build should not open on a scrub hero or close on a scrub with a countdown.

---

## Appending a row

After shipping, add one line to the table and one bullet to **What is taken** if
the build claimed something new. Fill every column. Say what the build shares
with existing rows.

Rows are append-only. A build that has been superseded stays in the table,
because the space it occupies is still occupied.

---

## Worked example

The skill's author kept a registry of twelve builds across eight page grammars.
If you want to see what a filled-in table looks like, and which shapes tend to
collide, read `EXAMPLES.md` in the scroll-craft repository. Treat it as
illustration only: those rows are somebody else's builds and they do **not**
constrain yours.

| tenet (sites/builds/nolan/tenet, 7 Oct 2026) | Split stage | The divider is the chrome: FORWARD and INVERTED labels, a folio (act, watch or world number, the day or "day unstated"), the mode toggle, a Films link; a top strip on phones | Two halves of one still (a bullet hole in glass), warm on the left and cold mirrored on the right, five planes each (plate, masked-portrait cutout, drawn bullet trace, sill), the title across the pivot | 8 acts, pin 1.3 / flow / pin 1.8 / flow / pin 2.0 / flow / pin 3.6 / flow 1.2, about 12.9vh | The collapse: the divider travels to the right edge over the last act, the inverted column clips away, an amber string draws across, the forward column holds the colophon | Inverted content enters against the scroll and the whole page re-sorts into world order through the turnstile toggle | Film stills, graded red and blue, no generated media | 4521 |

- Taken by `tenet`: split stage; the divider-as-chrome with a mode toggle; the collapse close; against-the-scroll inverted content; a pinned peak where scroll is a literal clock; 8 acts at about 12.9vh.
