"""P-0181: does imozuru's report.py reject an extract altered by one word? Seven variants of its demo."""
import copy
import json
import shutil
import subprocess
from pathlib import Path

REPO = Path("/Users/triton/PROTEUS/sandbox/p0181-imozuru/imozuru-main")
REPORT = REPO / "skills/imozuru/scripts/report.py"
DEMO = REPO / "examples/demo"
WORK = Path("/Users/triton/PROTEUS/sandbox/p0181-imozuru/cases")
OUT = Path("/Users/triton/PROTEUS/experiments/2026-10-19-P-0181/results.json")

base = json.loads((DEMO / "extracts.json").read_text(encoding="utf-8"))
PAPER_Q = (0, 1)  # claims[0].quotes[1], the sample paper, lines 6-8


def variant(fn):
    d = copy.deepcopy(base)
    fn(d["claims"][PAPER_Q[0]]["quotes"][PAPER_Q[1]])
    return d


def sub(old, new):
    def f(q):
        assert old in q["text"], old
        q["text"] = q["text"].replace(old, new)
    return f


def setline(n):
    def f(q):
        q["line"], q["end"] = n, n + 2
    return f


def setfile(name):
    def f(q):
        q["file"] = name
    return f


CASES = [
    ("original demo", base, 0),
    ("one word swapped: darkest -> lightest", variant(sub("darkest", "lightest")), 1),
    ("one digit swapped: 9 of 12 -> 8 of 12", variant(sub("In 9 of", "In 8 of")), 1),
    ("whitespace and line breaks changed", variant(sub(" produced fewer ", "\n   produced    fewer\n")), 0),
    ("line number off by 2 (inside tolerance)", variant(setline(8)), 0),
    ("line number off by 4 (outside tolerance)", variant(setline(10)), 1),
    ("ellipsis drops the word 'fewer', meaning flips", variant(lambda q: q.update(text="In 9 of 12 cases, placing the darkest tone first produced… visible seams at layer boundaries.")), 1),
    ("path traversal ../extracts.json", variant(setfile("../extracts.json")), 1),
]

results = []
for i, (name, data, want) in enumerate(CASES):
    d = WORK / f"case{i}"
    if d.exists():
        shutil.rmtree(d)
    shutil.copytree(DEMO / "sources", d / "sources")
    (d / "extracts.json").write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    p = subprocess.run(["python3", str(REPORT), str(d), "--check"], capture_output=True, text=True)
    row = {"case": name, "rc": p.returncode, "wanted_rc": want, "as_wanted": p.returncode == want,
           "stdout": p.stdout.strip()[:300]}
    results.append(row)
    print(f"{'OK ' if row['as_wanted'] else 'GAP'} rc={p.returncode} want={want}  {name}")

OUT.write_text(json.dumps(results, ensure_ascii=False, indent=1), encoding="utf-8")
print("as wanted", sum(r["as_wanted"] for r in results), "of", len(results))
