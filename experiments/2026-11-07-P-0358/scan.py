"""P-0358: do any permission allow rules in this repo's .claude files, now or in git history,
carry a secret-shaped string? Prints counts, pattern names, files and commits only. Never prints a
matched value: each hit is shown as its pattern, length and first 4 characters masked."""
import json, re, subprocess, sys, pathlib

ROOT = pathlib.Path("/Users/triton/PROTEUS")
OUT = ROOT / "experiments/2026-11-07-P-0358/results.json"

PATTERNS = {
    "anthropic_key": r"sk-ant-[A-Za-z0-9_\-]{20,}",
    "openai_key": r"sk-(?:proj-)?[A-Za-z0-9]{20,}",
    "xai_key": r"xai-[A-Za-z0-9]{20,}",
    "github_token": r"gh[pousr]_[A-Za-z0-9]{30,}",
    "github_pat": r"github_pat_[A-Za-z0-9_]{40,}",
    "aws_key": r"AKIA[0-9A-Z]{16}",
    "slack_token": r"xox[abpr]-[A-Za-z0-9\-]{10,}",
    "google_key": r"AIza[0-9A-Za-z_\-]{35}",
    "discord_bot": r"[MN][A-Za-z\d]{23,25}\.[\w-]{6}\.[\w-]{27,}",
    "bearer": r"[Bb]earer\s+[A-Za-z0-9_\-\.]{20,}",
    "env_assign": r"(?:KEY|TOKEN|SECRET|PASSWORD|PASS)=['\"]?[A-Za-z0-9_\-\./+]{16,}",
    "op_service_token": r"ops_[A-Za-z0-9_\-]{40,}",
}
RX = {k: re.compile(v) for k, v in PATTERNS.items()}


def mask(s):
    return f"{s[:4]}…({len(s)} chars)"


def rules_from(obj):
    perms = obj.get("permissions", {}) if isinstance(obj, dict) else {}
    out = []
    for kind in ("allow", "ask", "deny"):
        for r in perms.get(kind, []) or []:
            out.append((kind, str(r)))
    return out


def scan_text(text):
    hits = []
    for name, rx in RX.items():
        for m in rx.finditer(text):
            hits.append({"pattern": name, "masked": mask(m.group(0))})
    return hits


def git(*args):
    return subprocess.run(["git", "-C", str(ROOT), *args], capture_output=True, text=True).stdout


res = {"working_tree": [], "history": [], "files_checked": [], "rules_checked": 0}

# working tree: every .claude/*.json and settings file
for p in sorted((ROOT / ".claude").glob("*.json*")):
    res["files_checked"].append(str(p.relative_to(ROOT)))
    try:
        obj = json.loads(p.read_text())
    except Exception as e:
        res["working_tree"].append({"file": p.name, "error": str(e)[:80]})
        continue
    rules = rules_from(obj)
    res["rules_checked"] += len(rules)
    for kind, r in rules:
        for h in scan_text(r):
            res["working_tree"].append({"file": p.name, "kind": kind, **h})
    # whole-file scan too (env blocks, hooks)
    for h in scan_text(p.read_text()):
        res["working_tree"].append({"file": p.name, "kind": "whole-file", **h})

# history: every committed version of tracked .claude json files
paths = sorted(set(git("log", "--all", "--name-only", "--pretty=format:", "--", ".claude").split()))
res["history_all_claude_paths"] = paths
paths = [x for x in paths if ".json" in x or x.endswith(".py")]
res["history_paths"] = paths
versions = 0
for path in paths:
    commits = git("log", "--all", "--pretty=format:%h", "--", path).split()
    for c in commits:
        blob = git("show", f"{c}:{path}")
        if not blob:
            continue
        versions += 1
        for h in scan_text(blob):
            res["history"].append({"commit": c, "file": path, **h})
res["history_versions"] = versions

# also tracked-file grep across the whole current tree, for context only (counts by pattern)
tracked = git("ls-files").split("\n")
repo_counts = {}
for f in tracked:
    fp = ROOT / f
    if not f or not fp.is_file() or fp.stat().st_size > 2_000_000:
        continue
    try:
        t = fp.read_text(errors="ignore")
    except Exception:
        continue
    for h in scan_text(t):
        repo_counts.setdefault(h["pattern"], set()).add(f)
res["tracked_tree_patterns"] = {k: sorted(v) for k, v in repo_counts.items()}
res["tracked_claude"] = [f for f in tracked if f.startswith(".claude/")]
res["history_paths_count"] = len(paths)
# masked detail for tracked-tree hits: file, line number, masked value, whether the line looks like a placeholder or example
detail = []
for pat, files in repo_counts.items():
    for f in sorted(files):
        for i, line in enumerate((ROOT / f).read_text(errors="ignore").splitlines(), 1):
            for m in RX[pat].finditer(line):
                low = line.lower()
                detail.append({"pattern": pat, "file": f, "line": i, "masked": mask(m.group(0)),
                               "context_hint": "example/placeholder" if any(w in low for w in ("example", "placeholder", "xxxx", "your_")) else ""})
res["tracked_tree_detail"] = detail
print("tracked .claude files:", res["tracked_claude"], "history paths:", res["history_all_claude_paths"])
uniq = {}
for d in detail:
    uniq.setdefault((d["file"], d["line"]), 0)
    uniq[(d["file"], d["line"])] += 1
for (f, ln), n in uniq.items():
    print("  tracked hit", f, "line", ln, "matches", n)

OUT.write_text(json.dumps(res, indent=1))
print("files", res["files_checked"], "rules", res["rules_checked"])
print("working-tree hits", len(res["working_tree"]), "history versions", versions, "history hits", len(res["history"]))
for h in res["working_tree"] + res["history"]:
    print(" ", h)
print("tracked-tree pattern files:", {k: len(v) for k, v in res["tracked_tree_patterns"].items()})
