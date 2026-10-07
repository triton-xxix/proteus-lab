---
format: 1920x1080
duration: 108s
message: "Sixteen nights, every one on the record, losses first"
arc: Night → Rules → The books, losses first → Silence → The probe field → What I got wrong → The survivor → The goal → Tonight
audience: Luke first, then anyone who follows the public lab page
mode: collaborative
---

## Decisions

- **Message.** Sixteen nights, every one on the record, losses first. (A claim, not a topic.)
- **Audience and arc.** Luke, on his phone or laptop, at the end of the first sixteen nights; then
  anyone who follows the lab page. Arc: night, rules, the books with the losing numbers first, an
  authored silence, the probe field as the peak, what I got wrong, the one survivor, the goal, and
  tonight's run as the resolve.
- **Format.** 1920x1080, 30fps, about 92 seconds. Voiceover yes (ElevenLabs stock British voice, Proteus
  in the first person). Music yes (ElevenLabs bed, Nocturne register) with data marks layered on top
  (one tick per nightly run, one thud per kill, one brighter tone where the Grinder crosses back above
  £1,000). No captions burned in, so no caption keep-out; the film is embedded with its own player.
- **The spine.** The run clock: a mono timestamp top-left on every frame, amber, reading a real night
  and run time from the record. It advances through the sixteen nights as the film moves and ends on
  "Tonight, 23:15". It is the one persistent prop and the callback at the end answers frame 01.
- **Brand.** `frame.md` in this folder: canvas #07090d, ink #ece6d9, ink-soft #9a9486, amber #e0a450,
  verdict colours semantic. Archivo (display) + Geist (text) + Geist Mono (data). 0 radius, 1px rules,
  no shadows, grain 4 percent. Taken from the page BRIEF, not from memory.
- **Bans.** No em dashes on screen. No invented numbers. No fake UI. No glow or gradient text. No
  centred-everything. No static end card that fades to nothing. Two motion failures to avoid: the
  slideshow (every beat a fresh card) and the screensaver (motion that says nothing). The equity line,
  the field and the clock are the only things that move for their own sake, and each says something.
- **Held frame.** Frame 12, the three lines of what I got wrong: nothing moves while the voice reads.
- **Truthfulness.** Every figure on screen is read from `../record.json` at authoring time and the
  script is checked against it before the voice is rendered. The two Veo clips are generated imagery
  and the page says so beneath the player. Where two repo figures disagree (xAI spend), the film does
  not use the figure.
- **Seam direction.** Leftward for wipes throughout. Cuts and fades where named.
- **Numbers as of this draft (7 Oct 2026, 03:45):** 16 nightly runs, 257 commits, 91 probes with 70
  verdicts (53 works, 4 broken, 10 blocked, 3 not worth it), 4 killed; Grinder £1,000 to £617.95 low
  (30 Sep) to £1,391.78, seven stops in a row at the worst; football backtest 6,766 matches, market RPS
  0.1964 against 0.2026 to 0.2061 for the models; judgement book 57 calls, +0.0067 behind the market;
  Lichess 4 wins 3 draws, rating 3032; G1 killed 3 Oct at 2,252 trades and -£14.20; systems book 970
  backtest trades, +0.64% a trade, 75% winners, luck test p 0.001; card spend £0.00; McLaren 720S,
  about £140,000, cheapest UK listing £134,100, by 7 Oct 2027.

## Locked

Luke approved the v1 sheet in session on 7 Oct 2026 (about 04:10): all fifteen film frames and the
seven page acts as drawn, voice Edward (ElevenLabs, British, professional, id goT3UYdM9bhm0n2lmKQx),
clips by Veo 3.1 via the Gemini key. Composition is settled: the build dresses these layouts and never
redraws them.

## Changes from v1

- Luke approved v1 as drawn (7 Oct, about 04:10). No frame was redrawn.
- The build stretched frames to the voice: Edward reads at about 120 words a minute, so each frame
  is the longer of its storyboard length and its line plus a breath. Four lines were trimmed (04, 07,
  08, 12). Final length 107.6s, not 92s.
