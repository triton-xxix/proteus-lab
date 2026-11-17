#!/usr/bin/env python3
"""Title-and-opening digests for the Skool reading queue rows S-39 and S-55 (13 Nov 2026, F-0093).

    python3 -I /Users/triton/PROTEUS/sandbox/skool_digest_titles.py

Reads the local transcripts in field-notes/skool/transcripts/ (gitignored) and writes, next to them:
    field-notes/skool/digest-S-39-titles.md   vault-*  (YouTube lessons from the vault rooms), grouped by room
    field-notes/skool/digest-S-55-titles.md   whatisskool-*  (What Is Skool videos), oldest post first
One entry per transcript: a heading made from the slug, the filename, then the first 150 words of
the talk. A transcript under 20 words is skipped and listed at the bottom. Stdlib only, local files
only, no network. It does not touch the queue; that is edited separately.
"""
import os
import re
import sys
from collections import Counter, defaultdict

ROOT = "/Users/triton/PROTEUS/"
TDIR = ROOT + "field-notes/skool/transcripts/"
OPENING_WORDS = 150
MIN_WORDS = 20
BUILT = "13 Nov 2026"
TS = re.compile(r"\[\d+:\d{2}(?::\d{2})?\]")


def read_transcript(path):
    """Return (source line, words). Header lines start with '#'; [mm:ss] stamps are dropped."""
    lines = open(path, errors="replace").read().splitlines()
    via = next((l[1:].strip() for l in lines if l.startswith("# via")), "source unknown")
    body = TS.sub(" ", " ".join(l for l in lines if not l.startswith("#")))
    return via, body.split()


def titleise(words):
    t = " ".join(w for w in words.split("-") if w)
    return t[:1].upper() + t[1:] if t else "(no title in slug)"


def vault_ids():
    """slug -> YouTube id, from the batch TSV, because an id can itself start with '-' or contain '_'."""
    ids = {}
    tsv = ROOT + "field-notes/skool/batch-2026-10-15-vault-youtube.tsv"
    for line in open(tsv):
        parts = line.rstrip("\n").split("\t")
        if len(parts) < 2:
            continue
        m = re.search(r"[?&]v=([^&]+)", parts[1]) or re.search(r"youtu\.be/([^?&]+)", parts[1])
        if m:
            ids[parts[0]] = m.group(1)
    return ids


def parse_vault(slug, ids):
    vid = ids.get(slug)
    m = re.match(r"vault-(.+?)-" + re.escape(vid) + r"(?:-(.*))?$", slug) if vid else None
    if not m:
        return None
    return {"room": m.group(1), "id": vid, "title": titleise(m.group(2) or "")}


def parse_wis(slug):
    m = re.match(r"whatisskool-post-(\d{4}-\d{2}-\d{2})-(.*)$", slug)
    if not m:
        return None
    return {"date": m.group(1), "title": titleise(m.group(2))}


def looks_loopy(opening):
    """Whisper sometimes loops on one phrase; flag an opening that is mostly repeats."""
    return len(opening) >= 100 and len(set(w.lower() for w in opening)) / len(opening) < 0.3


def source_name(via):
    """'via whisper base.en (local)' -> 'whisper base.en'; 'via loom transcript' -> 'loom transcript'."""
    return via.replace("via ", "", 1).replace(" (local)", "")


def entry(heading, fname, via, words, extra=""):
    opening = words[:OPENING_WORDS]
    text = " ".join(opening) + (" ..." if len(words) > OPENING_WORDS else "")
    meta = "`%s` | %s words | %s%s" % (fname, format(len(words), ","), source_name(via), extra)
    flag = "**Check:** the opening repeats itself, possibly a whisper loop.\n\n" if looks_loopy(opening) else ""
    return "### %s\n%s\n\n%s%s\n" % (heading, meta, flag, text)


def main():
    files = sorted(f for f in os.listdir(TDIR) if f.endswith(".txt"))
    vault = [f for f in files if f.startswith("vault-")]
    wis = [f for f in files if f.startswith("whatisskool-")]
    ids = vault_ids()
    unparsed = []

    # ---- S-39 ----
    rooms = defaultdict(list)
    skipped39, via39 = [], Counter()
    for f in vault:
        slug = f[:-4]
        meta = parse_vault(slug, ids)
        via, words = read_transcript(TDIR + f)
        if not meta:
            unparsed.append(f)
            continue
        if len(words) < MIN_WORDS:
            skipped39.append((f, len(words)))
            continue
        via39[via] += 1
        h = "%s: %s" % (meta["room"], meta["title"])
        rooms[meta["room"]].append(entry(h, f, via, words, " | youtube %s" % meta["id"]))
    n39 = sum(len(v) for v in rooms.values())
    out = ["# S-39 digest: title and opening of the vault-room YouTube lessons",
           "Built %s from %d local transcripts (%s) in field-notes/skool/transcripts/: heading from the slug (the slug cuts long titles short), then the first %d words, grouped by room. %d skipped as empty or under %d words, listed at the end."
           % (BUILT, n39, ", ".join("%d %s" % (n, source_name(v)) for v, n in via39.items()), OPENING_WORDS, len(skipped39), MIN_WORDS),
           "Rooms (entries): " + ", ".join("%s (%d)" % (r, len(rooms[r])) for r in sorted(rooms, key=lambda r: (-len(rooms[r]), r))) + ".",
           ""]
    for r in sorted(rooms, key=lambda r: (-len(rooms[r]), r)):
        out.append("## Room: %s (%d)\n" % (r, len(rooms[r])))
        out.extend(rooms[r])
    out.append("## Skipped (under %d words)\n" % MIN_WORDS)
    out.extend("- `%s` (%d words)" % x for x in skipped39) if skipped39 else out.append("None.")
    open(ROOT + "field-notes/skool/digest-S-39-titles.md", "w").write("\n".join(out) + "\n")

    # ---- S-55 ----
    items, skipped55, via55 = [], [], Counter()
    for f in wis:
        meta = parse_wis(f[:-4])
        via, words = read_transcript(TDIR + f)
        if not meta:
            unparsed.append(f)
            continue
        if len(words) < MIN_WORDS:
            skipped55.append((f, len(words)))
            continue
        via55[via] += 1
        items.append((meta["date"], f, entry("%s: %s" % (meta["date"], meta["title"]), f, via, words)))
    items.sort()
    out = ["# S-55 digest: title and opening of the What Is Skool videos",
           "Built %s from %d local transcripts (%s) in field-notes/skool/transcripts/: heading is the post date and the slug title (the slug cuts long titles short), then the first %d words, oldest post first. %d skipped as empty or under %d words, listed at the end."
           % (BUILT, len(items), ", ".join("%d %s" % (n, source_name(v)) for v, n in via55.items()), OPENING_WORDS, len(skipped55), MIN_WORDS),
           ""]
    out.extend(i[2] for i in items)
    out.append("## Skipped (under %d words)\n" % MIN_WORDS)
    out.extend("- `%s` (%d words)" % x for x in skipped55) if skipped55 else out.append("None.")
    open(ROOT + "field-notes/skool/digest-S-55-titles.md", "w").write("\n".join(out) + "\n")

    print("S-39: %d vault transcripts, %d entries, %d skipped %s" % (len(vault), n39, len(skipped39), skipped39))
    print("S-55: %d whatisskool transcripts, %d entries, %d skipped %s" % (len(wis), len(items), len(skipped55), skipped55))
    if unparsed:
        print("UNPARSED slugs (not in a digest):", unparsed)
        sys.exit(1)


if __name__ == "__main__":
    main()
