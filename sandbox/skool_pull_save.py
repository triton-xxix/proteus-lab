#!/usr/bin/env python3
"""Save one room from the 19 Oct browser pull job (window.__pull[group]) to field-notes/skool/.

    skool_pull_save.py DUMP.txt PREFIX "Room title" SLUG

DUMP.txt is a saved javascript_tool result whose text is the JSON of one room:
{courses: [markdown], caps: [[title, transcript]], ext: [[title, url]], posts: [...], locked: [...], ownerId}.
Writes PREFIX-NN-course.md, transcripts/PREFIX-*.txt, PREFIX-posts-owner.md, PREFIX-posts-members.md,
PREFIX-index.md, and appends external videos to the transcribe queue.
"""
import json, os, re, subprocess, sys

dump, prefix, title, slug = sys.argv[1:5]
F = "/Users/triton/PROTEUS/field-notes/skool/"
txt = json.load(open(dump))[0]["text"]
R, _ = json.JSONDecoder().raw_decode(txt[txt.index("{"):])
sl = lambda s: re.sub(r"[^a-z0-9]+", "-", (s or "x").lower()).strip("-")[:60]
files = []
for i, md in enumerate(R.get("courses", []), 1):
    name = "%s-%02d-%s.md" % (prefix, i, sl(md.splitlines()[0].lstrip("# ")))
    open(F + name, "w").write("<!-- skool.com/%s classroom, pulled 19 Oct 2026 -->\n%s" % (slug, md))
    files.append((name, len(md.split())))
caps_words = 0
for t, body in R.get("caps", []):
    name = "transcripts/%s-%s.txt" % (prefix, sl(t))
    open(F + name, "w").write("# %s: %s\n# via Skool player English captions (Mux)\n\n%s\n" % (title, t, body))
    caps_words += len(body.split())
posts = sorted(R.get("posts", []), key=lambda p: p["d"])
own = [p for p in posts if p.get("own")]
oth = [p for p in posts if not p.get("own")]
if own:
    with open(F + prefix + "-posts-owner.md", "w") as fh:
        fh.write("# %s: owner posts, pulled 19 Oct 2026\n\n%d of %d posts saved are the owner's. Oldest first.\n\n" % (title, len(own), len(posts)))
        for p in own:
            fh.write("## %s · %s · %s\n" % (p["d"], p["by"], p["t"]))
            if p["v"]:
                fh.write("Video: %s\n" % ", ".join(p["v"]))
            fh.write("\n%s\n\n" % (p["c"] or "").strip())
if oth:
    with open(F + prefix + "-posts-members.md", "w") as fh:
        fh.write("# %s: member posts, first 280 characters each\n\n" % title)
        for p in oth:
            fh.write("- %s · %s · %s (%d comments): %s\n" % (p["d"], p["by"], p["t"], p["n"], (p["c"] or "").replace("\n", " ")[:280]))
ext = [("%s-lesson-%s" % (prefix, sl(t)), u) for t, u in R.get("ext", [])]
for p in own:
    for i, u in enumerate(p["v"]):
        ext.append(("%s-post-%s-%s%s" % (prefix, p["d"], sl(p["t"])[:50], "-%d" % i if i else ""), u.split("&")[0]))
qf = "/Users/triton/PROTEUS/sandbox/%s-videos.tsv" % prefix
open(qf, "w").write("".join("%s\t%s\n" % r for r in ext))
add = subprocess.run(["python3", "/Users/triton/PROTEUS/bin/skool-transcribe-queue.py", "add", qf], capture_output=True, text=True).stdout.strip()
ow = sum(len((p["c"] or "").split()) for p in own)
with open(F + prefix + "-index.md", "w") as fh:
    fh.write("# %s, pull index (19 Oct 2026)\n\nskool.com/%s, pulled through the browser pane (luke-boyd-4592) by the 19 Oct pull job.\n\n" % (title, slug))
    fh.write("- Classroom: %d open course(s): %s\n" % (len(files), ", ".join("`%s` (%d words)" % f for f in files) or "none"))
    fh.write("- Locked: %s\n" % (", ".join(R.get("locked", [])) or "none"))
    fh.write("- Skool-hosted videos captioned: %d (%d words), `transcripts/%s-*`\n" % (len(R.get("caps", [])), caps_words, prefix))
    fh.write("- Feed: %d posts saved, %d by the owner (%d words) in `%s-posts-owner.md`; others trimmed in `%s-posts-members.md`\n" % (len(posts), len(own), ow, prefix, prefix))
    fh.write("- External videos queued for transcription: %d (%s)\n" % (len(ext), add))
print("%s: %d courses, %d caps (%d words), %d posts / %d owner (%d words), %d ext videos; %s" % (prefix, len(files), len(R.get("caps", [])), caps_words, len(posts), len(own), ow, len(ext), add))
