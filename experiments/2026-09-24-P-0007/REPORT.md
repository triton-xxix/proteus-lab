# P-0007: Metaculus API without an account

`/api/posts/` open binary, 20 newest by hotness: HTTP 403 in 0.40s. Rate headers: none
Returned 0 posts. Fields on a post: n/a

| id | title | closes | community p | forecasters |
|---|---|---|---|---|

Community forecast present on 0 of 0 without any login.

429 at call 9 after 1.9s; headers {'Retry-After': '10'}

Burst: 9 calls in 1.9s, codes [403, 429], mean 0.21s per call, max 0.39s.


## What this says

- Every listing endpoint (`/api/posts/`, `/api/questions/`, the older `/api2/questions/`) answers 403 with the same body, with a plain and a browser user agent: "The API is only available to authenticated users. Please create an account and use your API token to access the API." No keyless read of open questions or community forecasts exists any more.
- One number came out anyway: the throttle sits in front of the auth check. Nine calls in 1.9 seconds drew a 429 with `Retry-After: 10`, so the public-side limit is on the order of a few calls a second, before any token.
- Verdict: blocked, on a Metaculus account and its API token. The ask is already on the persona's one-click list; nothing new to ask for. If the account arrives, the token goes in 1Password tagged `proteus` and this probe reruns unchanged with an `Authorization: Token` header.
