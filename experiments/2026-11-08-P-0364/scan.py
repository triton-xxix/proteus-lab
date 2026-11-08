"""P-0364: gitleaks' default rules, run by my own script over every blob in this repo's history.

The repo is public, so nothing written under experiments/ may carry a value. results.json holds
rule, path, line, length and entropy only. The triage file with redacted context lines goes in
sandbox/gitleaks-scan/, which is gitignored.

Mimics gitleaks: keyword prefilter, first non-empty group as the secret, entropy floor, global and
per-rule allowlists. It is not gitleaks itself: Go RE2 and Python re differ, see failed_rules.
"""
import collections, json, math, os, pathlib, re, subprocess, time, tomllib

ROOT = pathlib.Path("/Users/triton/PROTEUS")
WORK = ROOT / "sandbox/gitleaks-scan"
WORK.mkdir(parents=True, exist_ok=True)
CONF = WORK / "gitleaks.toml"
if (ROOT / "sandbox/gitleaks.toml").exists():
    os.replace(ROOT / "sandbox/gitleaks.toml", CONF)
OUT = ROOT / "experiments/2026-11-08-P-0364/results.json"
TRIAGE = WORK / "triage.jsonl"
BUDGET_S = 420
MAX_BLOB = 2_000_000
LONG_LINE = 5000
WINDOW = 400

# P-0358's 12 shapes, for the "did mine miss it" column
MINE = {k: re.compile(v) for k, v in {
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
}.items()}


def git(*a):
    return subprocess.run(["git", "-C", str(ROOT), *a], capture_output=True, text=True).stdout


def entropy(s):
    if not s:
        return 0.0
    n = len(s)
    return -sum(c / n * math.log2(c / n) for c in collections.Counter(s).values())


def comp(p, failed, name):
    # Go RE2 allows a mid-pattern (?i) and \z; Python does not. Moving (?i) to the front widens a
    # rule slightly (more hits, not fewer), which is the safe direction for a leak scan.
    p = p.replace(r"\z", r"\Z").replace("[[:alnum:]", "[a-zA-Z0-9")
    if "(?i)" in p[1:]:
        p = "(?i)" + p.replace("(?i)", "")
    try:
        return re.compile(p)
    except re.error as e:
        failed.append({"rule": name, "error": str(e)[:80]})
        return None


cfg = tomllib.loads(CONF.read_text())
failed = []
G = cfg.get("allowlist", {})
g_paths = [r for r in (comp(p, failed, "global-path") for p in G.get("paths", [])) if r]
g_regex = [r for r in (comp(p, failed, "global-regex") for p in G.get("regexes", [])) if r]
g_stop = [s.lower() for s in G.get("stopwords", [])]

rules, no_kw = [], 0
for r in cfg["rules"]:
    if "regex" not in r:  # path-only rules
        continue
    rx = comp(r["regex"], failed, r["id"])
    if not rx:
        continue
    al = []
    for a in r.get("allowlists", []):
        al.append({
            "cond": a.get("condition", "OR"),
            "target": a.get("regexTarget", "secret"),
            "regex": [x for x in (comp(p, failed, r["id"] + ":allow") for p in a.get("regexes", [])) if x],
            "stop": [s.lower() for s in a.get("stopwords", [])],
            "paths": [x for x in (comp(p, failed, r["id"] + ":allowpath") for p in a.get("paths", [])) if x],
        })
    kw = [k.lower() for k in r.get("keywords", [])]
    no_kw += not kw
    rules.append({"id": r["id"], "rx": rx, "ent": r.get("entropy", 0), "group": r.get("secretGroup", 0), "kw": kw, "al": al})

by_kw = collections.defaultdict(list)
always = []
for r in rules:
    if not r["kw"]:
        always.append(r)
    for k in r["kw"]:
        by_kw[k].append(r)
KW = re.compile("|".join(sorted(map(re.escape, by_kw), key=len, reverse=True)))


def path_allowed(path):
    return any(r.search(path) for r in g_paths)


def allowed(rule, secret, match, line, path):
    low = secret.lower()
    if any(r.search(secret) for r in g_regex) or any(s in low for s in g_stop):
        return True
    for a in rule["al"]:
        target = {"match": match, "line": line}.get(a["target"], secret)
        checks = []
        if a["regex"]:
            checks.append(any(r.search(target) for r in a["regex"]))
        if a["stop"]:
            checks.append(any(s in low for s in a["stop"]))
        if a["paths"]:
            checks.append(any(r.search(path) for r in a["paths"]))
        if checks and (all(checks) if a["cond"] == "AND" else any(checks)):
            return True
    return False


t0 = time.monotonic()
head = []
for row in git("ls-tree", "-r", "HEAD").splitlines():
    meta, path = row.split("\t", 1)
    head.append((meta.split()[2], path, True))
