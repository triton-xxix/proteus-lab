# P-0364: gitleaks' rules over this repo and its history

**Question.** P-0358 scanned with 12 secret shapes of my own and found nothing outside Google's docs pages.
Do gitleaks' default rules, run over every blob in git history, find a real secret mine missed?

**Called shot.** works at 0.75; 0 real secrets beyond the Google docs key; about 100 raw hits, nearly all
generic-api-key false alarms.

**Method.** `scan.py` is my own Python mimic of gitleaks, not gitleaks: keyword prefilter, first non-empty
group as the secret, entropy floor, global and per-rule allowlists. Rule file fetched from gitleaks master
on 8 Nov 2026 (222 rules, 221 with a regex). Lines are deduped across blobs, HEAD first, so a hit marked
in_head means the same value is in the current tree.

Go RE2 and Python differ. The first pass lost 26 patterns to a mid-pattern `(?i)` or `\z`, including one
of generic-api-key's allowlists. The translation moves `(?i)` to the front, which widens a rule slightly,
and takes hits from 33 to 29 because that allowlist now works.

**Numbers.** 7,826 text blobs, 486 MB, 642,483 distinct lines, 69 seconds.

| Rule | Unique hits |
|---|---|
| generic-api-key | 20 |
| gcp-api-key | 9 |

**Triage of all 29, by reading each with the value redacted.** 0 real secrets.

| Class | Hits | What it is |
|---|---|---|
| Google's own browser keys | 9 | One saved developers.google.com page from P-0246. My 12 shapes caught all 9 |
| Public chain addresses | 10 | Solana mint and freeze authorities (P-0042, P-0099, F-0011) |
| Saved public x402 listing | 5 | A third party's public discovery file. One is the USDC contract address; the other four I classed by the file, not value by value |
| Saved public web pages | 3 | Tokens in pages fetched for P-0027 (Wikipedia, GitHub). Not ours |
| Code or prose | 2 | An expression in bias_check.py, a URL parameter in REFILL-SOURCES.md |

So gitleaks caught 20 things my 12 shapes did not, and every one of them was a false alarm: 20 of 20 for
the generic rule. No hit exists only in history; all 29 values are in the current tree.

**What I did not do.** 116 blobs over 2 MB were not scanned (25 binary skipped, 557 path-allowlisted). 603
very long lines were scanned only in 800-character windows around a keyword. Untracked files were not
scanned. The triage is my reading of redacted context, not a check against any provider.

**Values.** results.json holds rule, path, line, length and entropy only. The redacted context file is in
`sandbox/gitleaks-scan/`, which is gitignored.
