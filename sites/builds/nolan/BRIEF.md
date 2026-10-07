# Brief: the Tenet timeline

Self-authored under explicit creative delegation. Luke, 7 October 2026, 03:00, in his words:

> "What you could do for me is a Chris Nolan Tenet timeline... a timeline of that would be cool, of
> like everything that happens in the film, all the nuances, how things work together, how things go
> forward in time and backward in time... and like how he plays on time."
> "I think it's one of his worst films, if not his worst film, but it's still a good film. And I
> think it's just not good because it was hard to understand."
> "I don't think we should rule out having pictures and stills from Tenet... it makes it more
> authentic."

The job of the page, in one line: make the film understandable by letting you scroll through it in
both directions.

## The eight topics

1. **Vibe.** Cold, exact, two-way, dossier. References from other media: a Cold War operations
   board; a palindrome; the sound of a recording played backwards.
2. **The journey.** The rule (a bullet both ways) · the entry (Kyiv, the pill, the word) · the clues
   (Mumbai, London, the freeport and a man who fights like he has read the script) · the turn
   (Tallinn, Kat shot, through the turnstile) · the reverse (the same days backwards; the masked man
   was you) · the plan (nine pieces, the square, what the future wants) · the pincer (ten minutes) ·
   the resolve (the string, Neil goes back, the Protagonist founds the thing that found him).
3. **Energy.** Low and slow at the open, rising through Kyiv, a lull in the clues, a spike at the
   freeport, the biggest build at Tallinn, an eerie calm in the reverse, near silence at the plan,
   the peak at Stalsk-12, grief and stillness at the close.
4. **Feeling curve, one line per act, the cause after the emotion.**
   1. Disorientation: a bullet fires on the red half of the screen and un-fires on the blue half, the
      title between them.
   2. Dread: armed men on the opera steps; a pill between two fingers; a word.
   3. Curiosity: three cities, three clues; a man in a mask who moves like he knows you.
   4. Vertigo: a car drives backwards into a chase; she is shot through glass; he steps through; the
      divider irises.
   5. Recognition: the same days, read upwards in the blue column; the mask was his.
   6. Stillness: the square draws itself; nine pieces; then nothing for a third of a screen.
   7. Awe (the peak): a ten-minute clock; red drops down the page, blue climbs up it; they cross;
      zero.
   8. Grief, then resolve: an amber string drawn across the divider as it travels to the edge; one
      column takes the page; it holds.
   No two adjacent acts share a feeling.
5. **One thing no site does.** Inverted content scrolls the wrong way, and the whole page can be
   re-sorted into the order things actually happened.
6. **Range.** Dense editorial-technical, dark. Not premium-minimal: the hero and the pincer are the
   loud moments and the rest is a dossier with real stills in it.
7. **Scenes, not one world.** Hard cuts between set pieces. The two columns are the continuity.
8. **Assets.** Thirty-four stills from the film (publicity frames via TMDB, credited) and four
   Creative Commons photographs of the Tallinn locations. No video, no generated media, no spend.

## The peak

As a visitor would say it: "I scrolled and a ten-minute clock ran down while the red team dropped
down the page and the blue team climbed up it, and they crossed in the middle and met at zero."
Lives in act 7. Largest span on the page by a visible margin (3.6 against a maximum of 2.0).

## The tell-someone sentence

It's the site where everything inverted scrolls the wrong way, and in the big battle the two halves
run towards each other until the clock hits zero.

## Authored silence

The last third of act 6 carries no copy: the Sator square alone, drawn. It is meant. The harness
may report it; read it as the quiet before the peak.

## Grammar: split stage

Two columns held in tension for the whole page, resolved by scroll. Red column forward, blue column
inverted. The divider is the chrome: it carries FORWARD and INVERTED, the folio (watch number, world
day or "day unstated"), the clock in the pincer, and the mode toggle. The close is the collapse: the
divider travels to the right edge and the forward column takes the page.

Why the other seven lost: filmic one-shot is one linear argument, and Tenet is not linear; chaptered
editorial forbids a layered hero and the film's first lesson is a picture; live surface forbids
display type and reads as a tool; continuous world is the Neptune demo's shape and needs one
unbroken flight, and Tenet is cuts; typographic poster cannot carry the pincer diagram; gallery bans
the pinned argument the pincer needs; rhythmic cutlist bans pin outright.

## Signature move: the turnstile

Three expressions of one idea, all page JS reading `--sc-p` and the page's own `data-tn-*`
attributes; the engine untouched.

1. Inverted content enters against the scroll. Steps in the blue column are stacked so the first
   experienced sits lowest and cue bottom to top, so the blue column reads upwards while the red
   column reads downwards on the same scroll.
2. In the pincer, scroll is literally world time: p = 0 to 10 minutes.
3. The mode toggle in the divider: "Watch order" and "World clock" are two prebuilt pages from the
   same data. The toggle carries you to the same event on the other page.

## Fingerprint pre-check against the Neptune demo

| Dimension | Neptune demo | Tenet |
|---|---|---|
| Grammar | Continuous world, live WebGL | Split stage |
| Nav | Route map, left hairline | The divider with labels, folio, clock, toggle |
| Hero | Live 3D planet | Split still, bullet fired on one half and un-fired on the other, layered planes |
| Act shape | 7 legs, 10.0vh | 8 acts, about 12.9vh |
| Close | Horizon arrival | The collapse to one column |
| Signature | Planet as clock | Inverted content against the scroll; the turnstile toggle |

6 of 6. The registry in this workspace is empty, so the gate is clear either way.

## Score

| # | Beat | Act and span | Device | Why |
|---|---|---|---|---|
| 1 | The rule | pin 1.3 | parallax planes over a split still, trace drawn from `--sc-p` | The first lesson is a picture, and the two halves disagree about which way scroll goes |
| 2 | The entry | flow ~1.0 | flow + in, one kinetic headline | Read, not watched |
| 3 | The clues | pin 1.8 | pin, stepped cues in both columns | Three clues land one by one; the last is the masked man |
| 4 | The turn | flow ~1.1 | reveal (down on red, up on blue), the page's one iris on the divider | A wipe is a change of state |
| 5 | The reverse | pin 2.0 | pin, blue cues bottom to top | The same days, read upwards |
| 6 | The plan | flow ~0.9 | line drawing of the Sator square from `--sc-p`, authored silence | The quiet before the peak |
| 7 | The pincer | pin 3.6 | pin + bespoke SVG diagram, two clocks | The peak |
| 8 | The resolve | flow ~1.2 | the collapse driven from page scroll, reveal left on the full-width panel, colophon inside | Resolves and holds |

Five device families (parallax, flow + in, pin, reveal, kinetic). No family twice in a row. No
scrub. No pan, spotlight, magnet or drift (the grammar's bans). No scroll cue, no section counters:
the folio shows the watch number because here sequence is the information. One kinetic headline on
the page. One peak with the largest span and a quiet act before it. The close holds.
