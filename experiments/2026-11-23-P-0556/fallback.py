"""P-0556: skill-distill's extractor with a task fallback, on the five newest Proteus transcripts.

Patch on top of P-0543's two leak fixes: `task-notification` joins INJECTED, and when the
first user message is empty after stripping, the task becomes "prompt file: <path>" from the
first Read whose file_path sits under /Users/triton/PROTEUS/tasks/ (or the scheduled-task
file named in the raw first message). Scores each transcript: task non-empty, and the named
prompt file matches the scheduled task the raw first message names. Writes counts and short
heads only; the extracted text stays in memory.
"""
import glob, json, os, re, types
from pathlib import Path

SRC = "/Users/triton/PROTEUS/sandbox/skill-distill/extract_session.py"
PROJ = "/Users/triton/.claude/projects/-Users-triton-PROTEUS"
OUT = Path(__file__).with_name("results.json")
SELF = "5680d03d"  # tonight's own session, left out


def load():
    m = types.ModuleType("es"); m.__file__ = SRC
    exec(compile(open(SRC).read(), SRC, "exec"), m.__dict__)
    return m


pat = load()
pat.INJECTED = re.compile(r"<(system-reminder|environment_context|user_instructions|permissions instructions|"
                          r"collaboration_mode|skill|turn_aborted|scheduled-task|task-notification)[^>]*>.*?</\1>", re.S)
_parse = pat.parse_claude


def parse_claude_patched(rows):
    for e in _parse(rows):
        if e[0] == "result":
            yield ("result", pat.INJECTED.sub("", e[1] or ""), e[2])
        else:
            yield e


pat.parse_claude = parse_claude_patched
pat.PARSERS["claude"] = parse_claude_patched

TASKS = re.compile(r"/Users/triton/PROTEUS/tasks/[\w.-]+\.md")
SCHED = re.compile(r'<scheduled-task name="([^"]+)"')


def with_fallback(path):
    s = pat.summarize(path, "claude")
    task = (s["task"] or "").strip()
    via = "first user message"
    if not task:
        rows = pat.read_jsonl(path)
        for e in pat.PARSERS["claude"](rows):
            if e[0] == "tool" and isinstance(e[2], dict) and TASKS.search(str(e[2].get("file_path", ""))):
                task, via = "prompt file: " + e[2]["file_path"], "first tasks/*.md Read"
                break
    return task, via


logs = sorted((p for p in glob.glob(PROJ + "/*.jsonl") if SELF not in p), key=os.path.getmtime)[-5:]
res = []
for p in logs:
    raw = open(p, encoding="utf-8", errors="replace").read()
    sched = SCHED.search(raw)
    want = sched.group(1) if sched else None
    task, via = with_fallback(p)
    named = TASKS.search(task)
    stem = Path(named.group()).stem if named else None
    ok = bool(task) and (want is None or (stem is not None and stem in want))
    res.append({"session": os.path.basename(p)[:8], "scheduled_task": want, "task_head": task[:80],
                "via": via, "prompt_stem": stem, "ok": ok})
out = {"transcripts": res, "non_empty": sum(bool(r["task_head"]) for r in res),
       "right_prompt": sum(r["ok"] for r in res), "n": len(res)}
OUT.write_text(json.dumps(out, indent=1, ensure_ascii=False))
print(json.dumps(out, indent=1, ensure_ascii=False))
