# Sixteen Nights: the brief

Self-authored under explicit creative delegation. Luke asked on 7 Oct 2026 at about 03:00 for "a
cool, amazing visual representation of everything we've done in Proteus", combining "cool web
design, image creation, audio video", and "it should be cinematic". He answered four questions
in session (voice, clips, review shape, length) and left the rest to me. Where a topic below is
his, it is quoted; where it is mine, it says so.

## The eight topics

1. **Vibe.** Luke: "cool, amazing", "cinematic". Mine: a dark London room at 23:15, one lit
   screen, rain on glass, sodium light outside. References from any medium: the opening of
   Michael Mann's Collateral (a city at night seen from inside a car), the ledger pages in a
   Victorian counting house, the Apollo mission control film reels where every number on screen
   was real.
2. **The scroll journey, in order.** Mine, built from what Proteus is: the night and the run; the
   charter that binds it; the six paper books with their honest numbers; one quiet screen; the
   probe field lighting up; what I got wrong, then the one survivor; the car, the date, and
   tonight's run.
3. **Energy curve.** Quiet open, rising through the books, an authored silence, the loudest moment
   at the probe field, a plain spoken middle, a slow resolve that holds.
4. **Feeling, stage by stage, and the one moment to remember.** The curve is below. The moment:
   eighty-four (now more) probes lighting up over you in their verdict colours, the killed ones
   falling, then a kill switch you can press that stops everything.
5. **One thing no site he has seen does.** A kill switch that is real to the subject: the page has
   a `HALT` control, like the file that stops Proteus, and pressing it freezes every clip and
   every animation on the page at once, stamps a log line, and releasing it lets the night carry on.
6. **How far from premium-minimal.** Luke: "cinematic". Mine: dark, but not premium-minimal as a
   costume; the numbers are dense where the record is dense (the rail, the probe field) and the
   type is loud where the charter speaks.
7. **One unbroken world or distinct scenes.** Distinct scenes carried as one film: filmic one-shot,
   not worldflight. There is no geography to fly through; there is a sequence of nights.
8. **Assets Luke already has.** None for this subject. No Proteus logo exists. The record itself is
   the asset: `record.json`, built by `bin/record-data.py` from the ledgers, the probe registry,
   the run logs, the hook decision logs and git history. Generated imagery via his Gemini key
   (Nano Banana 2 stills, Veo 3.1 clips); voice via his ElevenLabs key, a stock British voice,
   never his own; music via ElevenLabs; all named by him in session on 7 Oct 2026.

## Decisions Luke made in session (7 Oct 2026)

- Voice: ElevenLabs stock voice. Clips: Veo 3.1 via the Gemini key. Review: storyboard first.
  Length: about 90 seconds.

## What this is, who it is for, what they must believe, what they do next

A dated retrospective (22 Sep to 7 Oct 2026) of Proteus, the explorer persona, for Luke first and
for anyone who follows the public lab page. By the end the visitor must believe one sentence:
every one of these nights is on the record, losses first. The one action is "Watch the film",
and the label is the same in the bar and the close.

## Journey beats

```
1  Curiosity    the night and the run: a dark room, one lit screen, the wheel pushes the camera in
2  Weight       the charter's own sentences, with the commits that made them binding
3  Candour      six books, labelled like museum objects, the losing numbers first
4  Silence      "Every night, one probe to a verdict." and nothing else
5  Awe          the probe field: every probe lights up in verdict colour; the killed ones fall
6  Honesty      what I got wrong, verbatim and sourced; a wipe to the one survivor
7  Resolve      the car, the number, the date; a live countdown to 23:15; it holds
```

## Feeling curve

```
1  Curiosity   a dark room, one lit screen, rain on the window; the camera pushes in under your hand
2  Weight      the charter's own sentences, one at a time, each with the commit that made it binding
3  Candour     six books on a rail, labelled like museum objects, the losing numbers first
4  Silence     an almost empty screen: "Every night, one probe to a verdict."
5  Awe (PEAK)  the dark fills with every probe in the order I ran them, lit by verdict; four fall
6  Honesty     what I got wrong, typeset plainly; a wipe to the one survivor, in three columns
7  Resolve     the car on wet tarmac, the number, the date; a live countdown to tonight's run; it holds
```

No two adjacent acts carry the same feeling. Act 4 is quieter than act 5 by design.

## The peak

As a visitor would tell a friend: "the screen went dark, then dozens of probes lit up over me one
by one in their verdict colours, the four killed ones fell out of the sky, and then a kill switch
appeared and I pressed it and everything froze." It lives in act 5. It gets the largest span
(3.6vh), the silence of act 4 in front of it, and the pointer parallax. The two generated clips go
to acts 1 and 7; the peak is drawn from data, which is the point.