seen_sha = {s for s, _, _ in head}
rest = []
for row in git("rev-list", "--objects", "--all").splitlines():
    parts = row.split(" ", 1)
    if len(parts) == 2 and parts[0] not in seen_sha:
        seen_sha.add(parts[0])
        rest.append((parts[0], parts[1], False))
todo = [b for b in head + rest if not path_allowed(b[1])]
stats = {"blobs_total": len(head) + len(rest), "blobs_head": len(head), "path_allowlisted": len(head) + len(rest) - len(todo),
         "blobs_scanned": 0, "skipped_big": 0, "skipped_binary": 0, "not_blob": 0, "lines_distinct": 0, "bytes_read": 0,
         "long_lines_windowed": 0, "finished": False}

shafile = WORK / "shas.txt"
shafile.write_text("\n".join(s for s, _, _ in todo) + "\n")
proc = subprocess.Popen(["git", "-C", str(ROOT), "cat-file", "--batch"], stdin=open(shafile), stdout=subprocess.PIPE)

seen_lines, hits, unique = set(), [], {}
mine_counts = collections.Counter()


def scan_piece(text, line, lineno, path, in_head):
    kws = {m.group(0) for m in KW.finditer(text.lower())}
    todo_rules = {r["id"]: r for k in kws for r in by_kw[k]}
    for r in always:
        todo_rules[r["id"]] = r
    for r in todo_rules.values():
        for m in r["rx"].finditer(text):
            if r["group"] and r["group"] <= (m.re.groups or 0):
                secret = m.group(r["group"]) or m.group(0)
            else:
                secret = next((g for g in m.groups() if g), m.group(0))
            if r["ent"] and entropy(secret) < r["ent"]:
                continue
            if allowed(r, secret, m.group(0), line, path):
                continue
            mine = [n for n, rx in MINE.items() if rx.search(secret) or rx.search(m.group(0))]
            key = hash((r["id"], secret))
            first = key not in unique
            unique.setdefault(key, 0)
            unique[key] += 1
            if first:
                hits.append({"rule": r["id"], "path": path, "line": lineno, "len": len(secret),
                             "entropy": round(entropy(secret), 2), "in_head": in_head, "mine_caught": mine,
                             "_ctx": text.replace(secret, "<REDACTED>")[:240]})


for sha, path, in_head in todo:
    if time.monotonic() - t0 > BUDGET_S:
        break
    hdr = proc.stdout.readline().split()
    if len(hdr) < 3:
        stats["not_blob"] += 1
        continue
    kind, size = hdr[1], int(hdr[2])
    data = proc.stdout.read(size)
    proc.stdout.read(1)
    if kind != b"blob":
        stats["not_blob"] += 1
        continue
    if size > MAX_BLOB:
        stats["skipped_big"] += 1
        continue
    if b"\0" in data[:8000]:
        stats["skipped_binary"] += 1
        continue
    stats["blobs_scanned"] += 1
    stats["bytes_read"] += size
    for n, line in enumerate(data.decode("utf-8", "ignore").splitlines(), 1):
        h = hash(line)
        if h in seen_lines:
            continue
        seen_lines.add(h)
        for rx_name, rx in MINE.items():
            if rx.search(line[:LONG_LINE]):
                mine_counts[rx_name] += 1
        if len(line) <= LONG_LINE:
            scan_piece(line, line, n, path, in_head)
        else:
            stats["long_lines_windowed"] += 1
            spans, last = [], -1
            for m in KW.finditer(line.lower()):
                if m.start() < last:
                    continue
                last = m.start() + WINDOW
                spans.append((max(0, m.start() - WINDOW), m.start() + WINDOW))
                if len(spans) >= 200:
                    break
            for a, b in spans:
                piece = line[a:b]
                scan_piece(piece, piece, n, path, in_head)
else:
    stats["finished"] = True
proc.kill()
stats["lines_distinct"] = len(seen_lines)
stats["seconds"] = round(time.monotonic() - t0, 1)

with open(TRIAGE, "w") as f:
    for h in hits:
        f.write(json.dumps(h) + "\n")

by_rule = collections.Counter(h["rule"] for h in hits)
res = {
    "rules_in_file": len(cfg["rules"]), "rules_compiled": len(rules), "rules_without_keywords": no_kw,
    "failed_rules": failed, "stats": stats, "unique_hits": len(hits),
    "by_rule": dict(by_rule.most_common()),
    "hits_in_head": sum(h["in_head"] for h in hits),
    "hits_my_12_shapes_also_caught": sum(bool(h["mine_caught"]) for h in hits),
    "my_12_shapes_distinct_lines": dict(mine_counts),
    "hits": [{k: v for k, v in h.items() if k != "_ctx"} for h in hits],
}
OUT.write_text(json.dumps(res, indent=1))
print({k: v for k, v in res.items() if k != "hits"})
