"""P-0543: skill-distill's extract_session.py with P-0536's two leak fixes, on five Proteus transcripts.

Loads sandbox/skill-distill/extract_session.py (fetched and read in full on 22 Nov, P-0536) as a module,
runs the original summarize/to_markdown, then a patched copy: `scheduled-task` added to INJECTED, and
tool results passed through INJECTED.sub. Counts marker lines in each output, plus any email-shaped
string and any path under ~/.claude. Writes counts only; the extracted text stays in memory.
"""
import glob, json, os, re, types
from pathlib import Path

SRC = "/Users/triton/PROTEUS/sandbox/skill-distill/extract_session.py"
PROJ = "/Users/triton/.claude/projects/-Users-triton-PROTEUS"
OUT = Path(__file__).with_name("results.json")
SELF = "c585a15d"  # tonight's own session, left out
MARK = re.compile(r"system-reminder|Contents of /Users|userEmail|SCHEDULED TASK|scheduled-task|Attribution for git|gitStatus")
EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
CLAUDE_PATH = re.compile(r"/Users/triton/\.claude/")


def load():
    m = types.ModuleType("es")
    m.__file__ = SRC
    exec(compile(open(SRC).read(), SRC, "exec"), m.__dict__)
    return m


def counts(md):
    lines = md.splitlines()
    return {"lines": len(lines),
            "marker_lines": sum(1 for l in lines if MARK.search(l)),
            "email_shapes": len(set(EMAIL.findall(md))),
            "claude_paths": sum(1 for l in lines if CLAUDE_PATH.search(l))}


orig = load()
pat = load()
pat.INJECTED = re.compile(r"<(system-reminder|environment_context|user_instructions|permissions instructions|"
                          r"collaboration_mode|skill|turn_aborted|scheduled-task)[^>]*>.*?</\1>", re.S)
_parse = pat.parse_claude


def parse_claude_patched(rows):
    for e in _parse(rows):
        if e[0] == "result":
            yield ("result", pat.INJECTED.sub("", e[1] or ""), e[2])
        else:
            yield e


pat.parse_claude = parse_claude_patched
pat.PARSERS["claude"] = parse_claude_patched

logs = sorted((p for p in glob.glob(PROJ + "/*.jsonl") if SELF not in p), key=os.path.getmtime)[-5:]
res = []
for p in logs:
    raw = open(p, encoding="utf-8", errors="replace").read()
    row = {"session": os.path.basename(p)[:8], "raw_marker_lines": sum(1 for l in raw.splitlines() if MARK.search(l))}
    s0 = orig.summarize(p, "claude")
    s1 = pat.summarize(p, "claude")
    row["task_head"] = (s1["task"] or "")[:60]
    row["original"] = counts(orig.to_markdown(s0))
    row["patched"] = counts(pat.to_markdown(s1))
    res.append(row)
tot = {k: sum(r[k]["marker_lines"] for r in res) for k in ("original", "patched")}
out = {"transcripts": res, "marker_lines_total": tot}
OUT.write_text(json.dumps(out, indent=1, ensure_ascii=False))
print(json.dumps(out, indent=1, ensure_ascii=False))
