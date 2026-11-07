# P-0362: tokens per word for Rust and Java

P-0351 found code runs about 2.51 cl100k tokens per whitespace word across Python, JS/TS and Go, so "words x 1.3"
counts about half the real tokens. This extends the table to Rust and Java with P-0351's counter, repo list
changed (6 each, chosen as popular and moderate in size, not strictly the 10 most starred), `/target/` added to
the skips. `count.py`, `results.json`, 12 codeload tarballs keyless, 0 errors.

| | median tokens/word | range | pooled |
|---|---|---|---|
| Rust (ripgrep, bat, fd, serde, axum, clap) | 2.82 | 2.31 to 3.38 | 2.68 |
| Java (gson, junit4, commons-lang, javapoet, guice, jsoup) | 2.32 | 2.29 to 2.65 | 2.35 |
| P-0351: Python / JS-TS / Go | 2.70 / 2.53 / 2.46 | | |

- P-0351's single factor of 2.51 holds within 15% on 11 of 12 repos; sharkdp/bat (3.38) falls out, as rich and
  black did for Python.
- Java is the tightest language yet (2.29 to 2.65) and the lowest: long camelCase identifiers split into few
  tokens per word. Rust runs higher and wider.
- words x 1.3 counts 0.50 of the true tokens (median); chars / 4 counts 1.07, so chars / 4 slightly over-counts
  Java (1.09 to 1.23) and is near exact for Rust (0.99 to 1.04).

Five languages now: one factor of 2.5 tokens a word is good to about 15% for all but a few outlier repos;
chars / 4 is the better rule of thumb where characters are to hand. cl100k only.
