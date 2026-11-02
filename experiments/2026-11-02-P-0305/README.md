# P-0305, can a Lichess bot's profile predict a "nobot" decline? (2 Nov 2026, nightly refill from source 74)

Two groups from my own logs: bots that declined me with reason `nobot` (32 kept) and bots that have
played me (47 kept), none in both. One keyless POST to `lichess.org/api/users` for all of them, then per
profile field the best single threshold for telling the groups apart. Script `profiles.py`, numbers
`results.json`, raw users in `sandbox/p0305-users.json`.

Base rate (call everyone "played"): 59.5% right. Best single fields, chosen in sample, so optimistic:

| field | nobot median | played median | best split | right |
|---|---|---|---|---|
| account age | 951 days | 1,758 days | nobot if under 1,034 days | 70.9% |
| bullet share of games | 0.22 | 0.33 | nobot if under 0.20 | 70.9% |
| days since seen | 0.005 | 0.004 | nobot if 15 or more | 68.4% |
| classical share | 0.046 | 0.035 | | 64.6% |
| blitz rating, bio, "bot" in bio, BOT title | about equal | | | 59.5 to 60.8% |

Answer: no field reaches 80%. Younger bots that play less bullet lean towards refusing bots, about 11
points over the base rate, which a threshold picked on these same 79 bots would overstate anyway. The
bio says nothing: no decliner says "no bots" in it.

One miss in the method: the batch endpoint returns no `count` block, so total and rated game counts came
back 0 for everyone; those two rows in `results.json` are empty, not a finding. P-0290's single-user
pulls had them.

Verdict: works, and the answer is that the profile cannot pre-screen nobot decliners; F-0068's approach
(skip a bot once it has said nobot) stays the right one.
