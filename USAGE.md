# Usage

What Proteus costs in Claude, in tokens, rebuilt every Sunday by `bin/usage.py` from the
session transcripts on this Mac. Never typed by hand.

What it cannot see: sessions on other machines or in other folders, and anything before the
transcripts on disk. Interactive sessions are labelled "interactive (Luke)" and kept apart
from the scheduled runs, so the nightly is not blamed for them. A session resumed later is
split at each prompt, so one transcript can be two rows. Wall time is active time, gaps
capped at 10 minutes. Times and weeks are UTC. No pounds figure yet: it waits until list
prices are checked, not remembered.

Rebuilt 2026-10-27 09:07.

## By month

| Month | Who | Output | Cache reads | Cache writes | Uncached input |
|---|---|---|---|---|---|
| 2026-09 | scheduled runs | 413.4k | 75.71M | 2.18M | 3.9k |
| 2026-09 | Luke's sessions | 1.52M | 263.86M | 6.81M | 20.7k |
| 2026-10 | scheduled runs | 3.12M | 736.55M | 17.99M | 30.9k |
| 2026-10 | Luke's sessions | 2.75M | 646.59M | 17.72M | 20.0k |

## Scheduled output by ISO week

The charter's alarm: a week more than double the trailing four-week average is named in
Field Notes with the step that caused it.

| Week | Runs | Output | Trailing 4-week average | Over double? |
|---|---|---|---|---|
| 2026-W39 | 8 | 221.1k | n/a | n/a |
| 2026-W40 | 8 | 423.7k | 221.1k | no |
| 2026-W41 | 11 | 637.1k | 322.4k | no |
| 2026-W42 | 39 | 913.6k | 427.3k | YES |
| 2026-W43 | 42 | 1.20M | 548.9k | YES |
| 2026-W44 | 8 | 138.6k | 793.6k | no |

## By session

