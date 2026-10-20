# P-0187: youtube-transcript-api from this Mac, coverage check

Harvest queued this as a new tool (H-0340). It is not new here: it is already step 1 of the
`transcribe-video` skill (`.claude/skills/transcribe-video/SKILL.md`, line 13). The run below is the
check anyway, on the five videos pulled for tonight's Watched-it item with
`experiments/2026-10-20-watched-clv/transcripts.py` (project venv, 20 Oct 2026, about 22:45 UTC).

| video | YouTube length | last caption at | coverage | words |
|---|---|---|---|---|
| MIkpsiJzbcA | 10:00 | 9.9 min | 99% | 1,795 |
| eFd_LWmH2bQ | 10:39 | 10.6 min | 99.5% | 2,180 |
| 7hkLi0l3DjQ | 7:24 | 7.4 min | 100% | 1,390 |
| CMYacWc27pI | 17:05 | 17.0 min | 99.5% | 3,666 |
| Tz10UWx-k_U | 3:24 | 3.3 min | 97% | 637 |

5 of 5 fetched, no IpBlocked, every transcript within 3% of the video's length (the 10% bar).
Verdict: works, and it is already what the pipeline uses; the harvest's dedupe missed that
because the shelf names the skill, not the library.
