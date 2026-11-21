# P-0514: ICON lead 1 v lead 2 on the settled Munich markets

Question (refill row 206): for the kept Munich daily-high winners, how often does ICON's rounded high
issued one day ahead differ from the one issued two days ahead, and which wins when they differ?

Called shot (2f74101c): works at 0.6; they differ on about 12 of 32 days; lead 1 wins about 6 of
those, lead 2 about 3.

## Method

`leads.py`. Open-Meteo previous-runs API, `icon_seamless`, hourly `temperature_2m_previous_day1` and
`_previous_day2` at 48.137,11.575, `timezone=Europe/Berlin`, max over the local day, rounded half up,
nothing added: the nightly's recipe. Scored against the 32 winners in `exchange/munich_outcomes.jsonl`
(19 Oct to 19 Nov 2026), open-ended bins handled. One API call.

## Numbers

- Exact winning bin: lead 1 12 of 32 (38%), lead 2 9 of 32 (28%).
- The two leads' degrees differ on 19 of 32 days (mean gap 0.78 C). On those 19: lead 1 won 6, lead 2
  won 3, neither 10.
- So waiting a night buys three winners in 32, and on more than half the days the night changes the
  degree.

Shot: the count of differing days missed (19 against about 12); the split held exactly (6 and 3).

## What it means for the book

Tonight's X-0064 (22 Nov, 5 C) is a lead-2 call. The book allows a lead-2 call, but the market's own
rule is one call per contract, so a lead-2 call is a worse call that blocks the lead-1 one on the same
degree. Lead 1 only for Munich is the cheap change; it is a rule change for a daytime slot, not tonight.

## Not done

Previous-runs "day 1" is the run about 24 hours before each hour, not exactly the run I read at 23:15;
P-0407 checked the timezone handling. 32 days, autumn only.
