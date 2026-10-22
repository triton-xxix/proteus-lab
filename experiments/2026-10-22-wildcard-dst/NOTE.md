# Open-Meteo across the clock change (wildcard, 22 Oct 2026)

Question: what does the end of BST on Sunday 25 Oct 2026 do to London's sunrise and sunset, read from
Open-Meteo's keyless forecast API with `timezone=Europe/London`?

Pulled at about 22:45 UTC on 22 Oct:

    curl "https://api.open-meteo.com/v1/forecast?latitude=51.507&longitude=-0.128&daily=sunrise,sunset,daylight_duration&timezone=Europe%2FLondon&start_date=2026-10-22&end_date=2026-10-31"

Every day from 22 to 31 Oct came back with `utc_offset_seconds` 3600 (GMT+1). Sunrise 07:36 on the
22nd, 07:41 on the 25th, 07:43 on the 26th: no one-hour jump. A second call for 26 to 27 Oct alone
also came back GMT+1, sunrise 07:43. So the offset is taken from the moment of the request, not the
date asked for, and every local time after the change is an hour late until the API's own clock
crosses it. On the 26th London's real sunrise is about 06:43 GMT.

Daylight itself: 36,984 s on the 22nd, 35,006 s on the 31st, so London loses about 3 min 40 s a day
this week, 33 minutes over nine days. The clock change moves none of it; sunset goes from about
17:46 to about 16:44 on the clock.

Why it matters to me: the exchange book's Munich weather calls use Open-Meteo daily maxima with a
local timezone, and Germany also leaves summer time on 25 Oct. For a market dated after the change,
the "day" Open-Meteo aggregates would run 01:00 to 01:00 local. For a daily maximum in late October
that hour is night and almost never holds the high, so I expect no effect on the calls; it would
matter for a daily minimum or a precipitation total.

Not checked: whether `timezone=auto` or `utc_offset` behaves differently, and whether the offset flips
once the request is made after 01:00 UTC on the 25th.
