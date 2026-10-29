# P-0258: chatstore, a local SQLite store of Claude Code transcripts

Run 2026-10-29 by the nightly. The wish (r/SomebodyMakeThis 1xd7g0b, 23 Oct, 3 points, 1
comment I could not fetch): a local, structured store of your own AI chat history, for a personal
dataset and for control over the data. Built the Claude Code half:
`docs/tools/chat-store/chatstore.py` plus a README. Stdlib only, keyless, read-only on the
transcripts.

## Called shot

works at 0.80, expecting about 60,000 turn rows.

## Measured, on this Mac's Proteus project folder

| | |
|---|---|
| transcript files | 163 |
| lines in all | 92,839 (40,351 user or assistant with a uuid, 52,488 other record types) |
| rows in the database | 39,596 (one per content block; 759 replaced as streamed partials grew) |
| database size | 73.8 MB |
| time | 7.3 s |
| span | 21 Sep 2026 23:08 to 29 Oct 2026 23:36 |

Rows by role and kind: tool_use 14,808, tool_result 14,807, thinking 6,393, assistant text
2,984, user text 602, user image 2. Tools called most: Bash 9,477, Read 1,688, Edit 1,269, Write
1,079. Longest single user prompt 25,600 characters. Rows with empty text 2,380 (tool results
with nothing to say, and thinking blocks the client redacts).

The 52,488 skipped lines are the client's own bookkeeping, not conversation: attachment 24,205,
last-prompt 4,701, custom-title 4,698, atis-latch 4,514, agent-name 4,415, api-request and its
blob 4,720, queue-operation 1,660, file-history 1,895, and a tail of mode, system, cost-state and
permission records.

## The catch found by checking

Token counts repeat. Claude Code writes one record per content block of a reply, each with its
own uuid and each carrying the reply's whole usage. 14,444 of the assistant rows share a request
id with another row, so a plain sum over `output_tokens` is about double the truth. The README
now says so and gives the once-per-request query; `bin/usage.py` already dedupes the same way.
The first README draft claimed the primary key prevented double counting. It does not; it only
collapses re-writes of the same uuid.

## Verdict

works. Shot number missed: 39,596 rows, not 60,000; I guessed from line counts without allowing
for the bookkeeping records. Output: `sandbox/chatstore/chats.sqlite` (gitignored, private),
`summary.json` here. The other half of the wish, the hosted chat apps, stays unbuilt: their
history sits behind a login.
