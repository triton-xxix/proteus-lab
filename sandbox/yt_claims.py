"""Pull checkable claims out of the staged YouTube transcripts.

The 'watched it' slot wants claims checked, not summaries repeated. This greps the
staged .txt transcripts for the specific, falsifiable assertions people make about
Agent Skills: field names, limits, load behaviour, file locations.
"""
import glob
import os
import re

STAGING = "/Users/triton/PROTEUS/field-notes/staging"

TERMS = [
    "character", "1024", "64", "frontmatter", "front matter", "yaml",
    "progressive disclosure", "only load", "loads only", "into context",
    "allowed-tools", "allowed tools", "dot claude", ".claude/skills",
    "always loaded", "token", "name and description",
]

for path in sorted(glob.glob(os.path.join(STAGING, "*.txt"))):
    text = open(path, encoding="utf-8", errors="replace").read()
    title = text.splitlines()[0].lstrip("# ").strip()
    hits = []
    low = text.lower()
    for t in TERMS:
        for m in re.finditer(re.escape(t), low):
            a = max(0, m.start() - 110)
            b = min(len(text), m.end() + 110)
            hits.append(" ".join(text[a:b].split()))
    seen, uniq = set(), []
    for h in hits:
        k = h[:70]
        if k not in seen:
            seen.add(k)
            uniq.append(h)
    print("=" * 70)
    print(os.path.basename(path), "|", title)
    for h in uniq[:8]:
        print("  -", h)
