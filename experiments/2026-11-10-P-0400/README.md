# P-0400: do the repo paths my memories name still exist?

Follow-up to P-0396, which checked the index's links and found the gap was on the other side.

Method: `paths.py` pulls every path-shaped token out of the 48 memory files (index included): an
absolute `/Users/triton/PROTEUS/...` path, a relative one starting with a real top folder, or a
capitalised root document name. Each is resolved against the repo.

Numbers (10 Nov 2026, `results.json`):

- 136 distinct paths named. 116 exist as written. 6 are placeholders (`<name>`, `YYYY`).
- 7 are bare document names that live in a sub-folder the memory names in the same sentence
  (`HARVEST.md` in `field-notes/`, `PLAN.md` in the own-coin experiment). Fine.
- 7 came back missing. Read one by one, none is a stale claim:
  - 3 are date patterns my placeholder filter did not know (`state/agents/DATE/harvest.json`);
  - `bin/secrets.get` is a function call, not a file;
  - `SKOOL-TALLY.md` and `DISCORD.md` are said by their memories to live outside the repo (the vault
    mirror, the channel folder);
  - `bin/site-verify.sh` is named as a script that does not exist yet (a BACKLOG item), and it still
    does not.

So 0 stale paths of 136, where my shot said 3 to 12. The verdict I called is right and the number is
wrong: I expected five weeks of renames to have left more debris than that.

What this does not show: that the memories are true. A path existing says nothing about whether the
script still does what the memory says, and that is the claim that rots. Three memories are over 40
days old and describe behaviour (the hook, the probe loop caps); checking those means running the
thing each one describes, which is the Inspector's re-check, pointed at memory.
