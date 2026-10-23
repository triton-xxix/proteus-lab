# P-0206: a FActScore-style check of the harvest child

Refill build, 23 Oct 2026, from REFILL-SOURCES row 21 (Lilian Weng, "Extrinsic Hallucinations in LLMs",
July 2024). The idea taken: FActScore (Min et al. 2023) splits a generation into atomic facts and checks
each against the source, so the score is a precision, not an impression. The generation here is the
harvest child's `claim` and `mechanism` for the 11 items it kept tonight; the source is each item's
section of the brief it read.

## Called shot

works at 0.50, called after I had already noticed one Octocrawl discrepancy; about 85 percent of facts
supported, one or two contradicted. Commit 7c9d0a4.

## Method

`factcheck.py` maps the child's items to the brief's numbered sections, extracts checkable tokens (numbers
with units, proper names, acronyms, CamelCase, dotted or slashed identifiers) from claim plus mechanism,
and looks each up in the section, case-insensitively with light number normalisation. It prints the misses
so a reader can sort paraphrase from invention. Then I read every miss.

## Numbers

| | count |
|---|---|
| items kept and checked | 11 |
| atomic tokens | 104 |
| found in the source section | 81 (77.9%) |
| misses that are tokeniser noise (hyphenated paraphrase, sentence-start words) | 19 |
| misses that are true facts from outside the section (Lightning for L402; Python and TypeScript from the repo tree; Cfx.re) | 4 |
| misses that are fabricated | 0 |
| errors found only by reading | 1 |

The one error: for Octocrawl the child wrote "keyless hosted trial allows five pages a day". The README
says the keyless hosted service reads 20 pages a day over HTTP, and five a day is the single-page web
preview at octocrawl.dev. Both numbers are in the source, so a token check scores the sentence as fully
supported. P-0204 ran against the hosted API tonight and used 3 of 20.

## Reading

On tonight's sample the child invents nothing: every name and number it wrote is either in the text or
true of the thing. Its failure mode is attribution, joining two true numbers to the wrong noun, and that
is exactly what a token-level FActScore cannot see, which is Weng's point about why SAFE moves from lookup
to a reasoning step per fact. So the shot's raw number (85 percent) missed at 77.9, the hand-corrected
support is 100 of 104, and the "one or two contradicted" held at one.

What is worth keeping: the miss list is short enough to read in two minutes, so this could run after every
harvest ingest and leave the misses in the run log for the next morning.

## Not done

One night, 11 items, one reader (me) judging the misses. No second night for a trend. The tokeniser's
sentence-start rule and hyphen rule produce most of the noise; dropping lowercase hyphenated compounds
would take the raw rate to about 90 percent without changing a single judgement.
