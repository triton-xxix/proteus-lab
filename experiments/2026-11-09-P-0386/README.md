# P-0386: how common is the "tiny repo, stars, paste-site install" pattern? (9 Nov 2026)

Detection side, read-only (`count.py`). Every repo GitHub's search lists as created since 6 Nov with 50 or more stars, 152 of them, README read as plain text. No linked file was fetched and no repo was run. Results are counts only: a regex match is not proof about any single repo, so none are named.

| Test | Repos of 152 |
|---|---|
| Under 50 KB | 38 |
| README has a paste-site, Telegram or shortener link | 14 |
| ...and the repo is under 50 KB | 11 |
| ...under 50 KB, paste-site link, and a run-the-exe, inject, disable-antivirus or archive-password phrase | 10 |
| Paste-site link in a repo of 50 KB or more | 3 |
| Mentions a binary or archive download | 54 (too loose to use) |
| Forks at least half the stars, under 50 KB | 9 |
| Forks at least half the stars, 50 KB or more | 10 of 114 |

Reading it: P-0381's pattern is not a one-off. 10 of the 152 starred new repos (6.6%) match all three parts, and 11 of the 14 paste-link READMEs sit in repos under 50 KB. Paste links concentrate in tiny repos: 11 of 38 tiny against 3 of 114 larger. High forks-to-stars is also commoner in the tiny group (9 of 38 against 10 of 114).

What it does not say: I did not audit the matches, so the false-positive rate is unknown. A Telegram link is an ordinary community link in plenty of honest projects; the run-or-inject phrases are the stricter part of the test. Whether any of the 10 is malicious is not established, and search only surfaces repos GitHub still lists, so anything already taken down is missing. One three-day window.
