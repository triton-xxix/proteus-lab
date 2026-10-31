#!/usr/bin/env python3
"""P-0270: the P-0206 FActScore-style check with three tokeniser fixes, run over any set of nights.

Fixes against experiments/2026-10-23-P-0206/factcheck.py:
 1. a number that ends a sentence loses its trailing full stop (`156.` -> `156`);
 2. lowercase hyphenated compounds (call-centre, per-clip) are not facts; a hyphenated token counts only
    when it carries a capital or a digit;
 3. an item whose brief section has no body (a vault-thread stub: title, meta, note, verdict, nothing
    else) is reported under `stub` and left out of the headline rate.
Everything else is the P-0206 logic. Prints the miss list per item; writes results.json beside itself
unless --out is given. Run: python3 .../factcheck2.py 2026-10-24 [more dates] [--out PATH]
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = "/Users/triton/PROTEUS/"

NUM = re.compile(r"\b\d[\d,\.]*\s?(?:%|percent|GB|MB|KB|B\b|fps|k\b|x\b|bn|m\b|million|billion)?", re.I)
STOP = {"The", "A", "An", "It", "This", "That", "When", "Then", "Each", "Every", "Open", "Access", "There",
        "Across", "On", "In", "For", "With", "No", "Labelled", "Turns", "Structured", "Checks"}
STUB_MARK = "The vault's verdict on the parent link"


def sections(text):
    parts = re.split(r"^## (\d+)\. ", text, flags=re.M)
    out = {}
    for i in range(1, len(parts), 2):
        out[int(parts[i])] = parts[i + 1]
    return out


def is_stub(body):
    """A vault-thread section with nothing after the parent verdict paragraph."""
    if STUB_MARK not in body:
        return False
    tail = body.split(STUB_MARK, 1)[1]
    tail = re.sub(r"Link: \S+", "", tail)
    tail = re.sub(r"Write-up: `[^`]*`", "", tail)
    first = tail.split("\n", 1)
    rest = first[1] if len(first) > 1 else ""
    return len(rest.strip()) < 40


def norm(s):
    s = s.lower().replace(",", "").replace(" percent", "%").replace(" %", "%")
    return re.sub(r"\s+", " ", s).strip()


def facts(text):
    toks = set()
    for m in NUM.finditer(text):
        t = m.group(0).strip().rstrip(".")          # fix 1
        if re.fullmatch(r"\d", t) or not t:
            continue
        toks.add(t)
    for sent in re.split(r"(?<=[.;:])\s+", text):
        words = re.findall(r"[A-Za-z][\w\.\-/]*", sent)
        for i, w in enumerate(words):
            if w in STOP:
                continue
            w2 = w.strip(".-/")
            if re.search(r"[A-Z]{2,}", w) or re.search(r"[a-z][A-Z]", w):
                toks.add(w2)
            elif re.search(r"[\./]", w2):
                toks.add(w2)
            elif "-" in w2 and re.search(r"[A-Z0-9]", w2):   # fix 2
                toks.add(w2)
            elif "-" not in w2 and i > 0 and w[0].isupper():
                toks.add(w2)
    return sorted(t for t in toks if len(t) > 1)


def supported(tok, body):
    b = norm(body)
    t = norm(tok)
    if t in b:
        return True
    m = re.match(r"([\d\.]+)", t)
    if m and m.group(1) in b:
        return True
    v = t.replace("-", " ")
    if v in b or v.rstrip("s") in b:
        return True
    return False


def night(date):
    with open(f"{ROOT}state/harvest/{date}/brief.md") as fh:
        brief = fh.read()
    with open(f"{ROOT}state/agents/{date}/harvest.json") as fh:
        judged = json.load(fh)
    secs = sections(brief)
    rows = []
    tot = sup = 0
    stubs = []
    for i, item in enumerate(judged, 1):
        if not item.get("keep"):
            continue
        body = secs.get(i, "")
        text = (item.get("claim") or "") + " " + (item.get("mechanism") or "")
        fs = facts(text)
        ok = [f for f in fs if supported(f, body)]
        miss = [f for f in fs if f not in ok]
        row = {"n": i, "key": item.get("key"), "facts": len(fs), "supported": len(ok), "unsupported": miss,
               "stub": is_stub(body), "section_chars": len(body)}
        if row["stub"]:                                 # fix 3
            stubs.append(row)
            print(f"  {i:2} {str(item.get('key'))[:44]:<44} STUB  {len(ok):2}/{len(fs):2} outside-text: {', '.join(miss)[:160]}")
            continue
        tot += len(fs)
        sup += len(ok)
        rows.append(row)
        if miss:
            print(f"  {i:2} {str(item.get('key'))[:44]:<44} miss {len(miss):2}/{len(fs):2}: {', '.join(miss)[:160]}")
    return {"date": date, "judged": len(judged), "kept": len(rows) + len(stubs), "stubs": len(stubs),
            "facts": tot, "supported": sup, "support_rate": round(sup / tot, 3) if tot else None,
            "items": rows, "stub_items": stubs}


def main():
    args = sys.argv[1:]
    out_path = os.path.join(HERE, "results.json")
    runlog = "--runlog" in args
    if runlog:
        args.remove("--runlog")
    if "--out" in args:
        k = args.index("--out")
        out_path = args[k + 1]
        del args[k:k + 2]
    dates = args or ["2026-10-24", "2026-10-25", "2026-10-26", "2026-10-27", "2026-10-28", "2026-10-29", "2026-10-30"]
    out = []
    for d in dates:
        print(f"== {d}")
        try:
            r = night(d)
        except FileNotFoundError as e:
            print(f"   missing {e.filename}")
            continue
        out.append(r)
        print(f"   judged {r['judged']} kept {r['kept']} stubs {r['stubs']} facts {r['facts']} supported {r['supported']} rate {r['support_rate']}")
    tot = sum(r["facts"] for r in out)
    sup = sum(r["supported"] for r in out)
    summary = {"nights": len(out), "kept": sum(r["kept"] for r in out), "stubs": sum(r["stubs"] for r in out),
               "facts": tot, "supported": sup, "support_rate": round(sup / tot, 3) if tot else None}
    print(json.dumps(summary))
    with open(out_path, "w") as fh:
        json.dump({"summary": summary, "nights": out}, fh, indent=1)
    if runlog and out:
        # one line per night into state/runs/<date>.md: the rate and every miss, so the morning can read it
        for r in out:
            misses = [f"{row['key']}: {', '.join(row['unsupported'])}" for row in r["items"] if row["unsupported"]]
            line = (f"- Harvest factcheck {r['date']}: {r['supported']} of {r['facts']} checkable tokens found in the "
                    f"source ({r['support_rate']}), {r['stubs']} body-less vault items left out; misses: "
                    f"{'; '.join(misses) if misses else 'none'}\n")
            with open(f"{ROOT}state/runs/{r['date']}.md", "a") as fh:
                fh.write(line)
            print("run log:", line.strip()[:200])


if __name__ == "__main__":
    main()
