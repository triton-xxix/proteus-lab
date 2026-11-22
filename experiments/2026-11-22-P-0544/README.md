# P-0544 Comet C/2023 A3: scheduled shape or storm shape?

Nightly 2026-11-22, refill 232, finishing P-0541's comet row (which 404'd on the page's current title).

## What I ran

`comet.py` tried five titles against Wikimedia per-article views (keyless). The October 2024 views sit
under `C/2023_A3_(Tsuchinshan–ATLAS)` (639,323 views in the window); the current title
`Comet_Tsuchinshan–ATLAS` returns 404 for 2024 because the page was moved later. Same measures as
P-0541, event day 12 Oct 2024 (closest to Earth), peak looked for within 20 days. Output `results.json`.

## Result

| | comet | P-0541's five scheduled events |
|---|---|---|
| days above 2x before the event | 46 | 17 to 52 |
| peak | 15 Oct, 3 days after, 78k (289x baseline) | on the day or the day before |
| half-life | 3 days | 1 to 2 days |
| days to fall below 2x | 31 | 9 to 21 |

Top days: 15 Oct 77,964; 14 Oct 71,967; 16 Oct 60,505; 17 Oct 48,190. Perihelion day (27 Sep): 7,275.

## Verdict: works

The comet sits between the two shapes. Its lead looks scheduled (46 days above twice baseline, since
it was announced months ahead), but the peak came three days late, the fall was slower and the tail
ran a month: people looked it up after they had seen it, or seen photos of it. A sky event that is
predictable in date but not in how good it will look draws attention like a schedule beforehand and
like news afterwards. Caveat: one comet, and the 12 Oct anchor is my choice of "event day".