| Start (UTC) | Task | Model | Output | Cache reads | Cache writes | Uncached input | Active time | Session |
|---|---|---|---|---|---|---|---|---|
| 2026-09-21 23:08 | interactive (Luke) | fable-5-1 | 156.9k | 18.41M | 652.7k | 2.1k | 144 min | 103415eb |
| 2026-09-21 23:09 | interactive (Luke), child ac10ec09 | opus-5 | 19.5k | 2.38M | 179.6k | 42 | 3 min | 103415eb |
| 2026-09-21 23:09 | interactive (Luke), child a2efb19f | opus-5 | 22.2k | 2.39M | 133.4k | 54 | 4 min | 103415eb |
| 2026-09-22 01:25 | interactive (Luke) | fable-5-1 | 114.0k | 4.73M | 950.3k | 700 | 71 min | c4756eff |
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
| 2026-09-24 07:28 | interactive (Luke) | fable-5-1 | 75.3k | 6.21M | 310.8k | 1.1k | 61 min | 4ce91b97 |
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
| 2026-09-30 22:23 | nightly | opus-5-5 | 42.3k | 11.45M | 151.2k | 180 | 34 min | 171ec545 |
| 2026-09-30 22:40 | nightly, child aa02b0a0 | sonnet-5-5 | 9.1k | 118.4k | 76.1k | 6 | 1 min | 171ec545 |
| 2026-09-30 22:40 | nightly, child a433df43 | sonnet-5-5 | 2.8k | 345.9k | 61.4k | 10 | 0 min | 171ec545 |
| 2026-09-30 22:40 | nightly, child aa5f67d0 | sonnet-5-5 | 2.1k | 203.0k | 39.2k | 8 | 0 min | 171ec545 |
| 2026-09-30 22:41 | nightly, child a8664573 | sonnet-5-5 | 2.5k | 216.8k | 39.3k | 8 | 0 min | 171ec545 |
| 2026-10-01 01:37 | interactive (Luke) | opus-5-5 | 3.9k | 1.20M | 159.8k | 14 | 6 min | 171ec545 |
| 2026-10-01 22:23 | nightly | opus-5-5 | 44.6k | 10.71M | 130.7k | 180 | 43 min | 6f9b3ee7 |
| 2026-10-01 22:44 | nightly, child a9bf776d | sonnet-5-5 | 10.0k | 130.4k | 83.6k | 6 | 1 min | 6f9b3ee7 |
| 2026-10-01 22:44 | nightly, child a3da2f81 | sonnet-5-5 | 2.2k | 171.5k | 46.9k | 6 | 0 min | 6f9b3ee7 |
| 2026-10-01 22:44 | nightly, child a44f48aa | haiku-4-5-20251001 | 3.6k | 262.3k | 59.6k | 50 | 0 min | 6f9b3ee7 |
| 2026-10-01 22:45 | nightly, child ad8a6620 | sonnet-5-5 | 1.9k | 238.8k | 41.2k | 8 | 0 min | 6f9b3ee7 |
| 2026-10-01 23:30 | interactive (Luke) | opus-5-5 | 88.1k | 25.50M | 191.4k | 196 | 78 min | 6f9b3ee7 |
| 2026-10-02 22:23 | nightly | opus-5-5 | 32.1k | 9.14M | 127.7k | 156 | 37 min | f62cb659 |
| 2026-10-02 22:36 | nightly, child aedb0d06 | sonnet-5-5 | 9.2k | 126.7k | 82.0k | 6 | 1 min | f62cb659 |
| 2026-10-02 22:36 | nightly, child aea5318b | sonnet-5-5 | 1.9k | 161.5k | 46.2k | 6 | 0 min | f62cb659 |
| 2026-10-02 22:36 | nightly, child afc9cae3 | sonnet-5-5 | 2.2k | 156.2k | 41.3k | 6 | 0 min | f62cb659 |
| 2026-10-02 22:36 | nightly, child a2efe73e | sonnet-5-5 | 1.8k | 223.3k | 39.8k | 8 | 0 min | f62cb659 |
| 2026-10-03 10:21 | interactive (Luke) | opus-5-5 | 88.5k | 18.78M | 289.1k | 156 | 77 min | f62cb659 |
| 2026-10-03 22:23 | nightly | opus-5-5 | 40.4k | 11.31M | 145.9k | 172 | 33 min | 63453bea |
| 2026-10-03 22:37 | nightly, child a59b0353 | sonnet-5-5 | 9.7k | 124.1k | 79.9k | 6 | 1 min | 63453bea |
| 2026-10-03 22:38 | nightly, child a6ae2768 | sonnet-5-5 | 2.2k | 169.4k | 54.3k | 6 | 0 min | 63453bea |
| 2026-10-03 22:38 | nightly, child a4689c4c | sonnet-5-5 | 1.8k | 182.0k | 66.8k | 6 | 0 min | 63453bea |
| 2026-10-03 22:38 | nightly, child aa76ea8a | sonnet-5-5 | 2.1k | 218.2k | 38.2k | 8 | 0 min | 63453bea |
| 2026-10-03 23:38 | interactive (Luke) | opus-5-5 | 7.1k | 798.3k | 174.1k | 10 | 11 min | 63453bea |
| 2026-10-04 17:01 | weekly | opus-5-5 | 15.1k | 2.65M | 106.2k | 48 | 12 min | b2e6d592 |
| 2026-10-04 22:23 | nightly | opus-5-5 | 35.9k | 12.10M | 146.3k | 178 | 39 min | bddbc704 |
| 2026-10-04 22:37 | nightly, child aede3e7d | sonnet-5-5 | 8.1k | 124.3k | 78.6k | 6 | 1 min | bddbc704 |
| 2026-10-04 22:37 | nightly, child adba122c | sonnet-5-5 | 2.2k | 158.0k | 43.2k | 6 | 0 min | bddbc704 |
| 2026-10-04 22:37 | nightly, child afa42e50 | sonnet-5-5 | 2.1k | 171.3k | 56.2k | 6 | 0 min | bddbc704 |
| 2026-10-04 22:45 | nightly, child acd64c37 | sonnet-5-5 | 1.9k | 197.7k | 74.2k | 8 | 0 min | bddbc704 |
| 2026-10-05 09:05 | interactive (Luke) | opus-5-5 | 1.3k | 647.0k | 114.1k | 10 | 2 min | b2e6d592 |
| 2026-10-05 09:24 | interactive (Luke) | opus-5-5 | 5.4k | 1.59M | 154.6k | 18 | 1 min | bddbc704 |
| 2026-10-05 22:23 | nightly | opus-5-5 | 35.2k | 11.77M | 150.9k | 174 | 44 min | c6121fab |
| 2026-10-05 22:49 | nightly, child aed54385 | sonnet-5-5 | 7.8k | 122.6k | 76.5k | 6 | 0 min | c6121fab |
| 2026-10-05 22:49 | nightly, child a8208942 | sonnet-5-5 | 2.4k | 161.8k | 46.9k | 6 | 0 min | c6121fab |
| 2026-10-05 22:49 | nightly, child a8f9408e | sonnet-5-5 | 2.1k | 178.3k | 63.1k | 6 | 0 min | c6121fab |
| 2026-10-05 22:49 | nightly, child a98cfc95 | sonnet-5-5 | 2.4k | 228.5k | 43.8k | 8 | 0 min | c6121fab |
| 2026-10-06 17:43 | interactive (Luke) | opus-5-5 | 56.0k | 17.78M | 463.3k | 138 | 27 min | c6121fab |
| 2026-10-06 22:23 | nightly | opus-5-5 | 44.0k | 16.34M | 177.2k | 224 | 62 min | e91a3bbf |
| 2026-10-06 22:38 | nightly, child a1b21ed5 | sonnet-5-5 | 8.7k | 124.5k | 78.9k | 6 | 1 min | e91a3bbf |
| 2026-10-06 22:38 | nightly, child a4463024 | sonnet-5-5 | 2.3k | 224.7k | 40.8k | 8 | 0 min | e91a3bbf |
| 2026-10-06 22:41 | interactive (Luke) | opus-5-5 | 140.9k | 46.39M | 339.0k | 354 | 85 min | b7f7f126 |
| 2026-10-06 23:29 | interactive (Luke) | opus-5-5 | 8.7k | 939.1k | 206.1k | 10 | 11 min | e91a3bbf |
| 2026-10-07 00:44 | interactive (Luke) | opus-5-5 | 254.4k | 57.55M | 496.0k | 382 | 120 min | d8107278 |
| 2026-10-07 01:45 | interactive (Luke) | fable-5-1 | 338.4k | 46.50M | 2.07M | 2.6k | 130 min | 5e0288f2 |
| 2026-10-07 01:46 | interactive (Luke), child a0b6f3f9 | opus-5-5 | 7.1k | 613.9k | 86.5k | 20 | 1 min | 5e0288f2 |
| 2026-10-07 01:46 | interactive (Luke), child a289ae60 | opus-5-5 | 4.4k | 774.1k | 107.8k | 22 | 1 min | 5e0288f2 |
| 2026-10-07 01:46 | interactive (Luke), child ab964141 | opus-5-5 | 9.0k | 1.36M | 97.2k | 38 | 2 min | 5e0288f2 |
| 2026-10-07 02:05 | interactive (Luke), child a28044a3 | fable-5-1 | 57.9k | 623.0k | 348.1k | 226 | 14 min | 5e0288f2 |
| 2026-10-07 02:05 | interactive (Luke), child aaad971a | fable-5-1 | 19.2k | 682.7k | 178.0k | 194 | 9 min | 5e0288f2 |
| 2026-10-07 02:05 | interactive (Luke), child ade73eb0 | fable-5-1 | 18.0k | 385.0k | 139.8k | 162 | 7 min | 5e0288f2 |
| 2026-10-07 02:06 | interactive (Luke) | fable-5-1 | 339.9k | 78.40M | 1.36M | 3.8k | 155 min | 0c4f1de5 |
| 2026-10-07 02:06 | interactive (Luke), child a1905e76 | opus-5-5 | 11.9k | 3.33M | 155.7k | 60 | 8 min | 0c4f1de5 |
| 2026-10-07 02:06 | interactive (Luke), child a2800ea7 | opus-5-5 | 16.6k | 6.69M | 237.2k | 80 | 9 min | 0c4f1de5 |
| 2026-10-07 02:06 | interactive (Luke), child a362629c | opus-5-5 | 15.0k | 2.76M | 198.4k | 46 | 7 min | 0c4f1de5 |
| 2026-10-07 02:11 | interactive (Luke), child a6779608 | sonnet-5-5 | 1.7k | 906.9k | 164.1k | 18 | 7 min | d8107278 |
| 2026-10-07 02:11 | interactive (Luke), child a930cd38 | sonnet-5-5 | 2.1k | 2.11M | 209.5k | 32 | 8 min | d8107278 |
| 2026-10-07 02:11 | interactive (Luke), child aa6ec45c | sonnet-5-5 | 555 | 939.4k | 130.3k | 20 | 5 min | d8107278 |
| 2026-10-07 02:16 | interactive (Luke), child a3553afb | sonnet-5-5 | 14.1k | 1.41M | 336.1k | 26 | 8 min | d8107278 |
| 2026-10-07 18:25 | interactive (Luke) | fable-5-1 | 73.2k | 7.34M | 347.9k | 1.5k | 41 min | 5184af27 |
| 2026-10-07 19:41 | interactive (Luke) | fable-5-1 | 6.8k | 355.7k | 36.7k | 130 | 1 min | 37d8101f |
| 2026-10-07 22:23 | nightly | fable-5-1 | 103.3k | 24.25M | 288.3k | 3.2k | 45 min | 9fb93396 |
| 2026-10-07 22:38 | nightly, child a948a6fe | sonnet-5-5 | 9.3k | 204.3k | 79.7k | 8 | 1 min | 9fb93396 |
| 2026-10-07 22:38 | nightly, child a5943efe | sonnet-5-5 | 8.6k | 410.5k | 43.1k | 14 | 2 min | 9fb93396 |
| 2026-10-07 22:42 | nightly, child a7cd1b58 | sonnet-5-5 | 2.3k | 226.2k | 41.5k | 8 | 0 min | 9fb93396 |
| 2026-10-07 23:09 | interactive (Luke) | fable-5-1 | 52.0k | 13.43M | 115.3k | 1.0k | 42 min | 9fb93396 |
| 2026-10-07 23:42 | interactive (Luke) | opus-5-5 | 152.9k | 38.97M | 865.1k | 298 | 98 min | 0ef509ad |
| 2026-10-07 23:43 | interactive (Luke), child a99dc27d | opus-5-5 | 6.6k | 702.4k | 175.9k | 22 | 13 min | 0ef509ad |
| 2026-10-07 23:43 | interactive (Luke), child ab3c4163 | opus-5-5 | 631 | 2.56M | 279.6k | 54 | 23 min | 0ef509ad |
| 2026-10-07 23:43 | interactive (Luke), child afae578e | opus-5-5 | 10.6k | 2.06M | 192.1k | 58 | 14 min | 0ef509ad |
| 2026-10-08 13:50 | interactive (Luke) | opus-5-5 | 12.8k | 2.67M | 58.0k | 62 | 24 min | b950d71b |
| 2026-10-08 22:24 | nightly | opus-5-5 | 55.7k | 18.72M | 177.0k | 246 | 48 min | 315fdc5b |
| 2026-10-08 22:37 | nightly, child a8ca08af | sonnet-5-5 | 8.2k | 129.2k | 80.9k | 6 | 1 min | 315fdc5b |
| 2026-10-08 22:37 | nightly, child a67f03d3 | sonnet-5-5 | 2.8k | 205.4k | 79.2k | 8 | 0 min | 315fdc5b |
| 2026-10-08 22:37 | nightly, child ac59793a | sonnet-5-5 | 8.6k | 448.4k | 48.8k | 14 | 1 min | 315fdc5b |
| 2026-10-08 23:19 | interactive (Luke) | opus-5-5 | 64.7k | 25.39M | 420.1k | 188 | 85 min | 315fdc5b |
| 2026-10-08 23:43 | nightly, child a6ba8b84 | sonnet-5-5 | 5.2k | 238.7k | 119.5k | 8 | 0 min | 315fdc5b |
| 2026-10-09 06:54 | lichess-morning | opus-5-5 | 3.0k | 1.08M | 40.0k | 32 | 22 min | e58646d1 |
| 2026-10-09 08:27 | interactive (Luke) | opus-5-5 | 13.5k | 1.52M | 58.1k | 34 | 14 min | e58646d1 |
| 2026-10-09 20:25 | interactive (Luke), child aec81b92 | haiku-5-5 | 29 | 69.3k | 42.5k | 6 | 0 min | 0ef509ad |
| 2026-10-09 22:23 | nightly | opus-5-5 | 88.2k | 30.39M | 269.7k | 314 | 42 min | 7c92089e |
| 2026-10-09 22:34 | nightly, child a58b81f9 | sonnet-5-5 | 8.9k | 130.4k | 82.2k | 6 | 1 min | 7c92089e |
| 2026-10-09 22:34 | nightly, child a369bcef | sonnet-5-5 | 9.7k | 508.6k | 47.0k | 16 | 1 min | 7c92089e |
| 2026-10-09 22:45 | nightly, child ab41442e | sonnet-5-5 | 1.9k | 191.8k | 71.8k | 8 | 0 min | 7c92089e |
| 2026-10-10 06:54 | lichess-morning | opus-5-5 | 2.0k | 752.2k | 33.9k | 22 | 11 min | 97fd4a91 |
| 2026-10-10 22:23 | nightly | opus-5-5 | 91.0k | 35.88M | 532.8k | 364 | 53 min | a05a4c7f |
| 2026-10-10 22:34 | nightly, child a687ea68 | sonnet-5-5 | 8.7k | 131.2k | 83.0k | 6 | 1 min | a05a4c7f |
| 2026-10-10 22:35 | nightly, child aacb4e04 | sonnet-5-5 | 9.0k | 512.0k | 48.2k | 16 | 2 min | a05a4c7f |
| 2026-10-10 22:38 | nightly, child adeed6ea | sonnet-5-5 | 2.5k | 206.9k | 78.0k | 8 | 0 min | a05a4c7f |
| 2026-10-11 06:54 | lichess-morning | opus-5-5 | 2.1k | 915.6k | 36.0k | 26 | 21 min | 94080747 |
| 2026-10-11 17:00 | weekly | opus-5-5 | 18.6k | 5.56M | 149.0k | 76 | 4 min | 3a30e0fd |
| 2026-10-11 22:23 | nightly | opus-5-5 | 62.6k | 29.39M | 191.1k | 356 | 39 min | 959624e5 |
| 2026-10-11 22:34 | nightly, child a0e02c2c | sonnet-5-5 | 8.4k | 137.0k | 87.0k | 6 | 1 min | 959624e5 |
| 2026-10-11 22:35 | nightly, child abe22777 | sonnet-5-5 | 9.1k | 442.8k | 48.1k | 14 | 1 min | 959624e5 |
| 2026-10-11 22:35 | nightly, child aa9434ff | sonnet-5-5 | 2.4k | 234.6k | 43.7k | 8 | 0 min | 959624e5 |
| 2026-10-11 23:02 | interactive (Luke) | opus-5-5 | 8.6k | 3.94M | 215.7k | 34 | 20 min | 959624e5 |
| 2026-10-12 06:54 | lichess-morning | opus-5-5 | 3.1k | 1.25M | 41.4k | 36 | 36 min | caee1db3 |
| 2026-10-12 08:05 | inspector | opus-5-5 | 10.4k | 2.69M | 58.8k | 62 | 2 min | ed465e49 |
| 2026-10-12 11:31 | trials | opus-5-5 | 34.6k | 8.34M | 109.5k | 154 | 21 min | 221f19ac |
| 2026-10-12 15:36 | workshop | opus-5-5 | 17.4k | 2.97M | 129.4k | 66 | 13 min | 85b52cf9 |
| 2026-10-12 19:04 | smith | opus-5-5 | 14.9k | 4.07M | 72.3k | 88 | 3 min | 4c87d6af |
| 2026-10-12 22:23 | nightly | opus-5-5 | 584 | 288.4k | 56.8k | 8 | 14 min | 2862abff |
| 2026-10-12 22:54 | interactive (Luke) | opus-5-5 | 48.9k | 16.21M | 124.4k | 204 | 29 min | 2862abff |
| 2026-10-12 23:03 | interactive (Luke), child a66d337d | sonnet-5-5 | 9.1k | 131.2k | 82.2k | 6 | 1 min | 2862abff |
| 2026-10-12 23:03 | interactive (Luke), child aba8a3b0 | sonnet-5-5 | 2.1k | 241.1k | 46.9k | 8 | 0 min | 2862abff |
| 2026-10-12 23:04 | interactive (Luke), child a0960dee | sonnet-5-5 | 9.9k | 370.5k | 51.2k | 12 | 1 min | 2862abff |
| 2026-10-13 06:54 | lichess-morning | opus-5-5 | 2.4k | 789.5k | 40.2k | 22 | 17 min | 2ec7913f |
| 2026-10-13 08:05 | inspector | opus-5-5 | 12.5k | 3.18M | 65.0k | 70 | 2 min | ce6d4128 |
| 2026-10-13 11:31 | trials | opus-5-5 | 39.9k | 8.38M | 123.6k | 142 | 24 min | 32a9385b |
| 2026-10-13 15:36 | workshop | opus-5-5 | 18.6k | 3.18M | 96.6k | 62 | 13 min | 678819a9 |
| 2026-10-13 15:49 | interactive (Luke) | opus-5-5 | 33.4k | 11.48M | 82.9k | 122 | 56 min | 678819a9 |
| 2026-10-13 15:53 | interactive (Luke) | opus-5-5 | 13.2k | 3.23M | 142.6k | 38 | 22 min | 32a9385b |
| 2026-10-13 19:04 | smith | fable-5-1 | 18.7k | 2.27M | 192.3k | 644 | 16 min | 296dea3a |
| 2026-10-13 22:23 | nightly | fable-5-1 | 110.0k | 32.00M | 329.7k | 3.7k | 55 min | b4aaef5f |
| 2026-10-13 22:28 | nightly, child a1d4e721 | sonnet-5-5 | 12.1k | 418.8k | 86.2k | 14 | 1 min | b4aaef5f |
| 2026-10-13 22:29 | nightly, child ae84244c | sonnet-5-5 | 8.3k | 168.2k | 52.8k | 6 | 1 min | b4aaef5f |
| 2026-10-13 22:49 | nightly, child a4af9a47 | sonnet-5-5 | 2.6k | 283.6k | 79.9k | 10 | 0 min | b4aaef5f |
| 2026-10-13 23:28 | interactive (Luke) | fable-5-1 | 638 | 367.2k | 742 | 2 | 0 min | b4aaef5f |
| 2026-10-14 06:54 | lichess-morning | fable-5-1 | 2.2k | 807.9k | 39.8k | 322 | 20 min | 00d9ba46 |
| 2026-10-14 08:05 | inspector | fable-5-1 | 20.6k | 1.77M | 98.0k | 546 | 16 min | 55a02649 |
| 2026-10-14 11:31 | trials | fable-5-1 | 53.6k | 6.44M | 134.2k | 1.7k | 30 min | 568f7e7f |
| 2026-10-14 14:55 | interactive (Luke) | fable-5-1 | 62.2k | 7.65M | 242.0k | 936 | 55 min | 55a02649 |
| 2026-10-14 14:55 | interactive (Luke) | fable-5-1 | 97.2k | 19.46M | 529.0k | 1.8k | 98 min | 568f7e7f |
| 2026-10-14 15:03 | interactive (Luke) | fable-5-1 | 4.4k | 1.28M | 44.3k | 450 | 7 min | 00d9ba46 |
| 2026-10-14 15:36 | workshop | opus-5-5 | 22.3k | 5.52M | 91.2k | 104 | 10 min | ac8caf5f |
| 2026-10-14 19:04 | smith | opus-5-5 | 12.3k | 3.73M | 70.9k | 80 | 10 min | dac31271 |
| 2026-10-14 19:15 | interactive (Luke) | opus-5-5 | 4.2k | 1.05M | 167.5k | 20 | 21 min | dac31271 |
| 2026-10-14 20:42 | interactive (Luke) | opus-5-5 | 357.7k | 132.51M | 1.73M | 836 | 266 min | 285f8be3 |
| 2026-10-14 22:23 | nightly | opus-5-5 | 72.2k | 29.22M | 252.9k | 306 | 30 min | 78c0e184 |
| 2026-10-14 22:27 | nightly, child a7b13898 | sonnet-5-5 | 9.5k | 133.6k | 84.5k | 6 | 1 min | 78c0e184 |
| 2026-10-14 22:28 | nightly, child a961d62a | sonnet-5-5 | 8.7k | 445.6k | 49.2k | 14 | 1 min | 78c0e184 |
| 2026-10-14 22:28 | nightly, child a2dbe24f | sonnet-5-5 | 3.8k | 234.4k | 114.8k | 6 | 0 min | 78c0e184 |
| 2026-10-14 22:37 | nightly, child ad1715bb | sonnet-5-5 | 2.7k | 211.6k | 81.2k | 8 | 0 min | 78c0e184 |
| 2026-10-15 05:39 | interactive (Luke), child a1732973 | sonnet-5-5 | 161 | 598.0k | 127.9k | 14 | 1 min | 285f8be3 |
| 2026-10-15 05:39 | interactive (Luke), child a2f2e707 | sonnet-5-5 | 1.2k | 611.0k | 106.6k | 16 | 0 min | 285f8be3 |
| 2026-10-15 05:39 | interactive (Luke), child a7b6e0be | sonnet-5-5 | 151 | 435.6k | 85.7k | 14 | 0 min | 285f8be3 |
| 2026-10-15 05:39 | interactive (Luke), child a894c49c | sonnet-5-5 | 149 | 316.3k | 104.0k | 10 | 0 min | 285f8be3 |
| 2026-10-15 05:39 | interactive (Luke), child a8cb8398 | sonnet-5-5 | 137 | 218.6k | 102.2k | 8 | 0 min | 285f8be3 |
| 2026-10-15 05:39 | interactive (Luke), child a93d4761 | haiku-5-5 | 820 | 408.0k | 158.0k | 10 | 0 min | 285f8be3 |
| 2026-10-15 05:39 | interactive (Luke), child ae746ab7 | sonnet-5-5 | 105 | 506.7k | 112.1k | 14 | 0 min | 285f8be3 |
| 2026-10-15 05:39 | interactive (Luke), child af77ecfe | sonnet-5-5 | 1.1k | 292.6k | 109.7k | 10 | 0 min | 285f8be3 |
| 2026-10-15 05:40 | interactive (Luke), child a42d70fb | sonnet-5-5 | 76 | 474.9k | 132.1k | 10 | 0 min | 285f8be3 |
| 2026-10-15 05:40 | interactive (Luke), child a4ae55e9 | haiku-5-5 | 2.4k | 289.4k | 120.1k | 8 | 1 min | 285f8be3 |
| 2026-10-15 05:40 | interactive (Luke), child a53ba304 | sonnet-5-5 | 1.0k | 658.3k | 147.6k | 12 | 0 min | 285f8be3 |
| 2026-10-15 05:40 | interactive (Luke), child a5d11513 | sonnet-5-5 | 727 | 468.0k | 76.5k | 12 | 0 min | 285f8be3 |
| 2026-10-15 05:40 | interactive (Luke), child a8e59442 | sonnet-5-5 | 1.9k | 1.26M | 154.0k | 22 | 1 min | 285f8be3 |
| 2026-10-15 05:40 | interactive (Luke), child ac06e34a | sonnet-5-5 | 159 | 816.8k | 142.2k | 14 | 1 min | 285f8be3 |
| 2026-10-15 05:40 | interactive (Luke), child aee39ef3 | sonnet-5-5 | 1.3k | 769.7k | 110.6k | 16 | 1 min | 285f8be3 |
| 2026-10-15 05:40 | interactive (Luke), child aef59c7f | sonnet-5-5 | 137 | 629.7k | 134.9k | 12 | 0 min | 285f8be3 |
| 2026-10-15 06:34 | interactive (Luke), child a8cd53a8 | sonnet-5-5 | 2.3k | 2.55M | 267.0k | 30 | 2 min | 285f8be3 |
| 2026-10-15 06:34 | interactive (Luke), child ac6fc219 | sonnet-5-5 | 1.6k | 372.7k | 118.0k | 10 | 1 min | 285f8be3 |
| 2026-10-15 06:54 | lichess-morning | opus-5-5 | 2.0k | 711.7k | 38.1k | 20 | 0 min | bfe716d2 |
| 2026-10-15 08:05 | inspector | opus-5-5 | 14.3k | 3.63M | 110.5k | 68 | 3 min | 294c0c02 |
| 2026-10-15 11:31 | trials | opus-5-5 | 20.8k | 5.72M | 94.3k | 108 | 16 min | 9921c9df |
| 2026-10-15 15:36 | workshop | opus-5-5 | 12.8k | 2.78M | 77.9k | 56 | 2 min | ae511c1b |
| 2026-10-15 21:11 | smith | sonnet-5-5 | 7.0k | 2.16M | 120.8k | 46 | 13 min | 7e605414 |
| 2026-10-15 22:23 | nightly | sonnet-5-5 | 20.2k | 9.04M | 131.9k | 130 | 12 min | 8e7526bc |
| 2026-10-15 22:26 | nightly, child a34daba9 | sonnet-5-5 | 7.4k | 135.5k | 84.0k | 6 | 0 min | 8e7526bc |
| 2026-10-15 22:27 | nightly, child aa3e9c92 | sonnet-5-5 | 3.6k | 336.3k | 95.0k | 8 | 0 min | 8e7526bc |
| 2026-10-15 22:27 | nightly, child ad75b266 | sonnet-5-5 | 1.7k | 240.1k | 45.8k | 8 | 0 min | 8e7526bc |
| 2026-10-15 22:27 | nightly, child a38062c4 | sonnet-5-5 | 8.1k | 508.6k | 47.9k | 16 | 1 min | 8e7526bc |
| 2026-10-16 06:54 | lichess-morning | sonnet-5-5 | 1.2k | 637.5k | 37.6k | 18 | 3 min | 40133edc |
| 2026-10-16 08:05 | inspector | sonnet-5-5 | 7.0k | 1.91M | 57.2k | 46 | 6 min | 4c4573bb |
| 2026-10-16 11:31 | trials | sonnet-5-5 | 16.6k | 3.34M | 72.9k | 74 | 4 min | e9a30298 |
| 2026-10-16 15:36 | workshop | sonnet-5-5 | 12.7k | 2.55M | 72.0k | 54 | 3 min | 8712b283 |
| 2026-10-16 22:23 | nightly | opus-5-5 | 56.5k | 23.46M | 230.8k | 266 | 18 min | d5fc316b |
| 2026-10-16 22:26 | nightly, child ab92fe47 | sonnet-5-5 | 8.7k | 405.2k | 81.9k | 14 | 2 min | d5fc316b |
| 2026-10-16 22:27 | nightly, child a9a9c397 | sonnet-5-5 | 8.1k | 166.7k | 50.8k | 6 | 0 min | d5fc316b |
| 2026-10-16 22:32 | nightly, child a0828231 | sonnet-5-5 | 2.2k | 219.1k | 82.7k | 8 | 0 min | d5fc316b |
| 2026-10-17 06:54 | lichess-morning | opus-5-5 | 1.7k | 557.7k | 37.0k | 16 | 0 min | b7aca686 |
| 2026-10-17 08:06 | inspector | opus-5-5 | 8.9k | 2.23M | 64.1k | 52 | 3 min | 98dba531 |
| 2026-10-17 11:31 | trials | opus-5-5 | 19.1k | 4.07M | 76.4k | 88 | 7 min | cc91fc0e |
| 2026-10-17 15:36 | workshop | opus-5-5 | 16.8k | 4.21M | 84.3k | 82 | 3 min | c39c026c |
| 2026-10-17 22:23 | nightly | opus-5-5 | 38.2k | 12.10M | 294.5k | 168 | 31 min | 9fb02aa5 |
| 2026-10-17 22:31 | nightly, child aa695ace | sonnet-5-5 | 9.6k | 134.8k | 85.3k | 6 | 1 min | 9fb02aa5 |
| 2026-10-17 22:32 | nightly, child aa94b3ac | sonnet-5-5 | 8.7k | 376.8k | 51.9k | 12 | 1 min | 9fb02aa5 |
| 2026-10-17 22:32 | nightly, child aaf3ce01 | sonnet-5-5 | 1.9k | 232.0k | 40.9k | 8 | 0 min | 9fb02aa5 |
| 2026-10-18 06:54 | lichess-morning | opus-5-5 | 1.7k | 565.2k | 38.5k | 16 | 1 min | 9fa6428e |
| 2026-10-18 08:06 | inspector | opus-5-5 | 10.8k | 2.92M | 74.2k | 62 | 5 min | 75f1c803 |
| 2026-10-18 11:31 | trials | opus-5-5 | 34.7k | 8.36M | 138.7k | 132 | 9 min | fac7da8c |
| 2026-10-18 15:36 | workshop | opus-5-5 | 20.1k | 3.58M | 82.7k | 70 | 5 min | f095de29 |
| 2026-10-18 17:00 | weekly | opus-5-5 | 16.7k | 5.10M | 135.1k | 74 | 4 min | 74f2f0a7 |
| 2026-10-19 00:10 | interactive (Luke) | opus-5-5 | 4.5k | 515.4k | 43.9k | 14 | 6 min | 64be3c9a |
| 2026-10-19 00:17 | interactive (Luke) | opus-5-5 | 40.5k | 6.73M | 176.2k | 116 | 62 min | 3e5364b9 |
| 2026-10-19 00:28 | interactive (Luke) | opus-5-5 | 20.6k | 1.90M | 95.6k | 36 | 30 min | cd365d06 |
| 2026-10-19 00:42 | interactive (Luke), child a8eb9584 | fable-5-1 | 309 | 5.27M | 224.0k | 966 | 19 min | cd365d06 |
| 2026-10-19 02:27 | nightly | opus-5-5 | 44.0k | 14.90M | 186.7k | 186 | 31 min | aec3b7a3 |
| 2026-10-19 02:34 | nightly, child a4ed95cd | sonnet-5-5 | 8.8k | 338.7k | 79.6k | 12 | 1 min | aec3b7a3 |
| 2026-10-19 02:36 | nightly, child a4784129 | sonnet-5-5 | 7.7k | 168.1k | 51.7k | 6 | 0 min | aec3b7a3 |
| 2026-10-19 03:02 | nightly, child a54835d5 | sonnet-5-5 | 1.9k | 208.1k | 76.1k | 8 | 0 min | aec3b7a3 |
| 2026-10-19 06:54 | lichess-morning | opus-5-5 | 2.5k | 971.8k | 43.3k | 26 | 10 min | f431b623 |
| 2026-10-19 08:06 | inspector | opus-5-5 | 9.1k | 1.67M | 66.4k | 38 | 3 min | 88a6ae3c |
| 2026-10-19 18:01 | trials | opus-5-5 | 27.0k | 12.51M | 117.0k | 196 | 12 min | d47fbcef |
| 2026-10-19 18:12 | workshop | opus-5-5 | 19.0k | 4.05M | 85.9k | 74 | 4 min | f56b8d71 |
| 2026-10-19 22:23 | nightly | opus-5-5 | 47.2k | 16.40M | 180.1k | 212 | 23 min | 1f9c03db |
| 2026-10-19 22:31 | nightly, child a3ce5d61 | sonnet-5-5 | 11.6k | 432.0k | 89.7k | 14 | 1 min | 1f9c03db |
| 2026-10-19 22:32 | nightly, child a0e72996 | sonnet-5-5 | 4.0k | 348.0k | 68.7k | 10 | 0 min | 1f9c03db |
| 2026-10-19 22:32 | nightly, child a28a6215 | sonnet-5-5 | 8.8k | 169.9k | 54.5k | 6 | 1 min | 1f9c03db |
| 2026-10-19 22:34 | nightly, child a416d6f2 | sonnet-5-5 | 2.3k | 217.4k | 81.6k | 8 | 0 min | 1f9c03db |
| 2026-10-20 06:54 | lichess-morning | opus-5-5 | 1.9k | 787.1k | 37.4k | 22 | 16 min | 04c10e56 |
| 2026-10-20 08:06 | inspector | opus-5-5 | 9.7k | 2.65M | 60.1k | 60 | 5 min | 9825fd27 |
| 2026-10-20 11:31 | trials | opus-5-5 | 21.6k | 4.37M | 85.5k | 90 | 9 min | 36b78f8f |
| 2026-10-20 15:36 | workshop | opus-5-5 | 21.1k | 4.03M | 96.3k | 74 | 5 min | 96ffe25a |
| 2026-10-20 15:37 | workshop, child a44008d1 | sonnet-5-5 | 10.9k | 458.8k | 77.7k | 16 | 2 min | 96ffe25a |
| 2026-10-20 22:23 | nightly | opus-5-5 | 54.1k | 19.07M | 193.8k | 250 | 24 min | 7958ee49 |
| 2026-10-20 22:31 | nightly, child a25d8ff9 | sonnet-5-5 | 8.0k | 134.1k | 82.9k | 6 | 1 min | 7958ee49 |
| 2026-10-20 22:31 | nightly, child aef2c3c6 | sonnet-5-5 | 2.0k | 259.5k | 54.2k | 8 | 0 min | 7958ee49 |
| 2026-10-20 22:31 | nightly, child a8e27642 | sonnet-5-5 | 9.3k | 450.8k | 51.4k | 14 | 1 min | 7958ee49 |
| 2026-10-20 22:34 | nightly, child abc98915 | sonnet-5-5 | 1.7k | 235.0k | 42.0k | 8 | 0 min | 7958ee49 |
| 2026-10-20 23:38 | smith | opus-5-5 | 8.7k | 2.28M | 58.4k | 52 | 2 min | 20b48e5f |
| 2026-10-21 06:54 | lichess-morning | opus-5-5 | 2.1k | 830.5k | 39.1k | 22 | 17 min | 8d2e8fd7 |
| 2026-10-21 08:05 | inspector | opus-5-5 | 9.3k | 2.02M | 71.1k | 42 | 2 min | d2ecbc3d |
| 2026-10-21 11:31 | trials | opus-5-5 | 8.2k | 2.56M | 107.7k | 58 | 12 min | 6eaca375 |
| 2026-10-21 15:36 | workshop | opus-5-5 | 21.9k | 5.18M | 94.9k | 96 | 5 min | f8742f2e |
| 2026-10-21 18:40 | interactive (Luke) | fable-5-1 | 93.2k | 4.08M | 229.6k | 642 | 21 min | fb2ba978 |
| 2026-10-21 19:04 | smith | fable-5-1 | 25.4k | 2.77M | 98.6k | 738 | 7 min | 6a61a56d |
| 2026-10-21 19:16 | interactive (Luke) | fable-5-1 | 17.5k | 4.79M | 181.0k | 1.7k | 73 min | 1e9d7039 |
| 2026-10-22 06:54 | lichess-morning | fable-5-1 | 3.9k | 860.0k | 43.4k | 322 | 18 min | 2f457931 |
| 2026-10-22 08:06 | inspector | fable-5-1 | 25.9k | 1.87M | 129.4k | 450 | 7 min | ae3fc86d |
| 2026-10-22 11:31 | trials | fable-5-1 | 45.6k | 6.80M | 133.9k | 1.6k | 13 min | fa5aa4a3 |
| 2026-10-22 15:36 | workshop | opus-5-5 | 20.5k | 4.55M | 86.3k | 84 | 5 min | 9f8d01cd |
| 2026-10-22 19:04 | smith | opus-5-5 | 13.8k | 4.30M | 76.5k | 84 | 3 min | bb4e94e5 |
| 2026-10-22 22:23 | nightly | opus-5-5 | 66.0k | 22.77M | 226.7k | 262 | 36 min | 361172cb |
| 2026-10-22 22:28 | nightly, child a6da71d9 | sonnet-5-5 | 9.6k | 602.7k | 89.9k | 18 | 2 min | 361172cb |
| 2026-10-22 22:28 | nightly, child afea33db | sonnet-5-5 | 3.8k | 386.9k | 68.0k | 10 | 0 min | 361172cb |
| 2026-10-22 22:29 | nightly, child ad58c5d8 | sonnet-5-5 | 8.3k | 177.7k | 51.4k | 6 | 1 min | 361172cb |
| 2026-10-22 22:39 | nightly, child af54b9ec | sonnet-5-5 | 1.7k | 213.5k | 78.5k | 8 | 0 min | 361172cb |
| 2026-10-23 06:54 | lichess-morning | opus-5-5 | 3.2k | 935.0k | 41.8k | 24 | 15 min | b98670e1 |
| 2026-10-23 08:06 | inspector | opus-5-5 | 11.0k | 2.49M | 70.1k | 50 | 3 min | eada42e9 |
| 2026-10-23 11:31 | trials | opus-5-5 | 26.7k | 5.96M | 93.7k | 110 | 6 min | 18927434 |
| 2026-10-23 15:36 | workshop | opus-5-5 | 20.2k | 3.48M | 81.2k | 64 | 3 min | 2de9c599 |
| 2026-10-23 19:04 | smith | opus-5-5 | 13.4k | 3.51M | 70.9k | 72 | 2 min | 1cdfef67 |
| 2026-10-23 22:23 | nightly | fable-5-1 | 87.5k | 17.97M | 282.8k | 2.3k | 29 min | 17edb0f9 |
| 2026-10-23 22:32 | nightly, child a10fdc83 | sonnet-5-5 | 9.1k | 142.3k | 88.4k | 6 | 1 min | 17edb0f9 |
| 2026-10-23 22:33 | nightly, child a9699378 | sonnet-5-5 | 7.8k | 2.64M | 168.6k | 38 | 1 min | 17edb0f9 |
| 2026-10-23 22:33 | nightly, child a6a66d45 | sonnet-5-5 | 5.2k | 1.09M | 124.2k | 20 | 0 min | 17edb0f9 |
| 2026-10-23 22:35 | nightly, child a887c877 | sonnet-5-5 | 1.6k | 248.9k | 41.8k | 8 | 0 min | 17edb0f9 |
| 2026-10-24 06:54 | lichess-morning | fable-5-1 | 3.6k | 963.5k | 44.7k | 354 | 16 min | 874c5e80 |
| 2026-10-24 08:06 | inspector | fable-5-1 | 15.3k | 1.75M | 84.1k | 482 | 3 min | 470eee31 |
| 2026-10-24 11:31 | trials | fable-5-1 | 44.8k | 5.20M | 132.3k | 1.4k | 11 min | 223aabc3 |
| 2026-10-24 15:36 | workshop | fable-5-1 | 28.9k | 3.22M | 123.3k | 708 | 6 min | ac00bad4 |
| 2026-10-24 15:37 | workshop, child a7b7828a | sonnet-5-5 | 2.0k | 191.9k | 67.9k | 8 | 0 min | ac00bad4 |
| 2026-10-24 19:05 | smith | fable-5-1 | 44.0k | 4.04M | 279.1k | 838 | 19 min | 145be128 |
| 2026-10-24 22:23 | nightly | fable-5-1 | 87.8k | 16.05M | 295.2k | 1.9k | 24 min | 6d39858a |
| 2026-10-24 22:31 | nightly, child a23d2566 | sonnet-5-5 | 9.0k | 141.0k | 87.2k | 6 | 1 min | 6d39858a |
| 2026-10-24 22:31 | nightly, child a7754260 | sonnet-5-5 | 4.5k | 1.35M | 186.8k | 22 | 0 min | 6d39858a |
| 2026-10-24 22:31 | nightly, child ac9a651e | sonnet-5-5 | 4.9k | 823.4k | 119.8k | 16 | 0 min | 6d39858a |
| 2026-10-24 22:34 | nightly, child a566e895 | sonnet-5-5 | 2.0k | 242.8k | 39.8k | 8 | 0 min | 6d39858a |
| 2026-10-25 07:54 | lichess-morning | opus-5-5 | 2.8k | 848.9k | 39.9k | 22 | 13 min | 86f2b4bb |
| 2026-10-25 09:06 | inspector | opus-5-5 | 22.4k | 2.70M | 91.5k | 50 | 4 min | 5a26b172 |
| 2026-10-25 12:31 | trials | opus-5-5 | 18.5k | 4.21M | 76.5k | 86 | 4 min | 3f911d65 |
| 2026-10-25 16:36 | workshop | opus-5-5 | 23.4k | 5.06M | 100.2k | 90 | 5 min | 0c5cb4b9 |
| 2026-10-25 18:01 | weekly | opus-5-5 | 14.3k | 3.14M | 98.6k | 54 | 2 min | 4420c6c2 |
| 2026-10-25 20:05 | smith | opus-5-5 | 12.8k | 3.12M | 71.1k | 66 | 4 min | 1f04feb3 |
| 2026-10-25 23:24 | nightly | opus-5-5 | 52.2k | 17.78M | 182.7k | 222 | 23 min | 7a56da4e |
| 2026-10-25 23:30 | nightly, child a6b874fe | sonnet-5-5 | 8.8k | 137.9k | 85.3k | 6 | 1 min | 7a56da4e |
| 2026-10-25 23:31 | nightly, child ad11c040 | sonnet-5-5 | 3.5k | 377.7k | 71.6k | 10 | 0 min | 7a56da4e |
| 2026-10-26 07:55 | lichess-morning | opus-5-5 | 3.3k | 993.5k | 39.7k | 26 | 16 min | b7f83ab4 |
| 2026-10-26 09:06 | inspector | opus-5-5 | 10.3k | 2.13M | 66.4k | 44 | 3 min | 0e6ac93b |
| 2026-10-26 12:31 | trials | opus-5-5 | 17.2k | 3.69M | 80.7k | 76 | 8 min | 09b6e569 |
| 2026-10-26 16:36 | workshop | opus-5-5 | 20.3k | 2.85M | 80.6k | 54 | 4 min | f4409220 |
| 2026-10-26 20:05 | smith | opus-5-5 | 18.2k | 3.95M | 80.5k | 78 | 3 min | 0ca06549 |
| 2026-10-26 23:24 | nightly | opus-5-5 | 48.4k | 17.42M | 173.1k | 236 | 16 min | 2876333e |
| 2026-10-26 23:29 | nightly, child a2fa10e6 | sonnet-5-5 | 8.6k | 135.1k | 82.2k | 6 | 1 min | 2876333e |
| 2026-10-26 23:29 | nightly, child a7c24dd5 | sonnet-5-5 | 4.8k | 654.1k | 73.8k | 16 | 0 min | 2876333e |
| 2026-10-26 23:29 | nightly, child aa61aa65 | sonnet-5-5 | 2.3k | 250.5k | 55.4k | 8 | 0 min | 2876333e |
| 2026-10-26 23:35 | nightly, child ac47ea77 | sonnet-5-5 | 1.6k | 207.0k | 75.8k | 8 | 0 min | 2876333e |
| 2026-10-27 07:55 | lichess-morning | opus-5-5 | 2.3k | 669.9k | 36.9k | 18 | 0 min | 9b6f0441 |
| 2026-10-27 09:06 | inspector | opus-5-5 | 1.3k | 357.4k | 37.2k | 10 | 0 min | cd71786e |
