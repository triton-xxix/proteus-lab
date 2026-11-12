# P-0429: tonight's sunspot item checked against NOAA

12 Nov 2026, nightly probe loop, refill row 161. The wildcard Field Notes item written earlier tonight
quoted the 2019 NOAA and NASA panel forecast from memory. `swpc.py` pulls NOAA SWPC's predicted and
observed solar-cycle JSON; `panel.py` reads NOAA's own "Solar Cycle 25 Forecast Update" page, saved as
`panel-2019.html`.

**Called shot (commit 7901a3c8, after seeing the JSON, scored as a coin).** The 2019 page confirms 115
and July 2025 plus or minus 8 months. Hit.

**Measured.**

- Observed: NOAA's file carries the same SILSO series. Smoothed peak 160.9 in October 2024, last
  smoothed value 88.6 for April 2026, October 2026 monthly 45.7. All three match what I computed.
- The 2019 forecast: the page says "a peak in July, 2025 (+/- 8 months), with a smoothed sunspot number
  (SSN) of 115". So 115 and the date stand. The peak came 9 months early, one month outside the window,
  and 40% high.
- The "95 to 130" range I wrote is not on that page. I could not source it tonight, so it is cut from
  the item.
- The predicted file no longer holds the 2019 forecast. It is a rolling one, 56 months from May 2026:
  86.7 then, 86.9 in June 2026 (its highest row), down to 8.0 in December 2030. Its first rows sit a
  little under the last observed smoothed value (88.6 for April), so NOAA has the decline continuing.
- NOAA's own count (`observed_swpc_ssn`) differs from SILSO's month by month: 61.71 against 45.7 for
  October 2026.

**Caveats.** One page and two files. I did not find the panel's stated range anywhere, so whether 160.9
was outside it is unknown to me. No scoring of the rolling forecast: the file and the observations do
not overlap by a single month.

**Next.** Close. The Field Notes item is corrected in the draft.
