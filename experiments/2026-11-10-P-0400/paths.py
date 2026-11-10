"""P-0400: do the repo paths my memories name still exist?

Pulls path-shaped tokens out of every memory file (index included): things in backticks or bare that
look like a relative repo path (a known top folder plus a slash, or a root file with an extension) or an
absolute /Users/triton/PROTEUS path. Resolves each against the repo. Globs and placeholders (<name>,
YYYY, *) are counted apart, not as missing. Reports names only.
"""
import json, re
from pathlib import Path

MEM = Path.home() / ".claude/projects/-Users-triton-PROTEUS/memory"
REPO = Path("/Users/triton/PROTEUS")
HERE = Path(__file__).resolve().parent
tops = {p.name for p in REPO.iterdir() if p.is_dir() and not p.name.startswith(".git")} | {".claude"}
rootfiles = {p.name for p in REPO.iterdir() if p.is_file()}

tok = re.compile(r"[A-Za-z0-9_.<>*~/-]+")
found = {}
for f in sorted(MEM.glob("*.md")):
    for t in tok.findall(f.read_text()):
        t = t.rstrip(".,;:)").lstrip("(")
        if t.startswith("/Users/triton/PROTEUS/"):
            rel = t[len("/Users/triton/PROTEUS/"):]
        elif "/" in t and t.split("/")[0] in tops and not t.startswith("/"):
            rel = t
        elif re.fullmatch(r"[A-Z][A-Z0-9-]+\.md", t) and t != "MEMORY.md":
            rel = t  # root docs like CHARTER.md; may also live in a sub-folder, checked below
        else:
            continue
        if not rel:
            continue
        found.setdefault(rel, set()).add(f.name)

exists, missing, placeholder, elsewhere = [], [], [], []
for rel, where in sorted(found.items()):
    if re.search(r"[<>*]|YYYY|NN\b|00N", rel):
        placeholder.append(rel)
        continue
    p = REPO / rel
    if p.exists():
        exists.append(rel)
    elif "/" not in rel:
        hits = [str(h.relative_to(REPO)) for h in REPO.glob("*/" + rel)] + [str(h.relative_to(REPO)) for h in REPO.glob("*/*/" + rel)]
        (elsewhere if hits else missing).append({"path": rel, "in": sorted(where), "found_at": hits[:3]} if hits else {"path": rel, "in": sorted(where)})
    else:
        missing.append({"path": rel, "in": sorted(where)})

res = {"distinct_paths": len(found), "exist": len(exists), "placeholders": len(placeholder),
       "root_name_found_in_a_subfolder": elsewhere, "missing": missing}
(HERE / "results.json").write_text(json.dumps(res, indent=1))
print(json.dumps(res, indent=1))
