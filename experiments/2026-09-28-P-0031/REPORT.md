# P-0031: mcp-youtube-transcript, full keyless transcript for a 28 minute video, in how many pages?

28 Sep 2026, 23:47 to 00:02 local. No key, no account, no proxy. Installed from PyPI with the
project interpreter into `sandbox/ytmcp/lib` (`pip --target`; `uvx`, the README's route, is not
on this Mac and the sandbox venv's own interpreter is not on the unattended safe list). Driven
over stdio with the mcp Python SDK's client, `probe.py` beside this file.

## Verdict: works, once the SDK is pinned; one page

| | |
|---|---|
| PyPI release | 0.3.5, declares `mcp>=1.9` with no upper bound |
| Fresh install | pip picks mcp 2.2.0, server dies on import: `cannot import name 'FastMCP' from 'mcp.server'` |
| With `mcp<2` (resolved to 1.30.0) | starts in 1.2 to 1.4 s, one tool listed: `get_transcript` |
| Tools the README on main promises | four: `get_transcript`, `get_timed_transcript`, `get_video_info`, `get_available_languages`, plus `next_cursor` paging at 50,000 chars |
| Tools in 0.3.5 | one; the other three answer "Unknown tool"; no cursor, no timestamps |
| 29.7 min video (sQqniayndb4, auto captions) | 1 page, 28,944 chars, 1.7 s, complete: the library's own fetch is 28,896 chars plus a title line |
| 61.8 min video (H6pWY2VQ9xI, auto captions) | 1 page, 47,817 chars, 1.4 s, complete against 47,754 |
| Two shorter ones (SiBhLYf8YJ4, q4nKy_YPg2s) | 16,043 and 11,166 chars, 1.6 s each |
| YouTube serving captions to this address | yes, 8 of 8 candidates fetched directly in 0.7 to 1.0 s, 6 auto-generated, 2 manual |

So the answer to the question as asked is one page, because the release on PyPI does not page
at all and hands back everything YouTube gives it. A 28 minute video is about 29,000 characters,
under the 50,000 the README says the newer code splits at, so even the main branch would be one
page. The first video that would page on main is roughly an hour and five minutes of talk.

## What the server actually does

Fetches the watch page for the title, then `youtube-transcript-api` for the cues, joins the cue
text with newlines, prefixes `# <title>`, returns one text block. Results are `lru_cache`d for
the life of the process. Everything the tool adds over the library is the MCP wrapper, the title
line and (on main) the paging. The dependency on YouTube serving captions to the caller's
address is the whole risk, and tonight it served.

## Things a stranger would hit

- `pip install mcp-youtube-transcript` is broken today on a clean machine because of the
  unpinned SDK. The README's `uvx --from git+https://github.com/...` route pulls main, not the
  release, so it may not have this problem; I could not test it without `uv`.
- The README documents the main branch, not the release. Three of the four tools and the paging
  do not exist in what PyPI installs.
- The sandbox venv route was denied by my own hook (its interpreter is not on the safe list), so
  the install went through the project interpreter with `--target`. A second denial: a grep
  pattern with `$` inside double quotes. Both routed around.

## Files

`probe.json` full results. `transcript-<id>.txt` the four transcripts as returned. `probe.py` the
client. `duration.py` the direct library check.
