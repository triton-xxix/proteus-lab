# P-0055: keyless Reddit feeds from this Mac, 2 Oct 2026

Python urllib, no login, two user agents (browser string and an honest script string). Results in
`results.json` (burst) and `results-slow.json` (after a 60 s cool-off, 10 s apart).

- `www.reddit.com/r/solana/.rss`: 200, Atom, 25 entries, 93 KB. Same with either user agent.
- `old.reddit.com/r/solana/.rss`: 200 but an HTML "Welcome to Reddit" page, not a feed.
- `/r/solana/new.json`: 403 "Blocked" with either user agent. The JSON route is closed keyless.
- Search RSS and thread RSS: 429 in the burst. After the cool-off the subreddit feed returned 200
  with headers `x-ratelimit-used 1`, `remaining 0.0`, `reset 43`; the next three thread feeds,
  10 s apart, all drew 429 with the reset counting down 32, 21, 11.

Verdict: works, narrowly. Keyless RSS returns real text, but the budget is about one request per
rolling minute per IP. Enough for one subreddit feed a minute (a poller), not for opening
threads in a run. Agent browsers still refuse reddit.com; plain HTTP does not.
