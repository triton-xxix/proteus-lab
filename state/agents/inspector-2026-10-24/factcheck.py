#!/usr/bin/env python3
"""P-0206: FActScore-style check of the harvest child's claims against the text it judged.

FActScore (Min et al. 2023, via Lilian Weng's hallucination post): split a generation into atomic facts
and verify each against the source. Here the generation is each kept item's `claim` and `mechanism` in
state/agents/<date>/harvest.json and the source is that item's section in state/harvest/<date>/brief.md.
Atomic facts are approximated as checkable tokens: numbers with their units, and proper names (capitalised
words not at a sentence start, acronyms, CamelCase, dotted or slashed identifiers). A token is supported
when it appears in the item's brief section, case-insensitively, with simple number normalisation.
The script lists what it could not find so a reader can judge paraphrase against invention.
Run: python3 /Users/triton/PROTEUS/experiments/2026-10-23-P-0206/factcheck.py [date]
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATE = sys.argv[1] if len(sys.argv) > 1 else "2026-10-23"
ROOT = "/Users/triton/PROTEUS/"
BRIEF = f"{ROOT}state/harvest/{DATE}/brief.md"
JUDGE = f"{ROOT}state/agents/{DATE}/harvest.json"

NUM = re.compile(r"\b\d[\d,\.]*\s?(?:%|percent|GB|MB|KB|B\b|fps|k\b|x\b|bn|m\b|million|billion)?", re.I)
STOP = {"The", "A", "An", "It", "This", "That", "When", "Then", "Each", "Every", "Open", "Access", "There",
        "Across", "On", "In", "For", "With", "No", "Labelled", "Turns", "Structured", "Checks"}


def sections(text):
    parts = re.split(r"^## (\d+)\. ", text, flags=re.M)
    out = {}
    for i in range(1, len(parts), 2):
        out[int(parts[i])] = parts[i + 1]
    return out


def norm(s):
    s = s.lower().replace(",", "").replace(" percent", "%").replace(" %", "%")
    return re.sub(r"\s+", " ", s).strip()


def facts(text):
    toks = set()
    for m in NUM.finditer(text):
        t = m.group(0).strip()
        if re.fullmatch(r"\d", t):      # single digits are not facts
            continue
        toks.add(t)
    # names: capitalised words not at sentence start, acronyms, CamelCase, identifiers with . / -
    for sent in re.split(r"(?<=[.;:])\s+", text):
        words = re.findall(r"[A-Za-z][\w\.\-/]*", sent)
        for i, w in enumerate(words):
            if w in STOP:
                continue
            if re.search(r"[A-Z]{2,}", w) or re.search(r"[a-z][A-Z]", w) or re.search(r"[\./-]", w):
                toks.add(w.strip(".-/"))
            elif i > 0 and w[0].isupper():
                toks.add(w.strip(".-/"))
    return sorted(t for t in toks if len(t) > 1)


def supported(tok, body):
    b = norm(body)
    t = norm(tok)
    if t in b:
        return True
    # a number: accept without unit, or as digits alone
    m = re.match(r"([\d\.]+)", t)
    if m and m.group(1) in b:
        return True
    # a name: accept the stem (drop trailing s) or hyphen/space variants
    v = t.replace("-", " ")
    if v in b or v.rstrip("s") in b:
        return True
    return False


def main():
    with open(BRIEF) as fh:
        brief = fh.read()
    with open(JUDGE) as fh:
        judged = json.load(fh)
    secs = sections(brief)
    rows = []
    tot = sup = 0
    for i, item in enumerate(judged, 1):
        if not item.get("keep"):
            continue
        body = secs.get(i, "")
        text = (item.get("claim") or "") + " " + (item.get("mechanism") or "")
        fs = facts(text)
        ok = [f for f in fs if supported(f, body)]
        miss = [f for f in fs if f not in ok]
        tot += len(fs)
        sup += len(ok)
        rows.append({"n": i, "key": item["key"], "facts": len(fs), "supported": len(ok), "unsupported": miss,
                     "claim": item.get("claim"), "section_chars": len(body)})
        print(f"{i:2} {item['key'][:48]:<48} facts {len(fs):2} supported {len(ok):2}  missing: {', '.join(miss)[:160]}")
    summary = {"date": DATE, "items": len(rows), "facts": tot, "supported": sup,
               "support_rate": round(sup / tot, 3) if tot else None}
    print(json.dumps(summary))
    with open(os.path.join(HERE, "results.json"), "w") as fh:
        json.dump({"summary": summary, "items": rows}, fh, indent=1)


if __name__ == "__main__":
    main()
