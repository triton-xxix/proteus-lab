"""P-0236: read agent-purge 0.2.8 statically, never run it.

Lists the tarball, then greps the JS for what `ls`/`detect` touches: file writes, spawned
processes, network calls, binary patching and the home paths it reads.
"""
import io, json, re, sys, tarfile
from pathlib import Path

tgz = Path(sys.argv[1])
out = {"files": [], "hits": {}}
PATTERNS = {
    "writes": r"writeFileSync|writeFile\(|appendFileSync|rmSync|unlinkSync|renameSync|chmodSync|copyFileSync",
    "spawns": r"spawnSync|execSync|execFileSync|spawn\(|execFile\(|exec\(",
    "network": r"fetch\(|https?\.request|http\.get|net\.connect|WebSocket",
    "binary_patch": r"Buffer\.from\([^)]*identity|patchBinary|binary|\.asar|equal-length|等长",
    "home_paths": r"\.claude|\.codex|\.config/opencode|homedir\(\)|AGENT_PURGE_HOME",
    "shim_path": r"PATH|\.local/bin|shim",
}
with tarfile.open(tgz) as t:
    for m in t.getmembers():
        if not m.isfile():
            continue
        out["files"].append([m.name, m.size])
        if not m.name.endswith((".mjs", ".js", ".ts", ".cjs")):
            continue
        text = t.extractfile(m).read().decode("utf-8", "replace")
        for k, p in PATTERNS.items():
            n = len(re.findall(p, text))
            if n:
                out["hits"].setdefault(m.name, {})[k] = n
        if m.name.endswith("bin/agent-purge.mjs"):
            # the command table: which subcommand calls what
            cmds = re.findall(r"case ['\"]([a-z-]+)['\"]", text)
            out["subcommands"] = sorted(set(cmds))
            i = text.find("'ls'")
            out["ls_context"] = text[max(0, i - 200): i + 600] if i >= 0 else ""
json.dump(out, open(Path(__file__).parent / "static.json", "w"), indent=1, ensure_ascii=False)
for f, s in out["files"]:
    print(s, f)
print(json.dumps(out["hits"], indent=1))
print("subcommands", out.get("subcommands"))
print("ls_context:", out.get("ls_context", "")[:800])
