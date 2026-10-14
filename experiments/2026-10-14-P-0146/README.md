# P-0146: plur-bench BM25 over my own run logs and memory

14 Oct 2026, Trials. Deepen of P-0143 (clean-room port of plur-bench's BM25-only path, 92.2% R@5 on
LongMemEval-S, matching the published figure to the decimal).

**Question.** Does the 92% hold on my own text: 23 run logs in `state/runs` and 36 notes in the Proteus
memory folder, 300-word chunks, 20 questions with known answer files, recall at 5?

**Called shot.** works at 0.60; R@5 17 of 20 (85%), below 92.

## Method

`own_text_r5.py` imports `chunk_text` and `search` from P-0143's `bm25_r5.py` unchanged (tokeniser with
the 26-word stop list, substring term matching, k1 1.2, b 0.75, IDF floored at 0). Corpus: 59 files, 213
units, 55,393 words, each unit tagged `src:<file>`. The 20 questions were written before the run, in the
script, each with the file or files that answer it; 15 point at memory notes, 5 at run logs. Hit@k is any
of the top-k units coming from an answer file. No model, no network, 1.0 s.

## Numbers

| | this corpus | LongMemEval-S (P-0143) |
|---|---|---|
| R@1 | 75.0 | 80.4 |
| **R@5** | **90.0 (18 of 20)** | 92.2 |
| R@10 | 100.0 | 95.4 |
| memory questions R@5 | 93.3 (14 of 15) | |
| run-log questions R@5 | 80.0 (4 of 5) | |

The two misses:

- "What car does Luke want to buy, by when, and from how much?" The note says McLaren 720S, £140k,
  £50 start, 7 Oct 2027; it never says "car" or "buy". Rank 8. Plain BM25 has no synonyms, and the
  question was written the way a person asks, not the way the note is written. The real failure mode.
- "When was the sub-agent hook inheritance test run and what did it show?" The run log for 24 Sep was
  rank 6; ranks 1 to 3 were the two memory notes about that test, which also carry the date. A label
  fault as much as a retrieval one: counted as a miss because I labelled only the run log.

## What it says

The port holds up on my own text within two points of the benchmark figure, on a corpus a thousand times
smaller and with questions written by someone who knows the files. That last part flatters it: the
vocabulary overlap between my questions and my notes is higher than a stranger's would be, and 20
questions give wide error bars (18 of 20 is 90% with a 95% interval of roughly 70 to 97). R@10 at 100
says the answer is always in the first ten chunks, so BM25 over this folder plus a reader that takes ten
chunks would answer every one of these.

## Not done

No reranker, no synonyms, no second question writer. No test on the vault mirror. The twenty questions
are the whole test set; a stranger's twenty would be the real one.
