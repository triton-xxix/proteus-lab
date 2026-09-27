# Usage

What Proteus costs in Claude, in tokens, rebuilt every Sunday by `bin/usage.py` from the
session transcripts on this Mac. Never typed by hand.

What it cannot see: sessions on other machines or in other folders, and anything before the
transcripts on disk. Interactive sessions are labelled "interactive (Luke)" and kept apart
from the scheduled runs, so the nightly is not blamed for them. A session resumed later is
split at each prompt, so one transcript can be two rows. Wall time is active time, gaps
capped at 10 minutes. Times and weeks are UTC. No pounds figure yet: it waits until list
prices are checked, not remembered.

Rebuilt 2026-09-27 20:16.

## By month

| Month | Who | Output | Cache reads | Cache writes | Uncached input |
|---|---|---|---|---|---|
| 2026-09 | scheduled runs | 172.9k | 32.27M | 762.7k | 646 |
| 2026-09 | Luke's sessions | 1.01M | 109.34M | 4.56M | 14.4k |

## Scheduled output by ISO week

The charter's alarm: a week more than double the trailing four-week average is named in
Field Notes with the step that caused it.

| Week | Runs | Output | Trailing 4-week average | Over double? |
|---|---|---|---|---|
| 2026-W39 | 7 | 172.9k | n/a | n/a |

## By session

| Start (UTC) | Task | Model | Output | Cache reads | Cache writes | Uncached input | Active time | Session |
|---|---|---|---|---|---|---|---|---|
| 2026-09-21 23:08 | interactive (Luke) | fable-5-1 | 156.9k | 18.41M | 652.7k | 2.1k | 134 min | 103415eb |
| 2026-09-21 23:09 | interactive (Luke), child ac10ec09 | opus-5 | 19.5k | 2.38M | 179.6k | 42 | 3 min | 103415eb |
| 2026-09-21 23:09 | interactive (Luke), child a2efb19f | opus-5 | 22.2k | 2.39M | 133.4k | 54 | 4 min | 103415eb |
| 2026-09-22 01:25 | interactive (Luke) | fable-5-1 | 112.6k | 4.33M | 627.9k | 666 | 61 min | c4756eff |
| 2026-09-22 01:27 | nightly | opus-5 | 25.9k | 5.44M | 81.1k | 124 | 16 min | e0b140bc |
| 2026-09-22 01:44 | interactive (Luke) | opus-5 | 27.5k | 3.71M | 39.0k | 52 | 19 min | e0b140bc |
| 2026-09-22 22:23 | nightly | opus-5-5 | 11.8k | 2.75M | 68.1k | 70 | 5 min | 0279d1fb |
| 2026-09-23 22:24 | nightly | opus-5-5 | 7.6k | 1.83M | 51.5k | 54 | 14 min | 5c33015e |
| 2026-09-24 01:48 | interactive (Luke) | opus-5-5 | 14.1k | 1.88M | 83.4k | 36 | 3 min | 5c33015e |
| 2026-09-24 07:21 | interactive (Luke) | fable-5-1 | 1.7k | 169.0k | 31.3k | 66 | 0 min | 383d8034 |
| 2026-09-24 07:23 | interactive (Luke) | fable-5-1 | 30.0k | 1.64M | 88.5k | 424 | 27 min | 12ac3230 |
| 2026-09-24 07:24 | interactive (Luke) | fable-5-1 | 1.6k | 176.7k | 31.5k | 66 | 0 min | 437d8fcf |
| 2026-09-24 07:24 | interactive (Luke) | fable-5-1 | 58.0k | 5.17M | 153.2k | 972 | 35 min | 4e5425b0 |
| 2026-09-24 07:27 | interactive (Luke) | fable-5-1 | 68.0k | 5.83M | 151.3k | 1.2k | 37 min | 7b8d0e87 |
| 2026-09-24 07:28 | interactive (Luke) | fable-5-1 | 61.8k | 4.73M | 133.7k | 944 | 46 min | 4ce91b97 |
| 2026-09-24 07:30 | interactive (Luke), child a31535c2 | haiku-4-5-20251001 | 5.6k | 299.7k | 55.9k | 74 | 2 min | 7b8d0e87 |
| 2026-09-24 07:32 | interactive (Luke), child a1839ba6 | fable-5-1 | 2.6k | 584.1k | 55.1k | 354 | 0 min | 7b8d0e87 |
| 2026-09-24 08:06 | interactive (Luke) | fable-5-1 | 65.3k | 5.39M | 202.4k | 810 | 15 min | acf2e2c2 |
| 2026-09-24 08:12 | interactive (Luke) | fable-5-1 | 81.9k | 8.99M | 181.2k | 1.7k | 26 min | 98ab5348 |
| 2026-09-24 08:13 | interactive (Luke) | fable-5-1 | 44.8k | 5.37M | 108.4k | 1.5k | 20 min | b750de9f |
| 2026-09-24 22:23 | nightly | opus-5-5 | 25.7k | 4.25M | 110.1k | 86 | 19 min | 185ebb06 |
| 2026-09-25 06:31 | interactive (Luke) | opus-5-5 | 73.4k | 10.35M | 661.3k | 98 | 55 min | 185ebb06 |
| 2026-09-25 07:01 | interactive (Luke) | fable-5-1 | 4.6k | 315.7k | 40.0k | 130 | 1 min | 1f2daa73 |
| 2026-09-25 22:23 | nightly | opus-5-5 | 28.9k | 5.10M | 119.6k | 96 | 11 min | 37174eed |
| 2026-09-26 10:04 | interactive (Luke) | fable-5-1 | 76.9k | 13.70M | 424.7k | 2.3k | 35 min | fe2c2b8b |
| 2026-09-26 10:15 | interactive (Luke), child a7020cd9 | sonnet-5 | 12.2k | 960.5k | 103.4k | 24 | 5 min | fe2c2b8b |
| 2026-09-26 19:56 | interactive (Luke) | fable-5-1 | 25.1k | 2.10M | 72.6k | 614 | 14 min | 6dd42555 |
| 2026-09-26 22:23 | nightly | opus-5-5 | 40.9k | 10.80M | 156.7k | 170 | 31 min | a0ef9751 |
| 2026-09-26 22:31 | nightly, child ab819663 | sonnet-5 | 17.4k | 128.6k | 89.3k | 6 | 3 min | a0ef9751 |
| 2026-09-27 10:08 | interactive (Luke) | opus-5-5 | 17.2k | 6.17M | 186.9k | 60 | 27 min | a0ef9751 |
| 2026-09-27 17:00 | weekly | opus-5-5 | 14.6k | 1.97M | 86.3k | 40 | 12 min | 7ec7c6f0 |
| 2026-09-27 18:34 | interactive (Luke) | opus-5-5 | 30.8k | 4.29M | 159.4k | 54 | 24 min | 7ec7c6f0 |
