"""P-0251: Munich airport (01262) v city (03379) daily high, same 60 complete local days.

DWD 10-minute air temperature, recent zips (keyless), read the way P-0241's hour_of_high.py reads them:
MESS_DATUM in UTC, local day Europe/Berlin, high = max TT_10, time = first stamp at that max.
Usage: python3 pair.py <01262 zip> <03379 zip>
"""
import io, json, sys, zipfile
from collections import defaultdict
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

BER = ZoneInfo('Europe/Berlin')
OUT = '/Users/triton/PROTEUS/experiments/2026-10-28-P-0251/results.json'


def highs(path):
    z = zipfile.ZipFile(path)
    name = [n for n in z.namelist() if n.startswith('produkt')][0]
    lines = io.TextIOWrapper(z.open(name), encoding='latin-1').read().splitlines()
    hdr = [h.strip() for h in lines[0].split(';')]
    iD, iT = hdr.index('MESS_DATUM'), hdr.index('TT_10')
    days = defaultdict(list)
    for ln in lines[1:]:
        f = [x.strip() for x in ln.split(';')]
        t = float(f[iT])
        if t <= -999:
            continue
        ts = datetime.strptime(f[iD], '%Y%m%d%H%M').replace(tzinfo=timezone.utc).astimezone(BER)
        days[ts.date()].append((ts, t))
    out = {}
    for d, v in days.items():
        if len(v) >= 140:
            hi = max(t for _, t in v)
            when = min(ts for ts, t in v if t == hi)
            out[d] = (hi, when.hour + when.minute / 60)
    return out


air, city = highs(sys.argv[1]), highs(sys.argv[2])
common = sorted(set(air) & set(city))
last = max(common)
if last >= datetime.now(BER).date():
    common = common[:-1]
use = common[-60:]
diff = [city[d][0] - air[d][0] for d in use]
n = len(use)
res = {'days': n, 'from': use[0].isoformat(), 'to': use[-1].isoformat(),
       'mean_city_minus_air': round(sum(diff) / n, 2),
       'share_abs_diff_ge_1': round(sum(abs(x) >= 1 for x in diff) / n, 3),
       'share_city_warmer': round(sum(x > 0 for x in diff) / n, 3),
       'share_same_rounded_degree': round(sum(round(city[d][0]) == round(air[d][0]) for d in use) / n, 3),
       'median_hour_air': sorted(air[d][1] for d in use)[n // 2],
       'median_hour_city': sorted(city[d][1] for d in use)[n // 2],
       'share_air_peak_later': round(sum(air[d][1] > city[d][1] for d in use) / n, 3),
       'rows': [{'day': d.isoformat(), 'city': city[d][0], 'air': air[d][0],
                 'city_hour': round(city[d][1], 2), 'air_hour': round(air[d][1], 2)} for d in use]}
json.dump(res, open(OUT, 'w'), indent=1)
print({k: v for k, v in res.items() if k != 'rows'})