- The hero clip (frame 02 and the page's act 1) is an ffmpeg push-in on the generated clean plate,
  not Veo: the Gemini prepaid balance ran out after the car clip (HTTP 402, 7 Oct 04:12). The car
  clip (frame 14 and the page's act 7) is Veo 3.1 fast.
- The music bed was regenerated at 110s and trimmed to the film with a fade, because the first 95s
  bed would have stopped inside frame 14.
- The project's HyperFrames pin moved 0.7.109 to 0.8.139: the old runtime read a video whose local
  window overlapped its host's root-time position as root time and cut the hero clip at 6.1s.

## Timing as built

| Frame | Start | Length | Voice |
|---|---|---|---|
| 01 clock | 0.00s | 4.00s | 2.5s |
| 02 room | 3.20s | 6.13s | 4.2s |
| 03 rule-one | 8.73s | 6.67s | 5.0s |
| 04 rule-two | 14.90s | 5.00s | 3.2s |
| 05 grinder-falls | 19.90s | 9.04s | 7.9s |
| 06 grinder-climbs | 28.94s | 8.90s | 7.8s |
| 07 pitch | 37.34s | 8.10s | 6.5s |
| 08 books | 45.44s | 7.65s | 6.5s |
| 09 silence | 52.49s | 2.20s | none |
| 10 field | 54.69s | 10.00s | 8.7s |
| 11 fall | 64.69s | 4.00s | 1.2s |
| 12 wrong | 68.69s | 15.45s | 14.3s |
| 13 survivor | 83.64s | 7.40s | 5.8s |
| 14 goal | 90.34s | 12.06s | 10.3s |
| 15 tonight | 101.61s | 6.00s | none |

## Frame 01 — Clock

- scene: Black. A mono clock top-left reads 23:15:00 and ticks to 23:15:03.
- duration: 4.0s
- transition_in: cut
- status: animated
- voiceover: "Every night at quarter past eleven, I run."
- src: compositions/01-clock.html

On screen: canvas black, the run clock in amber, nothing else. Motion: digits tick once a second,
first tick at 0.2s; one soft tick sound per second (data marks). Seam out: cut. Constraint: no title
yet, no logo, no fade-in from grey. Why: the whole piece is about a thing that happens at a time
nobody is watching; the first beat is the time.

## Frame 02 — The room

- scene: The night desk clip fades up behind the clock; the title sets in, lower-left.
- duration: 6.1s
- transition_in: crossfade
- status: animated
- voiceover: "Nobody is watching. This is what I did with sixteen nights."
- src: compositions/02-room.html

On screen: the hero clip (Veo push-in: dark room, one lit screen, rain on glass, sodium light
outside), the title "Sixteen Nights" in Archivo 900 at h1 scale anchored lower-left, the clock now
reading "22 Sep 2026 · 23:23 · 33d8821" (the first pre-register commit). Motion: clip fades up over
0.8s, title rises 14px into place at 1.2s. Audio: bed enters under the voice. Seam out: crossfade to
canvas. Constraint: no text inside the clip; the title is markup. Why: establishes where and when, and
names the film.

## Frame 03 — The first rule

- scene: One charter sentence types on, with its commit beneath.
- duration: 6.7s
- transition_in: crossfade
- status: animated
- voiceover: "Every prediction and every paper trade is committed before the outcome is knowable."
- src: compositions/03-rule-one.html

On screen: "Pre-register every prediction and paper trade by git commit before the outcome is
knowable." at h2, left-anchored; beneath in mono: "CHARTER.md · signed 22 Sep 2026 · cdf6a27".
Motion: words arrive in reading order over 1.6s. Seam out: wipe left. Constraint: no typewriter
cursor. Why: the first of the two rules that make the record trustworthy.

## Frame 04 — The second rule

- scene: The second charter sentence, and the two signing dates.
- duration: 5.0s
- transition_in: wipe
- status: animated
- voiceover: "A losing record goes where a winning one would. Luke signed that on the twenty-second of September."
- src: compositions/04-rule-two.html

On screen: "A losing record is published in exactly the same place and format as a winning one." at
h2; beneath in mono: "v1 signed 22 Sep · v2 signed 29 Sep · e1ebe88". Motion: same arrival as 03,
then still. Seam out: cut. Why: the second rule, and the reason the losses come first in every frame
that follows.

## Frame 05 — The Grinder falls

- scene: The paper bankroll line draws from £1,000 down to its low.
- duration: 9.0s
- transition_in: cut
- status: animated
- voiceover: "The meme-coin desk lost first. Seven stops in a row. Six hundred and eighteen pounds left of a thousand."
- src: compositions/05-grinder-falls.html

On screen: book label top-left ("The Grinder · meme-coin paper desk · £100 a trade"); the equity line
draws left to right from 1,000, dashed baseline at the start, line turns the loss colour below it,
reaching 617.95 at 30 Sep; the current pound figure counts beside the line head. Clock reads 30 Sep
2026 · 23:48. Motion: the line draws over 5.5s with ease-out; the counter follows the head. Seam out:
continuous into 06, same composition. Constraint: no smoothing of the path; one point per closed trade
from grinder.path. Why: the loss goes where a win would, so it comes first.

## Frame 06 — The Grinder climbs

- scene: The same line continues up to £1,391.78; the counter lands.
- duration: 8.9s
- transition_in: cut
- status: animated
- voiceover: "Then it came back. Thirteen hundred and ninety-one pounds. On paper, and I say on paper every time."
- src: compositions/06-grinder-climbs.html

On screen: the line continues to 6 Oct and 1,391.78; the counter lands in Archivo stat scale; small
mono beneath: "44 closed · 19 take-profits · 24 stops · 1 rug · hit rate 43%". Audio: the brighter
tone where the line crosses back above 1,000. Clock reads 06 Oct 2026 · 23:23. Seam out: wipe left.
Why: the recovery, told with the exact shape of the path, not a summary.

## Frame 07 — The Pitch

- scene: Five horizontal bars, the market first; the models all longer.
- duration: 8.1s
- transition_in: wipe
- status: animated
- voiceover: "The football model found no edge against the closing line in six thousand seven hundred and sixty-six matches, so it has made no live call yet."
- src: compositions/07-pitch.html

On screen: book label ("The Pitch · football forecast desk · 0 live predictions"); five bars labelled
closing market 0.1964, pre-close 0.1972, shots model 0.2026, Elo 0.2047, Dixon-Coles 0.2061 (RPS,
lower is better), market in amber, models in ink-soft; mono footer "6,766 matches, nine leagues,
three seasons". Motion: bars grow left to right, staggered 120ms. Seam out: cut. Constraint: no
decimal invented beyond the report's four places. Why: the honest zero on the second desk.

## Frame 08 — The other books

- scene: Three museum labels arrive in turn: Lichess, judgement, the graduation book.
- duration: 7.7s
- transition_in: cut
- status: animated
- voiceover: "The chess bot won four and drew three. My own judgement calls sit behind the market. One book hit its kill line, and I nearly missed it."
- src: compositions/08-books.html

On screen: three book labels in a row, left to right: "Lichess bot · 7 games · 4 wins 3 draws · rating
3032"; "Judgement book · 57 calls · +0.0067 behind the market"; "Graduation book G1 · KILLED 3 Oct ·
2,252 trades · -£14.20 each". The KILLED word in the killed colour. Motion: each label rises 14px into
place on its sentence. Seam out: fade to black over 0.6s. Why: the rest of the record, same label
schema, losses stated plainly.

## Frame 09 — Silence

- scene: Near-black. One line, small: "Every night, one probe to a verdict."
- duration: 2.2s
- transition_in: fade
- status: animated
- voiceover: onscreen
- src: compositions/09-silence.html

On screen: canvas at its darkest, the line in Geist body at centre-left, the clock dimmed. No voice,
bed thins to the drone. Seam out: cut. Constraint: nothing else on the frame. Why: the silence before
the peak; the field needs something to be a change from.

## Frame 10 — The field fills

- scene: Ninety-one points surface across the dark in creation order, each lit by its verdict.
- duration: 10.0s
- transition_in: cut
- status: animated
- voiceover: "Ninety-one probes in sixteen nights. Fifty-three worked. Four broke. Ten were blocked. Three were not worth it."
- src: compositions/10-field.html

On screen: the probe field (canvas) fills the frame; points appear in creation order, dim, then stamp
their verdict colour; six counters along the bottom tick up (works, broken, blocked, not worth it,
killed, open) with mono labels; the clock runs through the nights as the points land. Motion: 91
points over 8s, eased so the first nights are slow and the busy nights fast (real timestamps). Seam
out: continuous into 11. Constraint: the point count is read from the registry, never typed. Why: the
peak, drawn from the data, which is the point of Proteus.

## Frame 11 — Four fall

- scene: The four killed points detach and fall out of the frame; a small amber HALT glyph appears.
- duration: 4.0s
- transition_in: cut
- status: animated
- voiceover: "Four I killed."
- src: compositions/11-fall.html

On screen: the field holds; the four killed points drop with gravity over 1.4s and leave; the killed
counter reads 4; bottom-right a small amber mark reading HALT in mono. Audio: four low thuds on the
drops. Seam out: cut. Why: the cull is part of the score, and it introduces the kill switch the page
makes pressable.

## Frame 12 — What I got wrong (held)

- scene: Three lines set in type, still, with their sources.
- duration: 15.4s
- transition_in: cut
- status: animated
- voiceover: "I got the Germany manager wrong. My one in ten was out by a factor of four. A test built to reject will reject, so now every strategy gets three columns: makes money, beats holding, beats luck."
- src: compositions/12-wrong.html

On screen: three quote plates stacked left: "Wrong with confidence." (state/runs/2026-09-28.md);
"Last week's "one in ten" was out by a factor of four." (field-notes/2026-W40.md); "The graduation
book has already hit its kill line, and I nearly missed that." (field-notes/2026-W40.md). Motion:
none after the first 0.6s; this is the held frame. Seam out: wipe up. Constraint: verbatim text,
verified by the data script. Why: candour is the record's price of admission.

## Frame 13 — The survivor

- scene: One row, three columns: makes money, beats holding, beats luck; one line beneath.
- duration: 7.4s
- transition_in: wipe
- status: animated
- voiceover: "One survived: buying the dip on nine index funds. It is not a route to the McLaren."
- src: compositions/13-survivor.html

On screen: heading "RSI(5) dip-buying, nine index ETFs"; three cells: "Makes money · 970 trades ·
+0.64% a trade · 75% winners" (tick), "Beats holding · not yet tested forward" (dash), "Beats luck ·
permutation p 0.001" (tick); beneath in Geist: "It is not a route to the McLaren." Clock reads 07 Oct
2026 · 9fd339e. Motion: cells arrive left to right. Seam out: fade to black. Why: the one thing that
passed the hardest bar, named plainly, with its limit in the same breath.

## Frame 14 — The goal

- scene: The car on wet tarmac under sodium light; the number and the date trail in.
- duration: 12.1s
- transition_in: fade
- status: animated
- voiceover: "A McLaren 720S. About one hundred and forty thousand pounds. By the seventh of October next year. From a card with nothing on it."
- src: compositions/14-goal.html

On screen: the car clip (Veo drift, no words in the image); trail copy bottom-left arrives on the
voice: "A McLaren 720S" (h2), "£140,000" (stat), "7 October 2027" (h3), "Card spend: £0.00" (mono).
Clock reads 07 Oct 2026 · 00:13 · 23657e3. Motion: each line rises on its word. Seam out: crossfade
to black. Constraint: cheapest listing and running costs stay off this frame (they are on the page).
Why: where this is going, said as a number and a date, not a mood.

## Frame 15 — Tonight

- scene: Black. The clock reads "Tonight, 23:15." and the lab address beneath. It holds.
- duration: 6.0s
- transition_in: crossfade
- status: animated
- voiceover: onscreen
- src: compositions/15-tonight.html

On screen: "Tonight, 23:15." at h1, the clock top-left now reading the same; beneath in mono:
"triton-xxix.github.io/proteus-lab/record". Audio: the bed resolves and stops at 4s; one last tick.
Motion: none after the arrival. Seam out: none; the frame holds to the end. Why: the callback to frame
01, and the resolve: the record continues tonight.

Total: 4 + 6 + 5 + 5 + 7 + 6 + 6 + 7 + 2 + 10 + 4 + 10 + 6 + 9 + 5 = 92s. Voice about 200 words over
about 70s of speech, near 150 words a minute with room to breathe.
