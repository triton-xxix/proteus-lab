"""Earliest sunset, latest sunrise and shortest day, winter 2026-27, NOAA solar equations.
Writes results.json to the experiment folder given as argv[1]."""
import json, math, sys, datetime as dt

CITIES = {"London": (51.5074, -0.1278), "Munich": (48.137, 11.575), "Edinburgh": (55.9533, -3.1883),
          "Madrid": (40.4168, -3.7038), "Oslo": (59.9139, 10.7522)}

def events(day, lat, lon):
    # NOAA spreadsheet algorithm, times in UTC minutes
    jd = day.toordinal() + 1721424.5 + 0.5  # noon UTC
    t = (jd - 2451545) / 36525
    L0 = (280.46646 + t * (36000.76983 + 0.0003032 * t)) % 360
    M = 357.52911 + t * (35999.05029 - 0.0001537 * t)
    e = 0.016708634 - t * (0.000042037 + 0.0000001267 * t)
    C = (math.sin(math.radians(M)) * (1.914602 - t * (0.004817 + 0.000014 * t))
         + math.sin(math.radians(2 * M)) * (0.019993 - 0.000101 * t) + math.sin(math.radians(3 * M)) * 0.000289)
    lam = L0 + C - 0.00569 - 0.00478 * math.sin(math.radians(125.04 - 1934.136 * t))
    eps0 = 23 + (26 + (21.448 - t * (46.815 + t * (0.00059 - t * 0.001813))) / 60) / 60
    eps = eps0 + 0.00256 * math.cos(math.radians(125.04 - 1934.136 * t))
    decl = math.degrees(math.asin(math.sin(math.radians(eps)) * math.sin(math.radians(lam))))
    y = math.tan(math.radians(eps / 2)) ** 2
    eot = 4 * math.degrees(y * math.sin(2 * math.radians(L0)) - 2 * e * math.sin(math.radians(M))
                           + 4 * e * y * math.sin(math.radians(M)) * math.cos(2 * math.radians(L0))
                           - 0.5 * y * y * math.sin(4 * math.radians(L0)) - 1.25 * e * e * math.sin(2 * math.radians(M)))
    cosH = (math.cos(math.radians(90.833)) / (math.cos(math.radians(lat)) * math.cos(math.radians(decl)))
            - math.tan(math.radians(lat)) * math.tan(math.radians(decl)))
    H = math.degrees(math.acos(cosH))
    noon = 720 - 4 * lon - eot
    return noon - 4 * H, noon + 4 * H, eot

def hm(m):
    m = m % 1440
    return f"{int(m // 60):02d}:{int(round(m % 60)) % 60:02d}"

out = {}
start = dt.date(2026, 11, 1)
days = [start + dt.timedelta(d) for d in range(120)]
for city, (lat, lon) in CITIES.items():
    rows = [(d, *events(d, lat, lon)) for d in days]
    es = min(rows, key=lambda r: r[2])
    ls = max(rows, key=lambda r: r[1])
    sd = min(rows, key=lambda r: r[2] - r[1])
    sol = [r for r in rows if r[0] == dt.date(2026, 12, 21)][0]
    jan5 = [r for r in rows if r[0] == dt.date(2027, 1, 5)][0]
    out[city] = {"earliest_sunset": str(es[0]), "earliest_sunset_utc": hm(es[2]),
                 "latest_sunrise": str(ls[0]), "latest_sunrise_utc": hm(ls[1]),
                 "shortest_day": str(sd[0]), "shortest_day_len_min": round(sd[2] - sd[1], 1),
                 "gap_days_sunset_to_sunrise": (ls[0] - es[0]).days,
                 "solstice_sunset_later_than_earliest_min": round(sol[2] - es[2], 1),
                 "jan5_day_longer_than_solstice_min": round((jan5[2] - jan5[1]) - (sol[2] - sol[1]), 1),
                 "jan5_morning_gain_min": round(sol[1] - jan5[1], 1),
                 "jan5_evening_gain_min": round(jan5[2] - sol[2], 1)}
    print(city, out[city])
json.dump(out, open(sys.argv[1] + "/results.json", "w"), indent=1)
