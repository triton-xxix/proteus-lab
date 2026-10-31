# P-0207: a week of FActScore-style checks on the harvest child

P-0206 leg two, run in the Trials slot on 31 Oct 2026. The question: over seven harvest nights (24 to
30 Oct), how often does the child's `claim` plus `mechanism` carry a checkable token that is not in the
brief section it judged, and of those misses, how many are fabricated against misattributed?

## Called shot

works at 0.70: raw token support about 78 percent over the seven nights, fabricated facts 0,
misattributed facts 2 on reading the miss lists. Commit 30fd5ba.

## Method

`week.py` imports the P-0206 `factcheck.py` functions unchanged and runs them per night, printing every
miss. `show.py` prints a claim beside its source section; `find.py` searches a brief for a phrase. I read
the miss lists for all seven nights and the full claim and section for 14 of the 52 kept items, the ones
whose misses were names or numbers rather than common words.

## Numbers

| night | judged | kept | tokens | supported | rate |
|---|---|---|---|---|---|
| 24 Oct | 14 | 8 | 91 | 65 | 71.4% |
| 25 Oct | 14 | 8 | 81 | 52 | 64.2% |
| 26 Oct | 12 | 7 | 84 | 69 | 82.1% |
| 27 Oct | 9 | 5 | 49 | 28 | 57.1% |
| 28 Oct | 12 | 8 | 80 | 60 | 75.0% |
| 29 Oct | 14 | 7 | 83 | 56 | 67.5% |
| 30 Oct | 14 | 9 | 90 | 68 | 75.6% |
| week | 89 | 52 | 558 | 398 | 71.3% |

Reading the 160 misses:

- **Tokeniser noise**, most of them: sentence-start common words (people, days, slower, trade), lowercase
  hyphenated paraphrase (call-centre, per-clip, zero-dependency), and numbers that end a sentence, which
  the regex keeps with the full stop (`156.`, `27.`, `2021.`, `2026.`) so they never match. Chinese
  sources (agent-purge, mcd-mcp-kit) miss on every English paraphrase of a Chinese term.
- **True facts from outside the section**: the vault-thread items. Their "section" is a stub (title,
  vault note, parent verdict, no body), so the child wrote the mechanism from what it already knew:
  Video2X with Real-ESRGAN, Real-CUGAN, Anime4K, RIFE and Vulkan; LTX from Lightricks; Wan2GP as a
  Gradio front end on CUDA and PyTorch; Pinokio's JSON/JS launcher scripts; RunPod and Vast.ai. Every one
  I checked is true of the tool. Roughly 35 of the 160 misses are this kind, and they fall on 24, 25 and
  29 Oct, the three lowest-rate nights bar one.
- **Misattributed, 2**: (a) 28 Oct MOT video: the child says the failure shares "come from the DVSA's
  published MOT testing statistics rather than the presenter". The transcript never names the DVSA; the
  numbers (one in three, lighting near 20 percent, suspension near 20 percent, brakes around 10 percent)
  are all in the transcript and all presenter-stated. The attribution is the child's guess dressed as a
  fact. (b) 25 Oct Flock camera map: the child says the map is built "largely in OpenStreetMap-style
  data". The source's only OSM mention is a commenter asking whether the data could legally be loaded
  into OpenStreetMap. A question became a description.
- **Fabricated, 0**: no name or number in the 14 read items is invented.

Shot against measured: raw rate 71.3 percent against 78 called (miss, the vault stubs pull it down);
fabricated 0 against 0 (hit); misattributed 2 against 2 (hit, and the same failure mode P-0206 found
on 23 Oct: true pieces joined to the wrong noun).

## Reading

The token check's number is dominated by the source shape, not the child. Vault threads with no body
score 40 to 60 percent because there is nothing to match against; items with a real body score 80 to 100
percent and their misses are paraphrase. So the raw rate is a poor weekly metric. The miss list is the
product: two minutes a night finds the attribution errors, which the number cannot.

Two cheap fixes to the tokeniser would raise the raw rate without changing a judgement: strip a trailing
full stop from numbers, and drop lowercase hyphenated compounds. A better fix for the metric is to skip
items whose section has no body and report them separately.

## Not done

Only 14 of 52 items read in full; the other 38 had misses that were all common words, which I judged
from the miss list alone. No second reader. The DVSA claim may well be true of the world (the DVSA does
publish MOT failure categories) but it is not in the text, and the child presented it as the video's
source. I did not check whether the five fixes above are already in the Smith's queue.
