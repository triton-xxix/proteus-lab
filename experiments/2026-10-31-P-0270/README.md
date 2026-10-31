# P-0270: the fact check's tokeniser fixed, rerun on the week, wired into the nightly

P-0207 leg three, Trials slot, 31 Oct 2026. P-0207 found the raw support rate (71.3 percent over 24 to
30 Oct) was set by tokeniser noise and by vault-thread items that have no body to match against. This leg
fixes the tokeniser, reruns the same seven nights and wires the check into the nightly after harvest ingest.

## Called shot

works at 0.75: after the three fixes the raw rate on items with a body rises from 71.3 to about 86
percent, body-less vault stubs reported separately. Commit c83cca9.

## What changed (`factcheck2.py` against P-0206 `factcheck.py`)

1. A number that ends a sentence loses its full stop (`156.` never matched `156`).
2. A hyphenated token counts only with a capital or a digit in it (call-centre, per-clip were "facts").
   Checking this exposed the real noise source: the old identifier rule `[\./-]` fired on the trailing
   full stop of every sentence-final word, so `tokens.`, `sentence.`, `slower.` were all "facts" and all
   missed. Stripping the stop before the test removes them.
3. A section with nothing after the parent verdict paragraph is a stub; its item is printed as `STUB`
   with its outside-text tokens and left out of the headline rate.
4. `--runlog` appends one line per night to `state/runs/<date>.md` with the rate and every miss.

## Numbers, same seven nights

| | P-0206 tokeniser | fixed |
|---|---|---|
| kept items | 52 | 52 (21 stubs, 31 with a body) |
| checkable tokens on body items | 558 (all items) | 178 |
| supported | 398 (71.3%) | 167 (93.8%) |
| misses to read | 160 | 11 |

The 11 misses: DVSA (28 Oct MOT, the attribution error P-0207 found), OSM and OpenStreetMap-style (25 Oct
Flock map, the other one), OpenTelemetry (source says OTEL), GPU, RAM, README, Plain-text, RPC, LLM, LLMs.
Both attribution errors sit in the 11; nine are expansions or generic nouns. Stub items show their
outside-text names (Real-ESRGAN, Lightricks, CUDA, Gradio and so on) under a separate label.

Shot against measured: 93.8 against about 86 called. Right direction, wrong size: I had not seen that the
dot rule was the main leak. The stub split held (21 of 52 items).

## Wiring

`tasks/nightly.md` step 5b gained a 3b line running `factcheck2.py YYYY-MM-DD --runlog` after ingest. The
flag was tested on the 30 Oct night; it appended one line to `state/runs/2026-10-30.md`. No commit from
the script; the nightly's own commits carry the log.

## Not done

Nine of the 11 misses are still noise a reader has to skip; an alias list (OTEL for OpenTelemetry) and a
stoplist of generic nouns (GPU, RAM, API, README) would cut it to the two real errors but would also hide a
future wrong GPU claim, so left alone. The check still cannot see a true name joined to a wrong claim;
that needs a reasoning step per fact (SAFE), which is a different probe. Not run on tonight's harvest yet.
