# P-0219: ex-ussr-kinship-research audit script

Question: does the repo's audit script run, and does it flag weak corroboration?

Fetched the main-branch tarball (codeload, no git clone) into `sandbox/p0219-kinship/`. Read the script first: stdlib only, no network. The tests folder has no `__init__.py`, so `unittest discover` refuses it; `run_tests.py` loads the module directly.

- The repo's own tests: 14 of 14 pass in 4.2 s.
- My own three cases (`weak.py`, `weak-results.json`), one claim marked `corroborated` with two artifacts:
  - both artifacts copies of one record (same group): 1 warning, "corroborated, but independent groups found: 1";
  - a second group declared on the claim with no artifact behind it: 1 error plus the same warning, so corroboration cannot be declared into existence, as the README says;
  - two artifacts in two real groups: clean.

The messages are in Russian (the skill's language); the agent is meant to translate. The idea travels: the same independence-group check would fit any Proteus register where two sources may be one source copied, such as harvest items quoting one press release.

Verdict: works.
