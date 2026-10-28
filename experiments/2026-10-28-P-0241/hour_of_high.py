"""P-0241: by what local hour is Munich Stadt's daily high reached, last 60 complete days.

Source: DWD 10-minute air temperature, station 03379, recent zip (keyless). MESS_DATUM is UTC.
Local day = Europe/Berlin calendar day. High = max TT_10 (2 m); time = first 10-minute stamp at that max.
"""
import io, json, sys, zipfile
from collections import defaultdict
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

ZIP = sys.argv[1]
OUT = '/Users/triton/PROTEUS/experiments/2026-10-28-P-0241/results.json'
BER = ZoneInfo('Europe/Berlin')

z = zipfile.ZipFile(ZIP)
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

complete = sorted(d for d, v in days.items() if len(v) >= 140)  # 144 slots a day, allow a few gaps
last_day = complete[-1]
if len(days[last_day]) < 144 and last_day == max(days):
    complete = complete[:-1]
use = complete[-60:]
rows = []
for d in use:
    v = days[d]
    hi = max(t for _, t in v)
    when = min(ts for ts, t in v if t == hi)
    rows.append({'day': d.isoformat(), 'high': hi, 'at': when.strftime('%H:%M'),
                 'hour_frac': when.hour + when.minute / 60, 'n': len(v)})

hf = sorted(r['hour_frac'] for r in rows)
n = len(hf)
p90 = hf[min(n - 1, int(0.9 * n + 0.999) - 1)]
by = {h: sum(1 for x in hf if x <= h) for h in (12, 13, 14, 15, 16, 17, 18)}
early = [r for r in rows if r['hour_frac'] < 9]
late = [r for r in rows if r['hour_frac'] > 18]
hist = defaultdict(int)
for x in hf:
    hist[int(x)] += 1
res = {'station': '03379 Muenchen-Stadt', 'file': name, 'days': n, 'from': use[0].isoformat(), 'to': use[-1].isoformat(),
       'p90_local': f'{int(p90):02d}:{round(p90 % 1 * 60):02d}', 'median_local': hf[n // 2],
       'share_by_hour': {f'{h}:00': round(c / n, 3) for h, c in by.items()},
       'before_09': [(r['day'], r['at'], r['high']) for r in early],
       'after_18': [(r['day'], r['at'], r['high']) for r in late],
       'hist_by_hour': dict(sorted(hist.items())), 'rows': rows}
json.dump(res, open(OUT, 'w'), indent=1)
print({k: v for k, v in res.items() if k != 'rows'})
