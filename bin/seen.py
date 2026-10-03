#!/usr/bin/env python3
"""Have I done this before? `seen.py check "<the item's own title and subject>"`

Written 3 Oct 2026 after the fuel-feed check ran twice (25 Sep and 2 Oct): the nightly searched
SEEN.md with words I chose ("car", "lease", "MOT") and missed "fuel". This takes the candidate's own
words, so the search terms are not mine to forget.

Searches SEEN.md, PROBES.md, every Field Notes draft, HARVEST.md and the experiment folder names.
Prints the closest lines and one verdict:
  REPEAT    a line shares at least 3 meaningful words, or at least 60 percent of them
  NEAR      a line shares 2
  CLEAR     nothing closer
Exit status 1 on REPEAT, so a script can stop on it. Read-only.
"""
import re
import sys
from pathlib import Path

ROOT = Path("/Users/triton/PROTEUS")
STOP = set("""a an and are as at be by for from has have how i in into is it its of on or that the
this to was what when which who why will with does do can not no new one two my our your their its
than then there these those via per about over under just more most very also all any each""".split())


def words(text):
    out = set()
    for w in re.findall(r"[a-z0-9][a-z0-9.\-]*[a-z0-9]|[a-z0-9]", text.lower()):
        w = w.strip(".-")
        if len(w) < 3 or w in STOP:
            continue
        out.add(w[:-1] if w.endswith("s") and len(w) > 4 else w)
    return out


def corpus():
    files = [ROOT / "field-notes/SEEN.md", ROOT / "PROBES.md", ROOT / "field-notes/HARVEST.md"]
    files += sorted((ROOT / "field-notes/drafts").glob("*.md"))
    for f in files:
        if f.exists():
            for i, line in enumerate(f.read_text().splitlines(), 1):
                yield f"{f.relative_to(ROOT)}:{i}", line
    for d in sorted((ROOT / "experiments").iterdir()):
        if d.is_dir():
            yield f"experiments/{d.name}", d.name.replace("-", " ")


def check(text, show=8):
    """Returns (verdict, report lines). verdict is REPEAT, NEAR or CLEAR."""
    q = words(text)
    if not q:
        return "CLEAR", ["CLEAR: no meaningful words in the query"]
    lines = [(where, line, words(line)) for where, line in corpus()]
    # A word is distinctive if it sits on at most 1.5 percent of register lines (floor 5): "fuel" and
    # "cma" are, "market" and "paper" are not. Only distinctive words decide the verdict.
    df = {w: sum(w in ws for _, _, ws in lines) for w in q}
    cut = max(5, int(0.015 * len(lines)))
    rare = {w for w in q if 0 < df[w] <= cut}
    hits = []
    for where, line, ws in lines:
        shared = q & ws
        if shared & rare:
            hits.append((len(shared & rare), len(shared), where, line.strip()[:160], sorted(shared & rare), sorted(shared - rare)))
    hits.sort(key=lambda h: (-h[0], -h[1]))
    out = [f"distinctive words in the query: {sorted(rare) or 'none'}; never seen: {sorted(w for w in q if df[w] == 0) or 'none'}"]
    for r, n, where, line, sr, sc in hits[:show]:
        out.append(f"{r} distinctive {sr} + common {sc}  {where}\n    {line}")
    top = hits[0][0] if hits else 0
    if top >= 2:
        out.append(f"REPEAT: a line shares {top} distinctive words. Read it before running this again.")
        return "REPEAT", out
    out.append("NEAR: a line shares one distinctive word; read it." if top == 1 else "CLEAR")
    return ("NEAR" if top == 1 else "CLEAR"), out


def main():
    if len(sys.argv) < 3 or sys.argv[1] != "check":
        print(__doc__)
        sys.exit(2)
    verdict, out = check(" ".join(sys.argv[2:]))
    print("\n".join(out))
    sys.exit(1 if verdict == "REPEAT" else 0)


if __name__ == "__main__":
    main()
