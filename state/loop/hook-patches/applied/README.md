# Applied patches

Patches moved here once applied from an attended session, so the Smith's nightly check-diff pass stops re-checking them.

- F-0044, F-0054, F-0056: applied 2026-11-12 in a session with Luke (his yes in chat). F-0054's test-hook.py hunks had no trailing context, which git apply reads as end-of-file, so those six cases were inserted by hand; the hook hunks applied with --include. test-hook.py 220 cases, 0 failed.
- record-writes: applied 2026-10-30 on Luke's word (the team record). Copied here by the Smith on 16 Nov 2026 after check-diff read MISMATCH on all three hunks because the hook already carries them (one `mcp__board__log_work` rule in the live hook). The originals in the parent folder still need deleting by an interactive session; a scheduled run has no rm.
