# P-0009: TfL unified API, no key

`/Line/victoria/Arrivals`: HTTP 200 in 0.27s, 286 predictions.

| station | platform | towards | seconds |
|---|---|---|---|
| Blackhorse Road Underground Station | Northbound - Platform 1 | Walthamstow Central | 22 |
| Blackhorse Road Underground Station | Southbound - Platform 2 | Brixton | 23 |
| Brixton Underground Station | Northbound - Platform 1 | Walthamstow Central | 23 |
| Finsbury Park Underground Station | Northbound - Platform 2 | Walthamstow Central | 24 |
| Highbury & Islington Underground Station | Southbound - Platform 5 | Brixton | 25 |
| Green Park Underground Station | Southbound - Platform 4 | Brixton | 25 |
| Pimlico Underground Station | Northbound - Platform 1 | Walthamstow Central | 26 |
| King's Cross St. Pancras Underground Station | Northbound - Platform 3 | Walthamstow Central | 26 |

`/Line/Mode/tube/Status`: HTTP 200 in 0.08s. Bakerloo: Good Service; Central: Severe Delays; Circle: Good Service; District: Minor Delays; Hammersmith & City: Good Service; Jubilee: Minor Delays; Metropolitan: Good Service; Northern: Minor Delays; Piccadilly: Good Service; Victoria: Minor Delays; Waterloo & City: Good Service
Rate headers on a normal reply: none

Burst: 49 calls in 12.0s, codes [200, 429], mean 0.24s, max 0.99s.
Throttled at call 49 after 12.0s, headers {'Retry-After': '48'}.

## What this says

- Fully keyless for reads: live arrivals for a whole line (286 predictions in 0.27 s) and the status of every tube line (0.08 s), no headers asking for a key.
- The anonymous limit is about 48 calls a minute: the 49th call inside 12 seconds drew a 429 with `Retry-After: 48`, and no rate headers are sent before that. A poller that takes one arrivals call per line every 15 seconds (44 a minute for eleven lines) sits just under it; an app key (free registration) lifts it to the documented 500 a minute.
- Verdict: works. Nothing to ask for unless a poller needs more than 48 a minute.
