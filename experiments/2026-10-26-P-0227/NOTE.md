# P-0227: FOMC dates 2023 to 2026, keyless (26 Oct 2026)

Called shot: 32 scheduled meetings, parsed from one public page with no key.

Ran `fomc.py` (stdlib only) against https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm:
one GET, 165,747 bytes, years 2021 to 2027 on the page. Parsed 8 scheduled meetings for each of 2023,
2024, 2025 and 2026: **32**, as called. One extra row kept apart: a notation vote on 22 Aug 2025,
which is not a meeting. Stars mark meetings with a Summary of Economic Projections (4 a year).
Cross-year meetings come through as "Jan/Feb 31-1", so a consumer has to split the month on `/`.
Decision day is the last day of each range.

Output `fomc.json`. Next meeting on the page: 27 to 28 Oct 2026, decision on the 28th.

Verdict: works. The release calendar the vault thread wanted can be built from this page without a key;
the FOMC leg of it is done.