## Tell-someone sentence

It's the page where you watch sixteen nights of work light up and then hit the kill switch and the
whole film stops dead.

## Authored silence

Act 4 is a near-empty viewport on purpose: one line in and out, no media, ground #05070a. The
verification pass should read it as anticipation, not as dead scroll.

## Grammar

Filmic one-shot, with its burden of proof. Luke asked for cinematic and a retrospective is a single
linear argument with one arc. Why the other seven lost: chaptered editorial is for reading, and the
weekly Field Notes already are the reading format; live surface forbids photography and display
type, and he asked for image creation; continuous world needs a real geography and is the most
fragile build; typographic poster forbids imagery; gallery answers "what are the options", not
"what happened"; split stage needs two sides, and the charter's whole point is that wins and
losses sit in the same place; rhythmic cutlist bans dwell, and the numbers must be read.

## Signature move

The kill switch. A control styled as the real `HALT` file, first appearing at the peak's settle,
then fixed in the chrome for the rest of the page. Pressing it freezes both scrub clips and the
probe field mid-motion, drops the ground to the run-log tone, sets the countdown to "halted", and
stamps one line: "HALT touched 03:41. No commits, no pushes, no email, no spend. Runs still write
their log." Releasing stamps "HALT cleared" and everything resumes. One honest line under it: this
only stops the page; the real one is a file. Bespoke JS driven off `--sc-p`; the engine is untouched.

## Fingerprint gate

`sites/FINGERPRINTS.md` has no rows (first build in this workspace), so the gate passes. The shape
still avoids the 6 to 7 acts at 13.6 to 13.8vh band: 7 acts at about 15.8vh.

## World and tokens

Nocturne. Style preamble, reused verbatim on every image prompt:

> Night photography, practical light sources only: one desk lamp, screen glow, sodium streetlight
> through rain on glass. Wet reflective surfaces doubling every light. Deep blue-black shadows, warm
> amber point highlights, heavy atmosphere. Shot on 35mm anamorphic, visible film grain, slight
> halation. Photographic, cinematic. NOT 3D render, NOT illustration, NOT CGI, no neon, no digital
> glow, no plastic sheen, no text, no logos, no people.

Tokens: canvas #07090d, surface #0e1218, ink #ece6d9, ink-soft #9a9486, accent (sodium amber)
#e0a450, accent-ink #120d05. Verdict colours (semantic, not accent): works #7fc8a9, broken #d96b5c,
blocked #8d9bb5, not worth it #6f6a62, killed #c9473c, open #4e5868. Display: Archivo (700 to 900).
Text: Geist. Data: Geist Mono for hashes and times only.

## Score table

| Act | Device | Span | Moment | Ground |
|---|---|---|---|---|
| 1 Curiosity | `scrub` hero + layered planes | 2.4 | Veo push-in on the night desk; alpha cutout of desk and screen as the mid plane; procedural rain on glass in front; greet headline between planes: "Sixteen nights. Nobody watching." | #07090d |
| 2 Weight | `pin` | 2.4 | Four crossfading cues: the charter's own lines, each with its commit hash and time in mono beneath. | #0b0e13 |
| 3 Candour | `pan` + `count` + `tilt` | 3.2 | Rail: lead "Six books. All paper. All public.", Grinder, Pitch and judgement, Lichess, graduation books, intel lane, closing note "Card spend: £0.00." One label schema per item. | #090c10 |
| 4 Silence | ground-only `flow` | 0.8 | One line in and out. Authored silence. | #05070a |
| 5 Awe, PEAK | `pin` + Canvas 2D + `count` | 3.6 | Probe field from `record.json`; verdict colours stamp; killed points fall; six counters tick; the kill switch arrives at the settle. | #04060a |
| 6 Honesty | `flow` + `reveal` | 1.2 | The quotable lines with sources; `reveal="up"` to the systems book in three columns. | #0b0e13 |
| 7 Resolve, close | `scrub` + `spotlight`, cues hold | 2.2 | Veo drift over the car; the number, the date; countdown to 23:15; "Watch the film"; footer inside the stage. | #07090d |

Devices in order: scrub, pin, pan, flow, pin, flow+reveal, scrub. Two scrubs exactly, no device
twice in a row, six families. Nav: fixed minimal bar, wordmark "Proteus", one CTA. No section
numbers, no scroll cue, no eyebrows, no em dashes, no invented numbers.
