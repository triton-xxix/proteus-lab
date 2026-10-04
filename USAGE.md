# Usage

What Proteus costs in Claude, in tokens, rebuilt every Sunday by `bin/usage.py` from the
session transcripts on this Mac. Never typed by hand.

What it cannot see: sessions on other machines or in other folders, and anything before the
transcripts on disk. Interactive sessions are labelled "interactive (Luke)" and kept apart
from the scheduled runs, so the nightly is not blamed for them. A session resumed later is
split at each prompt, so one transcript can be two rows. Wall time is active time, gaps
capped at 10 minutes. Times and weeks are UTC. No pounds figure yet: it waits until list
prices are checked, not remembered.

Rebuilt 2026-10-04 18:01.

## By month

| Month | Who | Output | Cache reads | Cache writes | Uncached input |
|---|---|---|---|---|---|
| 2026-09 | scheduled runs | 383.8k | 66.46M | 2.11M | 3.8k |
| 2026-09 | Luke's sessions | 1.54M | 272.43M | 6.54M | 20.6k |
| 2026-10 | scheduled runs | 133.2k | 21.67M | 1.05M | 466 |
| 2026-10 | Luke's sessions | 217.0k | 56.92M | 729.1k | 532 |

## Scheduled output by ISO week

The charter's alarm: a week more than double the trailing four-week average is named in
Field Notes with the step that caused it.

| Week | Runs | Output | Trailing 4-week average | Over double? |
|---|---|---|---|---|
| 2026-W39 | 8 | 221.1k | n/a | n/a |
| 2026-W40 | 7 | 295.9k | 221.1k | no |

## By session

