# P-0138: does agent-standup count tokens right?

13 Oct 2026, Trials. Source: harvest H-0238 (github Atoll92/agent-standup, npm @double_geste/agent-standup).

Question: does the tool's per-agent token total for a local Claude Code session match a deduplicated
transcript sum within 5%?

Called shot: broken at 0.50, "output tokens off by more than 5 pct against largest-record dedupe". I
expected it to keep the first streamed record, which `bin/usage.py`'s notes say is a partial count.

## Method

Installed from npm into `sandbox/agent-standup` with `--ignore-scripts`. Read its counting code:
`server.js` lines 364 to 366 keep one usage per `message.id`, overwriting with each later record, so the
last record wins. `compare.py` applies that rule, my rule (largest record per `requestId`) and a
first-record rule to the main transcripts of the 20 most recent Proteus sessions.

## Numbers

- 20 of 20 sessions agree within 5% on all four counts (input, output, cache read, cache write). They
  agree exactly: 2,282,404 output tokens and 551,888,879 input plus cache by both rules.
- The first-record rule also gives 2,282,404. In these 20 transcripts every repeat of a message carries
  identical usage, as the tool's own comment says.

So the tool is right and my shot missed. The bigger lesson is mine: the "first record is a partial
stream count" note behind `bin/usage.py` does not hold on these 20 sessions. Either the format changed
or it applied to files I did not read here. Largest-record dedupe is still safe; it is just not doing
anything on this data.

## Not done

I did not run the tool's server and read its numbers off its page; I applied its quoted rule in Python.
Sub-agent transcripts (in session subfolders) were not read. Its other claims (stuck after one minute,
quiet after three) are untested.
