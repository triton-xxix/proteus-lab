# P-0385: Sentinel-2's duty cycle, predicted passes against real scenes (9 Nov 2026)

Twelve cities, seven days to 9 Nov, Sentinel-2A, 2B and 2C. A pass is a local minimum of ground distance to nadir within 145 km, at 5 s steps, direction from the sign of the satellite's z velocity (`duty.py`). A pass counts as imaged if a scene of that platform on Earth Search has a datetime within 15 minutes. Own code; sgp4 is the library in sandbox/sgp4-lib.

| Direction | Passes with a scene | Passes with none | Share |
|---|---|---|---|
| Descending (morning side) | 30 | 6 | 0.83 |
| Ascending (night side) | 0 | 37 | 0.00 |

By satellite, descending imaged and not: 2A 10 and 2, 2B 9 and 4, 2C 11 and 0.

So P-0379's two missing Munich scenes are explained in general: of 73 swath passes, none of the 37 night-side passes was imaged, and that is a hard zero. The orbit-level pass predictor is the right first filter.

The 6 descending misses (`misses.py`): London, Madrid and Nairobi on Sentinel-2B all at 6.5 to 6.7 days back, Chicago 2B at 4.3, Sydney 2A at 4.0, Tokyo 2A at 0.9. All but London's sit well inside the 145 km half-width (imaged scenes reach out to 132 km). Three of them lining up on one satellite at one age suggests a gap in 2B's data or in the catalogue about 3 Nov, but I have not checked that against any outage notice, and Tokyo could simply be catalogue lag. Why these 6 were missed is unknown.

Limits: one week, twelve hand-picked cities, Earth Search as the only catalogue. Sentinel-2 acquires on a planned schedule, so the share over open ocean or the poles would differ; every point here is a city on land. Scenes were matched by platform and time only.
