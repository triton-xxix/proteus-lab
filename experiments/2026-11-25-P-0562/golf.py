"""P-0562: first-attempt MOT fail rate by model from the DVSA bulk results file.

Usage: python3 golf.py <dft_test_result_YYYY.zip> <first_use_year> <out.json>
Counts normal tests (test_type NT) on class 4 vehicles. A first-attempt fail is
F or PRS (failed, put right at the station within the hour), the DVSA's own
definition and the video's. Abandoned tests (ABA, ABR) are left out.
"""
import csv, io, json, sys, time, zipfile
from collections import defaultdict

src, year, out = sys.argv[1], sys.argv[2], sys.argv[3]
t0 = time.time()
z = zipfile.ZipFile(src)
names = [n for n in z.namelist() if not n.endswith('/')]
counts = defaultdict(lambda: [0, 0, 0])  # tests, F+PRS, F only
allage = [0, 0]
rows = 0
header = None
class D64(io.RawIOBase):
    """Stream one Deflate64 (method 9) member; Python's zipfile cannot (P-0562)."""
    def __init__(self, path, info):
        import inflate64, struct
        self.f = open(path, 'rb')
        self.f.seek(info.header_offset)
        h = self.f.read(30)
        n, m = struct.unpack('<HH', h[26:30])
        self.f.seek(info.header_offset + 30 + n + m)
        self.left = info.compress_size
        self.inf = inflate64.Inflater()
        self.buf = b''
    def readable(self):
        return True
    def readinto(self, b):
        while not self.buf and self.left > 0:
            chunk = self.f.read(min(8 << 20, self.left))
            self.left -= len(chunk)
            self.buf = self.inf.inflate(chunk)
        k = min(len(b), len(self.buf))
        b[:k] = self.buf[:k]
        self.buf = self.buf[k:]
        return k


for name in names:
    info = z.getinfo(name)
    raw = D64(src, info) if info.compress_type == 9 else z.open(name)
    with io.BufferedReader(raw, 1 << 20) as fh:
        text = io.TextIOWrapper(fh, encoding='utf-8', errors='replace', newline='')
        first = text.readline()
        delim = '|' if first.count('|') > first.count(',') else ','
        cols = [c.strip().lower() for c in first.strip().split(delim)]
        header = cols
        i = {c: k for k, c in enumerate(cols)}
        for r in csv.reader(text, delimiter=delim):
            rows += 1
            if len(r) < len(cols):
                continue
            if r[i['test_type']] != 'NT' or r[i['test_class_id']] != '4':
                continue
            if not r[i['first_use_date']].startswith(year):
                continue
            res = r[i['test_result']]
            if res not in ('P', 'F', 'PRS'):
                continue
            fail = res in ('F', 'PRS')
            allage[0] += 1
            allage[1] += fail
            key = (r[i['make']].upper(), r[i['model']].upper())
            c = counts[key]
            c[0] += 1
            c[1] += fail
            c[2] += res == 'F'

top = sorted(((k, v) for k, v in counts.items() if v[0] >= 2500), key=lambda kv: kv[1][1] / kv[1][0])
golf = counts.get(('VOLKSWAGEN', 'GOLF'), [0, 0, 0])
result = {
    'source': src.split('/')[-1], 'first_use_year': year, 'rows_read': rows, 'header': header,
    'seconds': round(time.time() - t0, 1),
    'all_cars_this_age': {'tests': allage[0], 'first_fail_pct': round(100 * allage[1] / max(allage[0], 1), 2)},
    'golf': {'tests': golf[0], 'first_fail_pct': round(100 * golf[1] / max(golf[0], 1), 2),
             'still_fail_pct': round(100 * golf[2] / max(golf[0], 1), 2)},
    'golf_rank_lowest_fail_of_models_2500plus': [k for k, _ in top].index(('VOLKSWAGEN', 'GOLF')) + 1 if golf[0] >= 2500 else None,
    'models_2500plus': len(top),
    'best10': [[f'{k[0]} {k[1]}', v[0], round(100 * v[1] / v[0], 2)] for k, v in top[:10]],
    'worst5': [[f'{k[0]} {k[1]}', v[0], round(100 * v[1] / v[0], 2)] for k, v in top[-5:]],
}
json.dump(result, open(out, 'w'), indent=1)
print(json.dumps({k: result[k] for k in ('rows_read', 'seconds', 'all_cars_this_age', 'golf', 'golf_rank_lowest_fail_of_models_2500plus', 'models_2500plus')}))
