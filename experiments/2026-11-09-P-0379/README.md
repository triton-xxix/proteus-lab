# P-0379: watched.earth's pass search, checked on Sentinel-2A over Munich (9 Nov 2026)

watched.earth (H-0586) propagates CelesTrak elements with SGP4 and claims no missed passes against a brute-force check.
I did not run its code. `run.py` is my own, using the sgp4 library from PyPI on CelesTrak's current Sentinel-2A elements,
over Munich for the last 7 days. Truth is a 1-second scan.

| Elevation above | Truth passes | 60 s scan | 300 s plus peak search |
|---|---|---|---|
| 0 degrees | 51 | 50 (1 missed) | 51 |
| 10 degrees | 34 | 34 | 34 |
| 45 degrees | 12 | 12 | 12 |

The coarse search had no extras and its peak times were within 0.48 s of truth. Time: 1 s scan 17 s, 60 s scan 0.3 s,
coarse 0.2 to 0.7 s, all in Python and for one satellite.

Against real scenes: Earth Search returned 5 Sentinel-2 items over Munich for the 7 days, 2 of them Sentinel-2A
(5 Nov 10:17:35 and 8 Nov 10:27:32 UTC). Each sits 0.1 and 0.3 s from a predicted pass peak, at 86 and 95 km from nadir,
inside the 145 km swath half-width. The source said Sentinel-2 timestamps can be 5 to 10 minutes off; in these two,
Earth Search's datetime is not. The other 3 items are not Sentinel-2A and were not checked.

The model has 4 passes within the swath half-width and 2 of them have a scene. I did not check the other two;
Sentinel-2 images on its descending daytime side only, which would explain them, but that is not measured here.

Verdict: works, for this slice. One satellite, one point, one week, and the timing check has n = 2. The 17,000-object
speed claim and the page itself were not tested.
