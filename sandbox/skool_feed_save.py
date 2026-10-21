#!/usr/bin/env python3
"""Write a Skool community feed, dumped from the browser pane, to field-notes/skool/ files.

    skool_feed_save.py DUMP.txt KEY PREFIX OWNER[,OWNER2] ["Room title"]

DUMP.txt is a saved javascript_tool result (JSON [{type, text}]) whose text is a JSON object; KEY picks
the list of posts in it ({d, by, name, t, c, v, s, n, u}). Writes:
  PREFIX-posts-owner.md     owners' posts in full, oldest first, videos listed
  PREFIX-posts-members.md   everyone else, 280 characters each (skipped if none)
  sandbox/PREFIX-owner-videos.tsv     slug<TAB>url for owners' YouTube/Loom/Vimeo links
  sandbox/PREFIX-owner-skoolvids.tsv  slug<TAB>post name<TAB>video id for Skool-hosted ones
Written 19 Oct 2026 after Start Your Skool showed the feed, not the classroom, can hold a room's material.
"""
import json, re, sys

dump, key, prefix, owners = sys.argv[1], sys.argv[2], sys.argv[3], set(sys.argv[4].split(","))
title = sys.argv[5] if len(sys.argv) > 5 else prefix
F = "/Users/triton/PROTEUS/field-notes/skool/"
S = "/Users/triton/PROTEUS/sandbox/"
txt = json.load(open(dump))[0]["text"]
data, _ = json.JSONDecoder().raw_decode(txt[txt.index("{"):])
posts = sorted(data[key], key=lambda x: x["d"])
own = [p for p in posts if p["by"] in owners]
oth = [p for p in posts if p["by"] not in owners]
slugify = lambda s: re.sub(r"[^a-z0-9]+", "-", (s or "post").lower()).strip("-")[:50]

with open(F + prefix + "-posts-owner.md", "w") as fh:
    fh.write("# %s: owner posts (%s), pulled from the community feed\n\n%d of %d posts. Oldest first.\n\n"
             % (title, ", ".join(sorted(owners)), len(own), len(posts)))
    for p in own:
        fh.write("## %s · %s · %s\n" % (p["d"], p["by"], p["t"]))
        if p["v"]:
            fh.write("Video: %s\n" % ", ".join(p["v"]))
        if p["s"]:
            fh.write("Skool-hosted video %s\n" % p["s"])
        fh.write("\n%s\n\n" % (p["c"] or "").strip())
if oth:
    with open(F + prefix + "-posts-members.md", "w") as fh:
        fh.write("# %s: member posts, first 280 characters each\n\n" % title)
        for p in oth:
            fh.write("- %s · %s · %s (%d comments): %s\n" % (p["d"], p["by"], p["t"], p["n"], (p["c"] or "").replace("\n", " ")[:280]))
ext, sk = [], []
for p in own:
    base = "%s-post-%s-%s" % (prefix, p["d"], slugify(p["t"]))
    for i, u in enumerate(p["v"]):
        ext.append((base + ("-%d" % i if i else ""), u.split("&")[0]))
    if p["s"]:
        for i, vid in enumerate(p["s"].split(",")):
            sk.append((base + ("-%d" % i if i else ""), p["name"], vid))
open(S + prefix + "-owner-videos.tsv", "w").write("".join("%s\t%s\n" % r for r in ext))
open(S + prefix + "-owner-skoolvids.tsv", "w").write("".join("%s\t%s\t%s\n" % r for r in sk))
print("%s: %d posts, %d by owners (%d words), %d external videos, %d Skool-hosted"
      % (prefix, len(posts), len(own), sum(len((p["c"] or "").split()) for p in own), len(ext), len(sk)))
