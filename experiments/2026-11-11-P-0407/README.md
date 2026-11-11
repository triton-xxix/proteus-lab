# P-0407: does Open-Meteo previous-runs honour the timezone parameter?

Trials, 11 Nov 2026. Refill source 144.

**Question.** P-0392 got identical daily highs on UTC days and Europe/Berlin days at Munich and left
it open whether the endpoint ignores `timezone`, which would mean every day-max script since P-0281
ran on UTC days whatever it asked for.

**Shot.** works at 0.85: honoured; offsets 0, 3600 and 50400 seconds; series line up at 1 and 14
slots; day max differs on 6 of 7 Kiritimati days and 0 of 7 Berlin days.

**Method.** `tz.py`: three keyless pulls of the Munich city point (48.137, 11.575), `icon_seamless`,
1 to 7 Nov 2026, `temperature_2m` and `temperature_2m_previous_day1`, with `timezone=UTC`,
`Europe/Berlin` and `Pacific/Kiritimati` (UTC+14, picked so a real shift cannot hide). For each, the
offset the reply reports, the slot shift that makes its hourly series equal the UTC pull's, and the
day maxima on its own days against UTC days. Raw replies saved.

**Numbers** (results.json):

| timezone asked | offset reported | first slot as UTC | shift v UTC pull | slots equal at that shift | day max differs from UTC days (lead 0, lead 1) |
|---|---|---|---|---|---|
| UTC | 0 | 1 Nov 00:00 | 0 | all | 0 of 7, 0 of 7 |
| Europe/Berlin | 3600 | 31 Oct 23:00 | 1 | 167 of 167 | 0 of 7, 0 of 7 |
| Pacific/Kiritimati | 50400 | 31 Oct 10:00 | 14 | 154 of 154 | 7 of 7 (up to 3.6 C), 7 of 7 (up to 4.7 C) |

**Reading.** The endpoint honours `timezone`. The window starts at local midnight, the hours shift by
exactly the offset, and every overlapping value is identical, lead 1 included. P-0392's identical
UTC and Berlin highs were real: a one-hour shift moves the 23:00 UTC hour into the next day, and a
November night hour is never the day's high. On these 7 days it changed 0 of 14 day maxima.

So the day-max scripts since P-0281 ran on the days they asked for, and UTC against Berlin does not
matter for a high at this time of year. It could matter for a daily low, or in a summer heat hold
past midnight; not tested.

**Not done.** Only one point, one week, one model. The daily (not hourly) variables were not pulled.
