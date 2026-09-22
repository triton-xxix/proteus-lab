---
name: project_charter_is_the_rules
description: CHARTER.md in /Users/triton/PROTEUS is the only rules file; the OBSIDIAN vault's policy, ledger and memory are out of bounds by design
metadata:
  type: project
---

Proteus's rules live in `/Users/triton/PROTEUS/CHARTER.md`. Nothing in `/Users/triton/OBSIDIAN`
binds it unless copied in. It never reads the Flywheel ledger, briefs or the OBSIDIAN memory index.

**Why:** the default agent's memory made it reach the same conclusions as Luke. Separate memory is
the structural fix, not a preference.

**How to apply:** at session start read CHARTER.md and this memory directory. Do not follow the
global CLAUDE.md instruction to load Luke's memory index or knowledge pack. Write only under the
Proteus folder and the vault mirror folder `TRITON-CORE/Proteus/`.
