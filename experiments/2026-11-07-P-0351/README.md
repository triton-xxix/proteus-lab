# P-0351: words times 1.3 for code, by language (7 Nov 2026)

Refill row 110, from P-0342, which found NeuroCode's "tokens = words x 1.3" undercounts a Flask slice by
about two. Question: across 18 popular repos (6 Python, 6 JS/TS, 6 Go), what is cl100k tokens per whitespace
word, does it differ by language, and does one factor hold within 15% for every repo?

Shot: works at 0.75, about 2.6 overall (Python 2.5, JS 2.8, Go 2.6), one factor within 15% of every repo.

## Method

`count.py`: one codeload tarball per repo (keyless, default branch, 7 Nov), every source file of the repo's
language, skipping vendored, built, minified, `.d.ts` and files over 512 KB. tiktoken cl100k_base from
`sandbox/neurocode-deps` under the 3.12 venv. 0 fetch errors, 3,343 files.

## Numbers (`results.json`)

| | shot | measured |
|---|---|---|
| tokens per word, median of 18 repos | 2.6 | **2.51** |
| Python median (range) | 2.5 | 2.70 (2.34 to 3.49) |
| JS/TS median (range) | 2.8 | 2.53 (2.36 to 2.80) |
| Go median (range) | 2.6 | 2.46 (2.25 to 2.60) |
| repos within 15% of one factor 2.51 | 18 of 18 | **16 of 18** |
| words x 1.3 as a share of the true count, median | | 0.52 |
| chars / 4 as a share of the true count, median (range) | | 0.96 (0.81 to 1.33) |

The two outside 15% are both Python: rich (3.49) and black (3.03). Go is the tightest; Python the widest,
because Python repos carry very different code (black's test data is odd source by design, rich has
box-drawing and escape tables). Within a repo, files run from about 1.6 to 3.4 tokens a word (p10 to p90).

## What it says

Words x 1.3 counts about half of a code file's tokens in every language, 0.37 to 0.58 of the truth. The
rule of thumb is a prose rule; for code the factor is about 2.5, and that holds within 15% for 16 of 18
repos. chars / 4 is the better cheap rule (median 0.96), but its spread is no tighter than words x 2.5.
Language matters less than the repo: the language medians sit within 10% of each other.

## Not done

Only cl100k (one tokeniser; o200k or a local model's would move every number). Repos chosen by me, popular
and well kept, not a sample. Whole-file counts, not slices.
