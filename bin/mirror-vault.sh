#!/usr/bin/env bash
# Mirror the human-readable Proteus artefacts into the vault folder, and nothing else.
#
#   bash /Users/triton/PROTEUS/bin/mirror-vault.sh
#
# Copies (only when changed):
#   field-notes/YYYY-WW.md   -> TRITON-CORE/Proteus/field-notes/YYYY-WW.md   (finished weekly notes; drafts stay here)
#   field-notes/SEEN.md      -> TRITON-CORE/Proteus/SEEN.md                  (novelty register)
#   TRACK-RECORD.md          -> TRITON-CORE/Proteus/TRACK-RECORD.md          (score snapshot, rebuilt by bin/score.py)
#   intel/*.md               -> TRITON-CORE/Proteus/intel/                  (intelligence lane, charter v2)
#   graduates/*.md           -> TRITON-CORE/Proteus/graduates/              (handover notes, charter v2)
#
# Never deletes anything in the vault folder and never touches files it did not copy, so a one-way
# feed written from the vault side can sit in the same folder. Replaces the symlink to the working
# tree that was removed 2026-09-24 (it made Obsidian index the venv, git objects and caches).
# Runs under HALT: a local copy into the vault is not a side effect the kill switch covers.
set -u
SRC="/Users/triton/PROTEUS"
DST="/Users/triton/OBSIDIAN/TRITON-CORE/Proteus"
if [ ! -d "$DST" ]; then
  echo "vault folder missing: $DST" >&2
  exit 1
fi
if [ -L "$DST/PROTEUS" ]; then
  echo "WARNING: $DST/PROTEUS symlink is back; the vault is indexing the whole working tree again" >&2
fi
mkdir -p "$DST/field-notes"
copied=0
copy() {
  local from="$1" to="$2"
  [ -f "$from" ] || return 0
  if [ ! -f "$to" ] || ! cmp -s "$from" "$to"; then
    cp "$from" "$to" && copied=$((copied + 1)) && echo "mirrored ${to#$DST/}"
  fi
}
for f in "$SRC"/field-notes/[0-9][0-9][0-9][0-9]-W[0-9][0-9].md; do
  [ -e "$f" ] && copy "$f" "$DST/field-notes/$(basename "$f")"
done
copy "$SRC/field-notes/SEEN.md" "$DST/SEEN.md"
copy "$SRC/TRACK-RECORD.md" "$DST/TRACK-RECORD.md"
for lane in intel graduates; do
  if [ -d "$SRC/$lane" ]; then
    mkdir -p "$DST/$lane"
    for f in "$SRC"/$lane/*.md; do
      [ -e "$f" ] && copy "$f" "$DST/$lane/$(basename "$f")"
    done
  fi
done
echo "mirror done: $copied file(s) copied"
exit 0
