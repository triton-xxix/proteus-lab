# Applied patches

Patches moved here once applied from an attended session, so the Smith's nightly check-diff pass stops re-checking them.

- F-0044, F-0054, F-0056: applied 2026-11-12 in a session with Luke (his yes in chat). F-0054's test-hook.py hunks had no trailing context, which git apply reads as end-of-file, so those six cases were inserted by hand; the hook hunks applied with --include. test-hook.py 220 cases, 0 failed.
