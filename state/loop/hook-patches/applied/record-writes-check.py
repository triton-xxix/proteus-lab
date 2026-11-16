#!/usr/bin/env python3
"""Proof for record-writes.diff, outside the hook: the decision table for the board tools, old and new.

Pure Python, imports nothing from .claude/, reads no logs. Exit 0 when the old table shows the two gaps
(a child may write the record; set_routine, set_handoff and set_row are refused for everyone) and the
new table closes both while still denying the task board. 30 Oct 2026.
"""
READS = ("mcp__board__list_log", "mcp__board__list_projects", "mcp__board__list_routines", "mcp__board__list_handoffs")
WRITES = ("mcp__board__log_work", "mcp__board__set_routine", "mcp__board__set_handoff", "mcp__board__set_row")
TASKS = ("mcp__board__claim_task", "mcp__board__post_handoff", "mcp__board__update_task", "mcp__board__list_tasks")


def old(tool, child):
    if tool in ("mcp__board__log_work", "mcp__board__list_log", "mcp__board__list_projects"):
        return "allow"
    return "deny"


def new(tool, child):
    if tool.startswith("mcp__board__"):
        if tool in READS:
            return "allow"
        if tool in WRITES:
            return "deny" if child else "allow"
        return "deny"
    return "deny"


def main():
    gaps_old = [old("mcp__board__log_work", True) == "allow",
                all(old(t, False) == "deny" for t in ("mcp__board__set_routine", "mcp__board__set_handoff", "mcp__board__set_row"))]
    fixed_new = [new("mcp__board__log_work", True) == "deny",
                 all(new(t, False) == "allow" for t in WRITES),
                 all(new(t, False) == "allow" for t in READS),
                 all(new(t, child) == "deny" for t in TASKS for child in (False, True)),
                 all(new(t, True) == "deny" for t in WRITES)]
    for name, ok in (("old: child may write the record", gaps_old[0]), ("old: set_* refused for the parent", gaps_old[1]),
                     ("new: child write denied", fixed_new[0]), ("new: parent writes allowed", fixed_new[1]),
                     ("new: reads allowed", fixed_new[2]), ("new: task board denied", fixed_new[3]),
                     ("new: every child write denied", fixed_new[4])):
        print(("PASS " if ok else "FAIL ") + name)
    raise SystemExit(0 if all(gaps_old) and all(fixed_new) else 1)


if __name__ == "__main__":
    main()
