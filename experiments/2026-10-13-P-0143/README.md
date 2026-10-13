# P-0143: does plur-bench's BM25-only path reproduce 92.2% R@5 on LongMemEval-S?

Yes, to the decimal: **92.2% R@5 on 500 questions** (R@1 80.4, R@10 95.4), 64 s on this Mac, from a
clean-room Python port of their BM25, chunker and scoring, on the corpus whose sha256 matches their pin.

Called shot: blocked at 0.45 (dataset or model download inside 30 min). Missed: the corpus is 278 MB and
came down in about a minute, and BM25 needs no model.

## Method

- Harness fetched as a tarball (no git clone): plur-ai/plur-bench HEAD, 13 Oct 2026.
- Corpus: `xiaowu0162/longmemeval`, file `longmemeval_s` (no extension on the Hub), 278,025,796 bytes,
  sha256 `08d8dad4…7894`, equal to the pin in their `config/datasets.yaml`. Deprecated on the Hub in
  favour of `longmemeval-cleaned`; they pin the old file deliberately.
- `bm25_r5.py` mirrors: `benchmark/chunker.ts` (role-tagged page per session, 300-word chunks, 50-word
  overlap, 6,000-char cap); `src/plur-core/fts.ts` (lower-case, non-word to space, drop tokens of two
  characters or fewer and a 26-word stop list, **substring** term matching for both df and tf, BM25
  k1 1.2 b 0.75, IDF log(N/(1+df)) floored at 0, uniform-weight fallback when every score is 0);
  `benchmark/per-question.ts` (search text is the chunk plus its `pq:<qid>:s<n>` source tag, top 10
  units mapped to sessions, hit_5 if any of the first 5 units comes from an answer session, questions
  with no canonical session skipped: none were).
- Their harness itself was not run: it needs pnpm, Node 22 and tsx, none on the unattended safe list.
  This is a port, so the match is evidence the published number is what the code computes, not a run of
  their binary.

## Numbers (results.json)

| Question type | n | R@5 |
|---|---|---|
| single-session-assistant | 56 | 100.0 |
| knowledge-update | 78 | 97.4 |
| multi-session | 133 | 96.2 |
| single-session-user | 70 | 90.0 |
| temporal-reasoning | 133 | 87.2 |
| single-session-preference | 30 | 73.3 |
| all | 500 | 92.2 |

## What it says

- The claim holds. Plain lexical retrieval with a crude tokeniser gets 92.2% of LongMemEval-S
  questions an answer session into the top five chunks. The hybrid and reranker steps buy the last
  five points (their 95.6 and 97.6), which is where the model downloads and the hours of CPU go.
- The per-question protocol is why it is this easy: each question searches only its own haystack of
  about 50 sessions. A combined corpus would be a different, harder test (their README says so).
- Preference questions are the weak spot at 73%: the question rarely shares words with the session
  that states the preference.
- One bug found in passing: their `scripts/fetch-corpus.sh` expects `data/longmemeval_s.json`, a path
  that does not exist on the Hub (the file is `longmemeval_s` at the root). Anyone following the README
  gets "Entry not found" before the harness runs.

## Not done

- Their TypeScript harness not executed (toolchain off the safe list); a Python port stands in.
- Hybrid and reranker paths not run (bge-small embedding, hours of CPU).
- No LOCOMO.
