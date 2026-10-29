# chatstore

Turn your Claude Code transcripts into one SQLite file you own.

Someone on r/SomebodyMakeThis asked for a local, structured store of their own AI chat
history: a personal dataset for later, and control over the data now. This is the Claude Code
half of that wish. Claude Code already writes every session to disk as JSONL under
`~/.claude/projects/<project>/<session>.jsonl`; this script reads those files and writes a
database with one row per content block (text, thinking, tool call, tool result), with the
model, the timestamp, the parent turn and the token counts.

## Use

```
python3 chatstore.py --out chats.sqlite ~/.claude/projects/-Users-me-myproject
python3 chatstore.py --out chats.sqlite --summary summary.json ~/.claude/projects/*
```

Keyless, standard library only, read-only on the transcripts. Re-running updates rows in place,
so you can run it nightly against the same file.

## Tables

- `sessions`: session id, file path, project folder, first and last timestamp, record and row counts.
- `turns`: `uuid`, `block_index`, `session_id`, `parent_uuid`, `ts`, `role`, `kind`, `model`, `text`,
  `tool_name`, `tool_use_id`, the four token counts (on the first block of each assistant turn),
  `request_id`.

Some queries:

```
-- everything you typed, in order
SELECT ts, text FROM turns WHERE role='user' AND kind='text' ORDER BY ts;
-- which tools the assistant calls most
SELECT tool_name, COUNT(*) FROM turns WHERE kind='tool_use' GROUP BY 1 ORDER BY 2 DESC;
-- output tokens per model, counted once per API request
SELECT model, SUM(o) FROM (
  SELECT model, request_id, MAX(output_tokens) AS o FROM turns
  WHERE request_id IS NOT NULL GROUP BY request_id) GROUP BY 1;
```

## Mind

The database holds every prompt and every answer in plain text, tool inputs and outputs
included. Keep it out of any public repository and off any shared drive.

Token counts repeat. Claude Code writes one record per content block of an assistant reply
(thinking, text, tool call), each with its own uuid and each carrying the whole reply's usage,
and a streamed reply is re-written as it grows. So never `SUM(output_tokens)` straight off the
table: group by `request_id` and take the max, as the query above does. On the first run here
14,444 of 24,000 assistant rows shared a request id with another row.

## What it does not do

Other chat apps (ChatGPT, Gemini, Meta) keep their history behind a login; they are not read
here. Only the files Claude Code writes locally.

Built by Proteus, 29 October 2026, probe P-0258. Measured on this Mac's own transcripts the first
night: see `experiments/2026-10-29-P-0258/REPORT.md` in the proteus-lab repository.
