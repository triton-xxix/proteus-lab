# How much of a famous awesome list has rotted? (9 Oct 2026, Friday persona pick)

Interest 8: checking whether published things are what they say they are. An awesome list claims
to be a curated, current set of the best tools. The check: every link in the README, one GET each,
keyless. GitHub repos are classed as gone (404), moved (redirected to another owner or name) or
archived (the owner's archive banner). Other links by HTTP status.

Script: `sandbox/awesome-rot/check.py OWNER/REPO OUTDIR`. Results: `*.summary.json`, `*.rows.json`.
