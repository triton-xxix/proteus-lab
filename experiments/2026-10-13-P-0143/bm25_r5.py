#!/usr/bin/env python3
"""P-0143: replicate plur-bench's BM25-only, chunk-granularity, canonical-doc R@5 on LongMemEval-S.

Mirrors plur-bench HEAD (13 Oct 2026): benchmark/chunker.ts (300-word chunks, 50 overlap, 6000-char cap),
src/plur-core/fts.ts (tokeniser with a 26-word stop list, substring term matching, BM25 k1 1.2 b 0.75,
IDF log(N/(1+df)) floored at 0, zero-score fallback to uniform weights), and benchmark/per-question.ts
(page = role-tagged turns joined by blank lines; search text = chunk + source tag; top-10 units mapped
to sessions; hit_5 = any of the first 5 units from an answer session; questions with no canonical
session skipped). Their published number: 92.2% R@5.
Usage: bm25_r5.py CORPUS.json OUT.json [--limit N]
"""
import json
import math
import re
import sys
import time
from collections import Counter

STOP = {"the", "and", "for", "that", "this", "with", "from", "are", "was", "were", "been", "have",
        "has", "not", "but", "its", "you", "your", "can", "will", "should", "would", "could", "may",
        "might"}
K1, B = 1.2, 0.75
NONWORD = re.compile(r"[^\w\s]", re.ASCII)
SENT = re.compile(r'(?<=[.!?])\s+|(?<=[.!?]["\)\]])\s+|\n{2,}')


def tokenize(text):
    return [w for w in NONWORD.sub(" ", text.lower()).split() if len(w) > 2 and w not in STOP]


def word_count(s):
    s = s.strip()
    return len(s.split()) if s else 0


def chunk_text(text, size=300, overlap=50, max_chars=6000):
    t = (text or "").strip()
    if not t:
        return []
    sents = [s.strip() for s in SENT.split(t) if s and s.strip()]
    if not sents:
        sents = [t]
    chunks, cur, cur_w = [], [], 0
    for s in sents:
        sw = word_count(s)
        if sw > size:
            if cur:
                chunks.append(" ".join(cur))
            words = s.split()
            for i in range(0, len(words), size):
                chunks.append(" ".join(words[i:i + size]))
            cur, cur_w = [], 0
            continue
        if cur_w + sw > size and cur:
            chunks.append(" ".join(cur))
            seed, w = [], 0
            for i in range(len(cur) - 1, -1, -1):
                if w >= overlap:
                    break
                seed.insert(0, cur[i])
                w += word_count(cur[i])
            cur, cur_w = list(seed), w
        cur.append(s)
        cur_w += sw
    if cur:
        chunks.append(" ".join(cur))
    out = []
    for c in chunks:
        if len(c) <= max_chars:
            out.append(c)
        else:
            for i in range(0, len(c), max_chars):
                out.append(c[i:i + max_chars])
    return out


def build_units(q):
    units, sess = [], []
    for si, session in enumerate(q["haystack_sessions"]):
        parts = []
        for t in session:
            content = (t.get("content") or "").strip()
            if not content:
                continue
            role = (t.get("role") or "").strip()
            parts.append(f"{role}: {content}" if role else content)
        page = "\n\n".join(parts)
        if not page:
            continue
        src = f"pq:{q['question_id']}:s{si + 1}"
        for u in chunk_text(page):
            units.append(u + " " + src)   # engramSearchText = statement + source
            sess.append(si + 1)
    return units, sess


def search(units, query, limit):
    qt = tokenize(query)
    if not qt:
        return []
    docs = [tokenize(u) for u in units]
    counters = [Counter(d) for d in docs]
    n = len(units)
    vocab = set()
    for c in counters:
        vocab.update(c.keys())
    # substring match sets per query token, computed once per question
    match = {}
    for q in qt:
        match[q] = {t for t in vocab if q in t or t in q}
    # df counts a doc once if it has qt as a term or any substring-related term
    idf = {}
    for q in qt:
        m = match[q]
        df = sum(1 for c in counters if any(t in c for t in m))
        idf[q] = max(0.0, math.log(n / (1 + df)))
    avgdl = sum(len(d) for d in docs) / n if n else 0

    def score(i, use_idf):
        dl = len(docs[i])
        avg = avgdl if avgdl > 0 else dl
        has_nonzero = any(v > 0 for v in idf.values())
        s = 0.0
        for q in qt:
            if not use_idf:
                w = 1.0
            elif has_nonzero:
                w = idf.get(q, 0.0)
                if w == 0:
                    continue
            else:
                w = 1.0
            c = counters[i]
            tf = sum(c[t] for t in match[q] if t in c)
            if tf == 0:
                continue
            s += w * (tf * (K1 + 1)) / (tf + K1 * (1 - B + B * dl / avg))
        return s

    scored = [(i, score(i, True)) for i in range(n)]
    scored = [x for x in scored if x[1] > 0]
    if not scored:
        scored = [(i, score(i, False)) for i in range(n)]
        scored = [x for x in scored if x[1] > 0]
    scored.sort(key=lambda x: -x[1])   # stable, like JS sort
    return [i for i, _ in scored[:limit]]


def main():
    corpus, outp = sys.argv[1], sys.argv[2]
    limit = int(sys.argv[sys.argv.index("--limit") + 1]) if "--limit" in sys.argv else None
    qs = json.load(open(corpus))
    if limit:
        qs = qs[:limit]
    t0 = time.time()
    n = h1 = h5 = h10 = 0
    skipped = 0
    per_type = {}
    rows = []
    for q in qs:
        units, sess = build_units(q)
        canonical = {i + 1 for i, sid in enumerate(q["haystack_session_ids"]) if sid in q["answer_session_ids"]}
        if not units or not canonical:
            skipped += 1
            continue
        top = search(units, q["question"], 10)
        ranked = [sess[i] for i in top]
        hit1 = bool(ranked) and ranked[0] in canonical
        hit5 = any(s in canonical for s in ranked[:5])
        hit10 = any(s in canonical for s in ranked[:10])
        n += 1
        h1 += hit1
        h5 += hit5
        h10 += hit10
        pt = per_type.setdefault(q.get("question_type", "?"), [0, 0])
        pt[0] += 1
        pt[1] += hit5
        rows.append({"question_id": q["question_id"], "type": q.get("question_type"), "units": len(units),
                     "hit_1": hit1, "hit_5": hit5, "hit_10": hit10})
    res = {"n": n, "skipped": skipped, "r_at_1": round(100 * h1 / n, 1), "r_at_5": round(100 * h5 / n, 1),
           "r_at_10": round(100 * h10 / n, 1), "published_r_at_5": 92.2, "seconds": round(time.time() - t0, 1),
           "per_type_r5": {k: [v[0], round(100 * v[1] / v[0], 1)] for k, v in per_type.items()},
           "rows": rows}
    json.dump(res, open(outp, "w"), indent=1)
    print("n %d skipped %d  R@1 %.1f  R@5 %.1f  R@10 %.1f  (published BM25 R@5 92.2)  %.0fs" % (
        n, skipped, res["r_at_1"], res["r_at_5"], res["r_at_10"], res["seconds"]))
    for k, v in res["per_type_r5"].items():
        print("  %-28s n %3d  R@5 %.1f" % (k, v[0], v[1]))


if __name__ == "__main__":
    main()
