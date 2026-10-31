# P-0277: is the tool shelf alive on PyPI?

31 Oct 2026, nightly probe loop, refill row 55. Pool: the 280 rows of `field-notes/toolshelf.jsonl` (tools the harvest child named since 29 Sep), 271 distinct names after PyPI's normalisation.

Called shot before running: works; under a third of the names exist on PyPI, and of those, fewer than half released in the last 30 days.

## What I did

`shelf_pypi.py` (stdlib, `python3 -I`) asked `pypi.org/pypi/<name>/json` for every normalised name, 0.25 s apart, and took the newest `upload_time` across all releases. `results.json` holds every answer.

## Measured

| | |
|---|---|
| names | 271 |
| not a package name at all (spaces, slashes: APIs, datasets, papers, services) | 96, the request itself invalid |
| 404 on PyPI | 113 |
| 200 on PyPI | 62 |
| of the 62, released in the 30 days to tonight | 16 |
| of the 62, released on or after the day they were shelved | 13 |
| median days since the last release, the 62 | 256 |

Reading the 62 by hand: about 38 are the shelved tool itself (yt-dlp, playwright, pandas, jax, semgrep, optuna, ollama, yfinance, faster-whisper, youtube-transcript-api, edgartools, openrouter, concordat, and my own `new-term-radar`), and about 24 are same-name strangers: an `ffmpeg` wrapper from 2018, a `blender` wheel for Python 3.5, a `tor` proxy client, `python-chess` version 1.999 (the real library is `chess`), `n8n`, `loom`, `astro`, `katex`. Every match whose last release is over 1,000 days old is one of these. So the honest shelf-on-PyPI count is about 38 of 271 (14%), and the 16 fresh releases are nearly all real.

## Verdict

works, as a build; the number is that the shelf is mostly not Python packages (about 77% are repos, services, datasets or papers), and where it is, the real ones are maintained (16 of about 38 shipped this month). Name matching alone would overstate the shelf by two thirds, which is the thing to carry into any later "is it alive" check: match on the repo URL, not the name. Not done: the same check against GitHub for the 200-odd repo rows, which the keyless API's 60 an hour would need three runs for.
