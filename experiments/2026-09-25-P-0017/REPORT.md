# P-0017: the six missing clubs, and the Wikimedia pageviews rate limit

**Verdict: works.** All six clubs P-0010 lost (Newcastle, Nottingham Forest, Sunderland, Tottenham,
West Ham, Wolves) came back 200 on the first try at a 2-second pace: 6 calls, 16 s, 420 days each.

**Correction to P-0010.** I wrote there that the 429 was "a quota of about 14 per short window, not
a burst limit". Tonight says the opposite. It is a short-window rate limit that clears in seconds:

- Burst of one-day requests at 0.5 s spacing (about 1.4 calls a second with latency): 8 calls fine,
  the 9th refused at 5.6 s with `Retry-After: 31`.
- Waited 15 s, not 31: next call 200. So Retry-After is conservative by at least half.
- At a 2 s pace (about 0.4 calls a second) no refusal in 6 calls. Last night's 1 s pace (about
  0.7 a second) failed at the 15th.

That shape fits a token bucket of roughly 8 to 14 requests refilling somewhere between 0.4 and 0.7 a
second. I have three points, not a curve, so the refill rate is bracketed, not measured. Working rule
for any script here: 2 s between calls, honour Retry-After on a 429.

**P-0010 rerun on all 20 clubs** (805 team-matches, was 569 on 14):

- Precede: r = -0.031 (95% CI -0.099 to +0.039). Still nothing before the match.
- Follow: r = +0.197 (CI +0.129 to +0.262). Down from +0.249 but clearly there.
- Day after: loss x1.26, draw x1.17, win x1.39. Same ordering as before.

Files: `fill.py`, `calls.csv`, `views.csv`, `matches.csv`, `numbers.md`, `window.py`, `window.csv`.
Sixteen calls to Wikimedia in total, one of them refused.
