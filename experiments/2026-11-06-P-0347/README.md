# P-0347: does the METAR gap depend on season? Five years at Munich airport

Question: P-0345's 18 months read 90% agreement in January and 66% in July. Does that survive five years?

Method: `five_years.py`. EDDM METAR highs by Berlin local day against DWD 01262's daily TXK, 1 Jan 2021 to 5 Nov 2026,
2,135 days, 102,496 reports. No day was more than 3 C apart.

- Same as rounded TXK on 74.1% of days. Misses lean low: 409 under, 145 over. Mean gap -0.08 C.
- By season: winter 75.7%, spring 71.6%, summer 72.6%, autumn 76.6%. Winter minus summer is 3 points with a standard
  error of about 2.7, so no season effect I can stand behind. My shot of at least 8 points missed.
- By month 68% (July) to 78% (June): the two neighbouring months sit at opposite ends, which is what noise looks like.
- By year the agreement runs 70% (2023) to 81% (2026), and the mean gap moved from -0.22 in 2023 to +0.04 in 2026.

So P-0345's January against July gap was small-sample noise, from one or two of each month. The year-to-year drift is
the more interesting thing and may mean a sensor or reporting change. I have not looked for one.

Caveats: TXK is a climate-day figure and P-0345 used TX_10 by local day, so 74% against 78% is not a clean comparison.
The 2021 to 2026 rule is still the D-023 one on trial.
