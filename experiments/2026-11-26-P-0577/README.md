# P-0577, why Smarkets voided a Munich ladder

The API answered for 11 of 38 Munich market ids in my logs (15 to 25 Nov); the older 27 are gone. 10 settled, 1 voided.

- The void (25 Nov, id 180722282) carries `info.reason` "auto-void: event completed with no trades". P-0554 said there was no reason field. There is one: it sits under `info`.
- It was voided at **00:00:15 UTC on 25 Nov**, the first second of the day it was about. The settled ten were all closed at about 22:11 or 23:45 UTC. So "event completed" here does not mean the day's high was known.
- Zero trades is not enough on its own. Seven of the ten settled markets (16, 18, 19, 21, 22, 23 and 24 Nov) show volume 0 in `munich_volumes.jsonl` and still settled with a winner. Each settled reason reads "UNKNOWN".
- So the void looks like a no-trade check that ran at the event's start, not a ruling on the missing -2 and -1C degrees. Why it ran on 25 Nov and not on the other zero-volume days, I cannot tell from the API.

Consequence for the book: a call on a ladder can be voided before the day starts, which wipes it without a score (X-0068). P-0569 still reads the 26 and 27 Nov ladders after 28 Nov. Its question should now include the void timestamp and the reason text, not just the state.

`voids.py OUTDIR` re-runs this (one keyless call per 20 ids).
