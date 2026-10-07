---
workflow: general-video
flow: companion
storyboard: yes
message: "Sixteen nights, every one on the record, losses first"
destination: the record page at https://triton-xxix.github.io/proteus-lab/record/ (click to play) and a link in the weekly Field Notes
aspect: 1920x1080
language: en-GB
audience: Luke first, then anyone who follows the public lab page
length: 90s
angle: retrospective, first person
---

## Intent

A ninety-second film in which Proteus, the explorer persona, tells Luke what it did with its first
sixteen nights: a charter signed, six paper books, dozens of probes to a verdict, two Field Notes,
a kill switch, no real money, and a twelve-month goal set the same day the film was made. Luke's
words: "cool, amazing", "cinematic", "audio video". Proteus's voice: first person, plain English,
UK spelling, no em dashes, losses in the same light as wins. Every number is read from
`../record.json`, which `bin/record-data.py` computes from the repo; the script is checked against
it before the voice is rendered.

## Assets

- `../record.json` — every figure the film shows; rebuilt by `bin/record-data.py`.
- `../assets/01-hero.mp4` and `../assets/01-hero-poster.jpg` — Veo 3.1 push-in on the night desk (to be generated); also the page's hero clip.
- `../assets/07-car.mp4` and `../assets/07-car-poster.jpg` — Veo 3.1 drift over the car on wet tarmac (to be generated); also the page's closing clip.
- `../assets/*.png` — Nano Banana 2 stills under the shared Nocturne preamble (to be generated).
- `media/voice/*.wav` — ElevenLabs stock British voice, one file per scene (to be generated).
- `media/bed.mp3` — ElevenLabs music, 95s, Nocturne register (to be generated).
- `media/marks/*.wav` — data marks from `bin/record-marks.py`: one tick per nightly run, one thud per kill, one tone where the Grinder crosses back above £1,000.

## Customizations

- Voice: ElevenLabs stock British voice, picked by ear on one test line; never Luke's own voice id (Proteus is not Luke). Reason for not using the docs-site default voice: this is Proteus's film, not a HyperFrames docs film, and the voice is chosen for the persona.
- Count-ups on the real figures (commits, probes, bankroll) and a drawn equity line from the Grinder ledger.
- The probe-field canvas module is shared with the page so page and film are visibly one piece.
- Data marks layered on the music bed (see Assets).
- Veo clips as scene grounds for the open and the goal; everything else is drawn.

## Notes

- Palette and type from the page BRIEF.md: canvas #07090d, ink #ece6d9, accent #e0a450, verdict colours semantic; Archivo display, Geist text, Geist Mono for hashes and times only.
- Bans: no em dashes on screen, no invented numbers, no section numbers, no fake UI, no neon or glow, no static end card that just fades out (the end holds on "Tonight, 23:15." and the lab address).
- Held frame: the "what I got wrong" lines sit still while the voice reads them.
- Spend lands on Luke's accounts, named in session on 7 Oct 2026; logged in SPEND.md and media-ledger.jsonl.
