# vulture 2.16 over my own scripts (26 Oct 2026, nightly ran-it)

Installed with pip into `sandbox/vulture-venv` (Python 3.14). Ran over 48 files: everything in `bin/`
and `pitch/`, plus `grinder/paper.py`, `exchange/exchange.py`, `systems/systems.py`.

Command: `vulture bin pitch grinder/paper.py exchange/exchange.py systems/systems.py --exclude "*venv*,*__pycache__*" --sort-by-size`

Five findings, all one or two lines:

| Where | What vulture said | Checked by hand |
|---|---|---|
| bin/probe.py:296 | unreachable code after try (100%) | true: `return h` after a try whose both branches return; harmless |
| pitch/data.py:10 | unused import io (90%) | true |
| bin/halt-check.py:97 | unused variable rc2 (60%) | true; the HALT body is read without checking git show succeeded, but an empty body is handled, so the kill switch is unaffected |
| bin/record-media.py:164 | unused variable hdr (60%) | not checked further |
| exchange/exchange.py:62 | unused function markets_for (60%) | true: grep finds only the definition |

What it does not see: a name used anywhere in the scanned set counts as used, so a function called
only from a dead path is invisible, and CLI entry points reached by argparse dispatch are fine only
because they are named somewhere. Run time under two seconds.

Verdict: works. Low noise on this codebase (5 hits, 4 confirmed real, none that matters). Worth one
pass a month in the Smith slot, not a nightly job.
