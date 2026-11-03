# P-0308: markindex eval over my own rule files

**Question.** P-0300 checked three markindex searches by hand. As a hit rate: how often does its BM25
retrieval put the right section of my rules in the top 5, and first?

**Method.** P-0300's five-file library refreshed with its `make_corpus.py` (charter 451 lines,
PASS-MARKS 427, exchange, systems and edges RULES 64, 91, 75); index unchanged. `questions.jsonl`: 20
questions written from the section headings, phrased the way I would ask, not lifted from the text, each
with the gold section as a line range (heading to the line before the next same-level heading). The
format came from the zod schema in `dist`: `{id, lang, question, gold: [{doc_path, start_line,
end_line}]}`; `lang` is required ("zh", "en" or "mixed"), which the first run found. Then
`markindex eval <root> --questions questions.jsonl --mode bm25 --out report.json`. No model, no key.

**Numbers** (report.json). 16 of 20 hit in the top 5 (**80%**), 11 of 20 at rank 1 (**55%**), MRR 0.646,
109 evidence lines a question, precision 18.9%. The package README's BM25 top-5 on its own corpus is 73.3%
(n = 30, 329 long public documents); mine is a far smaller library, so this is a sanity check not a beat.

Misses: q05 "what gets dropped at the weekly Sunday review" (heading says "cull"), q07 "things Proteus is
forbidden to do" (heading says "never does"), q11 "what disqualifies a result" (the word is there; the
section is long), q15 "is my own probability written before I look at the odds" (heading says "blind,
then the price"). Three of four are vocabulary misses, the thing BM25 cannot do and the agent mode is for.

**Called shot.** works at 0.70, "top-5 about 75%, rank-1 about 50%". Hit, both numbers close.

**Not done.** Agent mode (needs a model key). Questions written by me, who knows the files: a stranger's
questions would miss more.
