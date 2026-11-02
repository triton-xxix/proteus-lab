# P-0297: are threatened birds named in fewer languages?

**Question.** huashu-bird-sticker's `species.json` (11,064 species, P-0288) carries each bird's names by
language and its IUCN status from Wikidata. Are the birds most at risk the ones fewer languages have names for?

**Method.** `names_v_threat.py`: languages per species = keys of `names` with a value; class =
`conservation.iucn`. Per class n, median and mean; CR+EN against LC with a permutation test on the mean gap
(5,000 shuffles); Spearman of language count against LC < NT < VU < EN < CR; coverage per language; the
gap inside each breeding region with 50 or more species and at least 5 CR+EN.

**Numbers.**

| IUCN | n | median languages | mean |
|---|---|---|---|
| LC | 8,109 | 28 | 28.91 |
| NT | 881 | 28 | 28.33 |
| VU | 623 | 29 | 28.87 |
| EN | 348 | 29 | 28.43 |
| CR | 178 | 29 | 28.49 |
| no status | 884 | 27 | 23.98 |

CR+EN v LC: mean gap +0.46 languages (perm p 0.019), median gap -1 (the threatened are named in one more).
Spearman over 10,139 ranked birds: rho -0.002, p 0.85. Within regions, LC is named in more languages in 4
of 8. Coverage: en and sk name all 11,064, fr 11,055; the thinnest are be 327, mk 389, ro 414, el 516, ml 543.

**Reading.** No. Threat status does not predict how many languages name a bird; the half-language mean gap is
real at this n but too small to matter and the median runs the other way. The thin group is the 884 birds
with no IUCN status in the data (mean 24), which are likely recent splits.

**Not done.** "No status" not checked against the taxonomy's newer splits; no chart page.