| Start (UTC) | Task | Model | Output | Cache reads | Cache writes | Uncached input | Active time | Session |
|---|---|---|---|---|---|---|---|---|
| 2026-09-21 23:08 | interactive (Luke) | fable-5-1 | 156.9k | 18.41M | 652.7k | 2.1k | 144 min | 103415eb |
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
| 2026-09-26 19:56 | interactive (Luke) | fable-5-1 | 82.1k | 8.24M | 251.3k | 1.6k | 87 min | 6dd42555 |
| 2026-09-26 22:23 | nightly | opus-5-5 | 40.9k | 10.80M | 156.7k | 170 | 31 min | a0ef9751 |
| 2026-09-26 22:31 | nightly, child ab819663 | sonnet-5 | 17.4k | 128.6k | 89.3k | 6 | 3 min | a0ef9751 |
| 2026-09-27 10:08 | interactive (Luke) | opus-5-5 | 17.2k | 6.17M | 186.9k | 60 | 27 min | a0ef9751 |
| 2026-09-27 17:00 | weekly | opus-5-5 | 14.6k | 1.97M | 86.3k | 40 | 12 min | 7ec7c6f0 |
| 2026-09-27 18:34 | interactive (Luke) | opus-5-5 | 54.7k | 9.62M | 406.8k | 104 | 51 min | 7ec7c6f0 |
| 2026-09-27 22:23 | nightly | opus-5-5 | 27.1k | 6.30M | 96.5k | 130 | 17 min | 513b5f2e |
| 2026-09-27 22:31 | nightly, child aa6694f3 | sonnet-5 | 21.1k | 453.8k | 94.9k | 14 | 3 min | 513b5f2e |
| 2026-09-28 22:23 | nightly | fable-5-1 | 78.3k | 14.61M | 210.9k | 2.7k | 37 min | 8fb0ee22 |
| 2026-09-28 22:31 | nightly, child a097c2f1 | sonnet-5-5 | 6.5k | 113.4k | 70.8k | 6 | 0 min | 8fb0ee22 |
| 2026-09-28 23:00 | interactive (Luke) | fable-5-1 | 72.0k | 21.34M | 148.8k | 1.5k | 88 min | 8fb0ee22 |
| 2026-09-28 23:34 | nightly, child ac1a446d | sonnet-5-5 | 352 | 191.7k | 73.0k | 8 | 0 min | 8fb0ee22 |
| 2026-09-29 00:32 | interactive (Luke) | fable-5-1 | 94.8k | 17.39M | 501.1k | 2.9k | 76 min | 5bed9dda |
| 2026-09-29 22:23 | nightly | opus-5-5 | 28.5k | 6.52M | 102.1k | 126 | 31 min | 47045771 |
| 2026-09-29 22:31 | nightly, child a2e04e04 | sonnet-5-5 | 8.4k | 205.8k | 163.3k | 6 | 1 min | 47045771 |
| 2026-09-29 22:33 | nightly, child a9cda104 | sonnet-5-5 | 9.5k | 117.9k | 74.6k | 6 | 1 min | 47045771 |
| 2026-09-30 09:47 | interactive (Luke) | opus-5-5 | 244.8k | 100.46M | 509.7k | 612 | 338 min | 47045771 |
| 2026-09-30 10:26 | nightly, child adcab215 | sonnet-5-5 | 429 | 181.0k | 66.5k | 8 | 0 min | 47045771 |
| 2026-09-30 10:49 | nightly, child a9385873 | sonnet-5-5 | 1.7k | 2.41M | 98.5k | 68 | 5 min | 47045771 |
| 2026-09-30 10:57 | interactive (Luke), child a1784631 | sonnet-5-5 | 145 | 217.9k | 37.5k | 8 | 0 min | 47045771 |
| 2026-09-30 11:25 | interactive (Luke), child a0dc3f59 | sonnet-5-5 | 1.7k | 1.72M | 105.2k | 48 | 6 min | 47045771 |
| 2026-09-30 15:53 | interactive (Luke) | opus-5-5 | 1.3k | 38.6k | 25.7k | 2 | 0 min | 9c2991ee |
| 2026-09-30 22:23 | nightly | opus-5-5 | 12.7k | 2.21M | 82.7k | 50 | 17 min | 171ec545 |
| 2026-09-30 22:40 | nightly, child aa02b0a0 | sonnet-5-5 | 9.1k | 118.4k | 76.1k | 6 | 1 min | 171ec545 |
| 2026-09-30 22:40 | nightly, child a433df43 | sonnet-5-5 | 2.8k | 345.9k | 61.4k | 10 | 0 min | 171ec545 |
| 2026-09-30 22:40 | nightly, child aa5f67d0 | sonnet-5-5 | 2.1k | 203.0k | 39.2k | 8 | 0 min | 171ec545 |
| 2026-09-30 22:41 | nightly, child a8664573 | sonnet-5-5 | 2.5k | 216.8k | 39.3k | 8 | 0 min | 171ec545 |
| 2026-09-30 22:41 | interactive (Luke) | opus-5-5 | 33.4k | 10.45M | 228.3k | 144 | 23 min | 171ec545 |
| 2026-10-01 22:23 | nightly | opus-5-5 | 44.6k | 10.71M | 130.7k | 180 | 43 min | 6f9b3ee7 |
| 2026-10-01 22:44 | nightly, child a9bf776d | sonnet-5-5 | 10.0k | 130.4k | 83.6k | 6 | 1 min | 6f9b3ee7 |
| 2026-10-01 22:44 | nightly, child a3da2f81 | sonnet-5-5 | 2.2k | 171.5k | 46.9k | 6 | 0 min | 6f9b3ee7 |
| 2026-10-01 22:44 | nightly, child a44f48aa | haiku-4-5-20251001 | 3.6k | 262.3k | 59.6k | 50 | 0 min | 6f9b3ee7 |
| 2026-10-01 22:45 | nightly, child ad8a6620 | sonnet-5-5 | 1.9k | 238.8k | 41.2k | 8 | 0 min | 6f9b3ee7 |
| 2026-10-01 23:30 | interactive (Luke) | opus-5-5 | 88.1k | 25.50M | 191.4k | 196 | 78 min | 6f9b3ee7 |
| 2026-10-02 22:23 | nightly | opus-5-5 | 13.9k | 2.44M | 85.7k | 52 | 12 min | f62cb659 |
| 2026-10-02 22:36 | nightly, child aedb0d06 | sonnet-5-5 | 9.2k | 126.7k | 82.0k | 6 | 1 min | f62cb659 |
| 2026-10-02 22:36 | nightly, child aea5318b | sonnet-5-5 | 1.9k | 161.5k | 46.2k | 6 | 0 min | f62cb659 |
| 2026-10-02 22:36 | nightly, child afc9cae3 | sonnet-5-5 | 2.2k | 156.2k | 41.3k | 6 | 0 min | f62cb659 |
| 2026-10-02 22:36 | nightly, child a2efe73e | sonnet-5-5 | 1.8k | 223.3k | 39.8k | 8 | 0 min | f62cb659 |
| 2026-10-02 22:36 | interactive (Luke) | opus-5-5 | 106.8k | 25.48M | 331.1k | 260 | 102 min | f62cb659 |
| 2026-10-03 22:23 | nightly | opus-5-5 | 25.4k | 6.17M | 113.4k | 106 | 16 min | 63453bea |
| 2026-10-03 22:37 | nightly, child a59b0353 | sonnet-5-5 | 9.7k | 124.1k | 79.9k | 6 | 1 min | 63453bea |
| 2026-10-03 22:38 | nightly, child a6ae2768 | sonnet-5-5 | 2.2k | 169.4k | 54.3k | 6 | 0 min | 63453bea |
| 2026-10-03 22:38 | nightly, child a4689c4c | sonnet-5-5 | 1.8k | 182.0k | 66.8k | 6 | 0 min | 63453bea |
| 2026-10-03 22:38 | nightly, child aa76ea8a | sonnet-5-5 | 2.1k | 218.2k | 38.2k | 8 | 0 min | 63453bea |
| 2026-10-03 22:40 | interactive (Luke) | opus-5-5 | 22.1k | 5.94M | 206.6k | 76 | 28 min | 63453bea |
| 2026-10-04 17:01 | weekly | opus-5-5 | 497 | 186.4k | 39.7k | 6 | 0 min | b2e6d592 |
