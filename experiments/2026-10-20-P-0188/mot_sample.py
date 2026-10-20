"""P-0188: EV v petrol MOT fail rates by mileage band, from DVSA's anonymised MOT results (2025 extract).
The zip is 4.8 GB, so it is read over HTTP range requests: the central directory first, then rows
streamed from one member until --rows is reached. Nothing large is written to disk.

Usage: mot_sample.py list
       mot_sample.py run MEMBER --rows 3000000
"""
import csv, io, sys, urllib.request, zipfile
from collections import defaultdict

URL = "https://edh-dvsa-data-gov-uk-files-prod.s3.eu-west-1.amazonaws.com/dft_test_result_extracts_2025.zip"
UA = "proteus-probe P-0188"
# --since YYYY-MM-DD keeps only cars first used on or after that date (an age control)
MIN_FIRST_USE = sys.argv[sys.argv.index("--since") + 1] if "--since" in sys.argv else ""


class HTTPRangeFile(io.RawIOBase):
    def __init__(self, url, block=8 << 20):
        self.url, self.pos, self.block = url, 0, block
        req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=60) as r:
            self.size = int(r.headers["Content-Length"])
        self.cache_start, self.cache = -1, b""
        self.fetched = 0

    def seekable(self): return True
    def readable(self): return True
    def tell(self): return self.pos

    def seek(self, off, whence=0):
        self.pos = off if whence == 0 else (self.pos + off if whence == 1 else self.size + off)
        return self.pos

    def _fill(self, start):
        end = min(start + self.block, self.size) - 1
        req = urllib.request.Request(self.url, headers={"User-Agent": UA, "Range": f"bytes={start}-{end}"})
        with urllib.request.urlopen(req, timeout=120) as r:
            self.cache = r.read()
        self.cache_start = start
        self.fetched += len(self.cache)

    def read(self, n=-1):
        if n is None or n < 0:
            n = self.size - self.pos
        out = bytearray()
        while n > 0 and self.pos < self.size:
            if not (self.cache_start <= self.pos < self.cache_start + len(self.cache)):
                self._fill(self.pos)
            i = self.pos - self.cache_start
            chunk = self.cache[i:i + n]
            out += chunk
            self.pos += len(chunk)
            n -= len(chunk)
        return bytes(out)

    def readinto(self, b):
        d = self.read(len(b))
        b[:len(d)] = d
        return len(d)


def band(miles):
    if miles < 30000: return "0-30k"
    if miles < 60000: return "30-60k"
    if miles < 90000: return "60-90k"
    if miles < 120000: return "90-120k"
    return "120k+"


def main():
    f = HTTPRangeFile(URL)
    z = zipfile.ZipFile(f)
    if sys.argv[1] == "list":
        for i in z.infolist():
            print(i.filename, i.compress_size, i.file_size)
        print("fetched bytes", f.fetched)
        return
    member, rows_cap = sys.argv[2], int(sys.argv[4]) if len(sys.argv) > 4 else 3_000_000
    f.block = 32 << 20
    with z.open(member) as raw:
        # a stray quote in a model or colour field swallowed the rest of the file on the first try
        rd = csv.reader(io.TextIOWrapper(raw, encoding="utf-8", errors="replace"), quoting=csv.QUOTE_NONE)
        head = [h.strip().lower() for h in next(rd)]
        print("columns", head)
        ix = {k: head.index(k) for k in ("test_class_id", "test_type", "test_result", "test_mileage", "fuel_type") if k in head}
        print("index", ix)
        n = 0
        tally = defaultdict(lambda: [0, 0])  # (fuel, band) -> [tests, fails]
        results, types, fuels = defaultdict(int), defaultdict(int), defaultdict(int)
        for row in rd:
            n += 1
            if n > rows_cap:
                break
            try:
                cls, typ, res, mil, fuel = (row[ix[k]] for k in ("test_class_id", "test_type", "test_result", "test_mileage", "fuel_type"))
            except (IndexError, KeyError):
                continue
            results[res] += 1; types[typ] += 1; fuels[fuel] += 1
            if cls != "4" or typ != "NT" or res not in ("P", "F", "PRS"):
                continue
            try:
                m = int(float(mil))
            except ValueError:
                continue
            if m <= 0:
                continue
            if MIN_FIRST_USE and row[13][:10] < MIN_FIRST_USE:
                continue
            t = tally[(fuel, band(m))]
            t[0] += 1
            if res in ("F", "PRS"):
                t[1] += 1
    print("rows read", n - 1, "bytes fetched", f.fetched)
    print("results", dict(results)); print("types", dict(types)); print("fuels", dict(fuels))
    print("\nclass 4 normal tests, fail = F or PRS (failed then passed after rectification at the test)")
    print("fuel  band      tests     fail%")
    for fuel in ("PE", "DI", "EL", "HY"):
        for b in ("0-30k", "30-60k", "60-90k", "90-120k", "120k+"):
            t, fl = tally.get((fuel, b), [0, 0])
            if t:
                print(f"{fuel:4}  {b:8} {t:8}  {100*fl/t:6.1f}")


main()
