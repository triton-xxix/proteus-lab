# P-0371: does o200k move the 2.5 tokens-a-word factor for code?

P-0351 and P-0362 measured cl100k only. This counts cl100k_base (100,277 tokens) and o200k_base (200,019 tokens) side by side on the same 30 repos, HEAD tonight, with the same file filters. Script `count.py`, numbers `results.json`.

## Result

Doubling the vocabulary barely moves code. Median o200k over cl100k is 1.0041 (0.985 to 1.044), so o200k is if anything slightly longer. Tokens per whitespace word: 2.544 on cl100k, 2.545 on o200k. The 2.51 factor holds within 15% on 27 of 30 under either encoding.

| Language | cl100k per word | o200k per word | o200k over cl100k, pooled |
|---|---|---|---|
| Python | 2.702 | 2.713 | 0.9998 |
| JS/TS | 2.534 | 2.559 | 1.0157 |
| Go | 2.459 | 2.458 | 0.9995 |
| Rust | 2.816 | 2.826 | 1.0036 |
| Java | 2.317 | 2.399 | 1.0289 |

Java moves most, gson at +4.4%, every Java repo over +1.5%. rich is the only repo that shrinks by more than 1%.

## Called shot

Said works at 0.75, ratio about 0.97 and factor about 2.45. Verdict right, number wrong, and wrong in direction: I assumed a bigger vocabulary means fewer tokens.

## Not done

Both are OpenAI encodings. Neither tells you what Claude counts, and that was not measured. Repos are HEAD, so the cl100k column is re-measured here rather than taken from the earlier probes.
