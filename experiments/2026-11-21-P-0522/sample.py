"""P-0522: does DVSA's anonymised MOT data give an 8.4 point regional pass-rate spread for cars
first used 2015 to 2019 (MOTFaults claim: Scotland 81.4%, London 89.8%)?

The 2024 results zip is 1.5 GB. S3 serves byte ranges, so this reads the zip's central directory,
picks members, and streams only the first N MB of each through raw inflate. A sample, not the year.
Usage: sample.py [MB_PER_MEMBER] [MEMBERS]
"""
import csv
import io
import json
import os
import struct
import sys
import urllib.request
import zlib
from collections import defaultdict

URL = "https://edh-dvsa-data-gov-uk-files-prod.s3.eu-west-1.amazonaws.com/MOT+testing+data+results+(2024).zip"
HERE = os.path.dirname(os.path.abspath(__file__))
MB = int(sys.argv[1]) if len(sys.argv) > 1 else 40
NMEM = int(sys.argv[2]) if len(sys.argv) > 2 else 3

SCOTLAND = {"AB", "DD", "DG", "EH", "FK", "G", "HS", "IV", "KA", "KW", "KY", "ML", "PA", "PH", "TD", "ZE"}
LONDON = {"E", "EC", "N", "NW", "SE", "SW", "W", "WC"}
WALES = {"CF", "LD", "LL", "NP", "SA"}
NI = {"BT"}
NE = {"NE", "SR", "DH", "DL", "TS"}


def get(start, end):
    req = urllib.request.Request(URL, headers={"Range": "bytes=%d-%d" % (start, end),
                                               "User-Agent": "proteus-research/1.0"})
    return urllib.request.urlopen(req, timeout=120).read()


def members():
    head = urllib.request.urlopen(urllib.request.Request(URL, method="HEAD"), timeout=60)
    size = int(head.headers["Content-Length"])
    tail = get(size - 65536, size - 1)
    i = tail.rfind(b"PK\x05\x06")
    cd_size, cd_off = struct.unpack("<II", tail[i + 12:i + 20])
    if cd_off == 0xFFFFFFFF:  # zip64
        j = tail.rfind(b"PK\x06\x06")
        cd_size, cd_off = struct.unpack("<QQ", tail[j + 40:j + 56])
    cd = get(cd_off, cd_off + cd_size - 1)
    out, p = [], 0
    while p < len(cd) and cd[p:p + 4] == b"PK\x01\x02":
        method, = struct.unpack("<H", cd[p + 10:p + 12])
        csize, usize = struct.unpack("<II", cd[p + 20:p + 28])
        nlen, elen, clen = struct.unpack("<HHH", cd[p + 28:p + 34])
        loff, = struct.unpack("<I", cd[p + 42:p + 46])
        name = cd[p + 46:p + 46 + nlen].decode("utf-8", "replace")
        extra = cd[p + 46 + nlen:p + 46 + nlen + elen]
        if loff == 0xFFFFFFFF or csize == 0xFFFFFFFF:
            q = 0
            while q < len(extra):
                hid, hl = struct.unpack("<HH", extra[q:q + 4])
                if hid == 1:
                    vals = extra[q + 4:q + 4 + hl]
                    k = 0
                    if usize == 0xFFFFFFFF:
                        usize, = struct.unpack("<Q", vals[k:k + 8]); k += 8
                    if csize == 0xFFFFFFFF:
                        csize, = struct.unpack("<Q", vals[k:k + 8]); k += 8
                    if loff == 0xFFFFFFFF:
                        loff, = struct.unpack("<Q", vals[k:k + 8]); k += 8
                q += 4 + hl
        out.append({"name": name, "method": method, "csize": csize, "usize": usize, "loff": loff})
        p += 46 + nlen + elen + clen
    return size, out


def region(pc_area):
    a = (pc_area or "").strip().upper()
    if a in SCOTLAND:
        return "Scotland"
    if a in LONDON:
        return "London"
    if a in WALES:
        return "Wales"
    if a in NI:
        return "N Ireland"
    if a in NE:
        return "North East"
    return "rest of England"


def stream(m, mb):
    lh = get(m["loff"], m["loff"] + 29)
    nlen, elen = struct.unpack("<HH", lh[26:30])
    start = m["loff"] + 30 + nlen + elen
    want = min(m["csize"], mb * 1024 * 1024)
    raw = get(start, start + want - 1)
    d = zlib.decompressobj(-15)
    return d.decompress(raw).decode("utf-8", "replace")


def main():
    size, mems = members()
    csv.field_size_limit(10 ** 9)
    csvs = [m for m in mems if m["name"].lower().endswith((".csv", ".txt")) and "__MACOSX" not in m["name"]]
    print("zip", size, "bytes,", len(mems), "members:", [(m["name"], m["usize"]) for m in mems][:20])
    picks = csvs[:: max(1, len(csvs) // NMEM)][:NMEM]
    tally = defaultdict(lambda: defaultdict(int))
    header = None
    rows_read = 0
    for m in picks:
        text = stream(m, MB)
        lines = text.split("\n")[:-1]  # last line may be cut
        rdr = csv.reader(io.StringIO("\n".join(lines)), delimiter="," if lines[0].count(",") > lines[0].count("|") else "|",
                         quoting=csv.QUOTE_NONE)
        hdr = next(rdr)
        header = hdr
        idx = {h.strip().lower(): i for i, h in enumerate(hdr)}
        print(m["name"], "header", hdr)
        for r in rdr:
            if len(r) != len(hdr):
                continue
            rows_read += 1
            g = lambda k: r[idx[k]] if k in idx else ""
            if g("test_type") != "NT" or g("test_class_id") != "4":
                continue
            fu = g("first_use_date")[:4]
            if not ("2015" <= fu <= "2019"):
                continue
            res = g("test_result")
            reg = region(g("postcode_area"))
            tally[reg][res] += 1
            tally["ALL"][res] += 1
    out = {"zip_bytes": size, "members": [(m["name"], m["usize"]) for m in mems], "sampled": [m["name"] for m in picks],
           "mb_per_member": MB, "header": header, "rows_read": rows_read, "regions": {}}
    for reg, t in sorted(tally.items()):
        p, f, prs = t.get("P", 0), t.get("F", 0), t.get("PRS", 0)
        n = p + f + prs
        out["regions"][reg] = {"n": n, "P": p, "F": f, "PRS": prs, "other": {k: v for k, v in t.items() if k not in ("P", "F", "PRS")},
                               "pass_P_only": round(100 * p / n, 2) if n else None,
                               "pass_incl_PRS": round(100 * (p + prs) / n, 2) if n else None}
        print(reg, out["regions"][reg])
    with open(os.path.join(HERE, "results.json"), "w") as fh:
        json.dump(out, fh, indent=1)


main()
