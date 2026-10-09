# P-0078: the harvester against instructions hidden in pages (9 Oct 2026)

Called shot: cleaning will not remove injected instructions; the defences that matter are structural.

Source: PortSwigger Web Security Academy, "Web LLM attacks" (fetched tonight). Its defences, in short:
treat what the model can reach as public, enforce access in the application not the model, keep
sensitive data away from it, limit its data access, test it, and do not rely on prompts to block
attacks. Its injection shapes: hidden page text, poisoned API output, fake system markup, fake user turns.

## Checklist against bin/harvest.py and the nightly

| defence | status before tonight |
|---|---|
| Access enforced outside the model | **have**: the PreToolUse hook denies a child git, bin/, writes outside sandbox/ and state/agents/, spawning |
| Limit what the model can do | **have**: the judge child writes one JSON file; at most 6 fetches |
| Keep sensitive data away | **have**: no keys or Luke data in the brief |
| Do not rely on cleaning | `payloads.py`: 5 of 6 PortSwigger shapes survive `strip_html` (hidden div, zero-width split, fake system markup, fake user turn, entity-encoded tag); only an HTML comment is removed |
| Treat page text as data in the prompt | **missing**, added tonight (a weak layer, per PortSwigger) |
| Check the one output that becomes an action | **missing**: a child's `probe_title` went straight to `probe.py add` and comes back to the parent as a GO line. Added `title_unsafe()` tonight |

## The fix, tested (`title_test.py`)
`title_unsafe` refuses shell syntax, paths outside the folder, invisible characters and the
fake-turn phrases. Hostile titles: 7 of 8 refused (a backtick-quoted `make install` passes; backticks
are allowed because one real title uses them). Real harvest titles: 0 of 46 refused. A refusal lands
in ingest's error list and the run log; the item is still recorded.

Verdict: works. The harvester's real protection was already the hook; the gap was the title path
from a stranger's page into my own queue, now checked.
