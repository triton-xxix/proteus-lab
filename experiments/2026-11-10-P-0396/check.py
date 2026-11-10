"""P-0396: does every link in the Proteus memory index point at a real, non-empty file?

Also the reverse (files no index line points at), frontmatter presence, and [[wiki links]] in bodies
that name no existing memory. Reads only; prints counts and writes results.json beside itself.
File names are reported; file contents are not copied anywhere.
"""
import json, re
from pathlib import Path

MEM = Path.home() / ".claude/projects/-Users-triton-PROTEUS/memory"
HERE = Path(__file__).resolve().parent

index = (MEM / "MEMORY.md").read_text()
links = re.findall(r"\[([^\]]+)\]\(([^)]+\.md)\)", index)
lines = [l for l in index.splitlines() if l.strip()]
files = sorted(p.name for p in MEM.glob("*.md") if p.name != "MEMORY.md")

missing, empty, no_front, ok = [], [], [], []
names = {}
for title, target in links:
    p = MEM / target
    if not p.exists():
        missing.append(target)
        continue
    body = p.read_text()
    if len(body.strip()) < 40:
        empty.append(target)
        continue
    m = re.match(r"---\n(.*?)\n---\n", body, re.S)
    if not m or "name:" not in m.group(1) or "description:" not in m.group(1):
        no_front.append(target)
    else:
        nm = re.search(r"^name:\s*(.+)$", m.group(1), re.M)
        names[nm.group(1).strip()] = target
    ok.append(target)

linked = {t for _, t in links}
orphans = [f for f in files if f not in linked]
dupes = sorted({t for _, t in links if [x for _, x in links].count(t) > 1})
non_link_lines = [l[:60] for l in lines if not re.search(r"\]\([^)]+\.md\)", l)]

stems = {f[:-3] for f in files} | set(names)
wiki_total, wiki_dead = 0, {}
for f in files:
    for w in re.findall(r"\[\[([^\]]+)\]\]", (MEM / f).read_text()):
        wiki_total += 1
        if w not in stems and w.replace("-", "_") not in stems:
            wiki_dead.setdefault(w, []).append(f)

res = {
    "index_links": len(links), "files_on_disk": len(files),
    "missing": missing, "empty": empty, "no_frontmatter": no_front,
    "orphans_not_in_index": orphans, "duplicate_targets": dupes,
    "index_lines_without_a_link": non_link_lines,
    "wiki_links": wiki_total, "wiki_links_to_nothing": wiki_dead,
    "index_chars": len(index),
}
(HERE / "results.json").write_text(json.dumps(res, indent=1))
print(json.dumps(res, indent=1))
