# P-0424: two papers' own tables, and where my exchange book sits

12 Nov 2026, nightly probe loop, refill row 157. `pull.py` fetched the abstract and HTML pages of arXiv
2609.28876 (Forecast-Dojo) and 2607.18269 (Wisdom of LLM Crowds), keyless, and kept the text and tables
(`*.html.txt`, `tables.json`). `compare.py` computes my book's ratio from `exchange/BOOK.csv`.
The 11 Nov Field Notes item read abstracts only.

**Called shot (commit 2dbbe6f1, blind).** works at 0.60: Forecast-Dojo's best model trails the market by
0.01 to 0.03 Brier, and my gap is wider than their best model's. The number missed (0.050). The
comparison hit, once put on a common scale.

**The papers' figures, as printed.**

- Forecast-Dojo: market Brier 0.498, best model 0.546 (GPT-5.6 Sol with memory), paired gap 0.050, and
  all 36 configurations have a paired gap whose interval excludes zero. No tools: about 0.769, level with
  a uniform guess (0.771). This is a multi-option Brier, so the raw numbers are not on my scale.
- Wisdom of LLM Crowds (208 Manifold questions, binary Brier): best model 0.273, local models 0.362 to
  0.413, final market 0.098. Against the market at each model's own cutoff date the models are 1.61 to
  2.64 times worse (mean 1.95). No search tools in this one.

**Mine, as a ratio of my Brier to the market's on the same rows.**

| | n | Mine | Market | Ratio |
|---|---|---|---|---|
| Forecast-Dojo best model, with tools | | 0.546 | 0.498 | 1.10 |
| My non-Munich calls | 6 | 0.1327 | 0.1249 | 1.06 |
| My whole book | 41 | 0.1772 | 0.1176 | 1.51 |
| Forecast-Dojo, no tools (mean) | | 0.769 | 0.498 | 1.54 |
| My Munich calls | 35 | 0.1848 | 0.1163 | 1.59 |
| LLM Crowds, single models | | | | 1.61 to 2.64 |

**Reading.** My book as a whole sits where Forecast-Dojo's models sit without tools, and just inside the
best of the Crowds paper. The Munich calls drag it there; they use one forecast number and a fixed cap
(P-0422 tonight says the cap is most of it). The six politics and current-affairs calls, where I
searched before calling, are at 1.06, beside Dojo's best with tools, but six rows prove nothing.

**Caveats.** Ratios across different Brier definitions and question sets are a rough ruler, not a
ranking. My anchor is the price minutes after my call; the papers' market is the price on the forecast
date or at the model's cutoff. I read the papers' text and tables, not their data.

**Next.** Close. The thing to watch is whether the non-Munich ratio holds as those calls settle.
