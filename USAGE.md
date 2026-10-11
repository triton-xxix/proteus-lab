# Usage

What Proteus costs in Claude, in tokens, rebuilt every Sunday by `bin/usage.py` from the
session transcripts on this Mac. Never typed by hand.

What it cannot see: sessions on other machines or in other folders, and anything before the
transcripts on disk. Interactive sessions are labelled "interactive (Luke)" and kept apart
from the scheduled runs, so the nightly is not blamed for them. A session resumed later is
split at each prompt, so one transcript can be two rows. Wall time is active time, gaps
capped at 10 minutes. Times and weeks are UTC. No pounds figure yet: it waits until list
prices are checked, not remembered.

Rebuilt 2026-10-11 18:02.

## By month

| Month | Who | Output | Cache reads | Cache writes | Uncached input |
|---|---|---|---|---|---|
| 2026-09 | scheduled runs | 413.4k | 75.71M | 2.18M | 3.9k |
| 2026-09 | Luke's sessions | 1.52M | 263.86M | 6.81M | 20.7k |
| 2026-10 | scheduled runs | 774.6k | 195.91M | 4.68M | 5.7k |
| 2026-10 | Luke's sessions | 1.87M | 395.27M | 9.89M | 11.3k |

## Scheduled output by ISO week

The charter's alarm: a week more than double the trailing four-week average is named in
Field Notes with the step that caused it.

| Week | Runs | Output | Trailing 4-week average | Over double? |
|---|---|---|---|---|
| 2026-W39 | 8 | 221.1k | n/a | n/a |
| 2026-W40 | 8 | 423.7k | 221.1k | no |
| 2026-W41 | 10 | 543.2k | 322.4k | no |

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
| 2026-10-07 01:45 | interactive (Luke) | fable-5-1 | 319.0k | 32.89M | 1.33M | 2.0k | 115 min | 5e0288f2 |
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
| 2026-10-07 23:42 | interactive (Luke) | opus-5-5 | 140.2k | 34.11M | 495.2k | 272 | 75 min | 0ef509ad |
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
| 2026-10-11 17:00 | weekly | opus-5-5 | 7.2k | 2.49M | 132.5k | 42 | 1 min | 3a30e0fd |
