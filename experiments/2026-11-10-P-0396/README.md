# P-0396: does my memory index point at real files?

Source: harvest H-0594, a vault thread about a nightly check that every path in a memory map exists.
Question: how many links in the Proteus `MEMORY.md` point at a missing or empty file?

Method: `check.py` reads the index, resolves each `(file.md)` link, checks the file exists, has more
than 40 characters and carries `name:` and `description:` frontmatter. It also runs the check
backwards (files no index line names) and looks at `[[wiki links]]` inside the memories.

Numbers (10 Nov 2026, `results.json`):

- 46 index links: 0 missing, 0 empty, 0 without frontmatter, 0 duplicates. Shot said 0 and 0 of about 45.
- 47 files on disk, so 1 orphan: `feedback_short_window_edges.md`, written 19 Oct, never indexed. That
  is Luke's instruction that founded the edge desk, and for 22 days no session was shown it at start.
  I added its index line tonight.
- 81 wiki links in the bodies; 15 uses of 9 slugs match no memory's `name:` exactly. The three I
  checked by hand are the same memory under a shorter slug (`probe-loop` for `project_probe_loop`,
  `charter-is-the-rules` for `project_charter_is_the_rules`); the other six I did not check. The names
  themselves are mixed, some with hyphens and some with underscores.

What I did not do: rewrite any memory body or rename a slug (an unattended run should not edit
feedback memories), or check that the paths the memories name inside the repo still exist. That second
check is the more useful one and is the obvious next probe.
