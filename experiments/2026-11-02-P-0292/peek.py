"""Dump raw rows of the Bank Rate sheet around the date rows, to see how votes sit beside the dates."""
import sys
import zipfile
import xml.etree.ElementTree as ET

NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
z = zipfile.ZipFile(sys.argv[1])
shared = []
root = ET.fromstring(z.read("xl/sharedStrings.xml"))
for si in root.findall("m:si", NS):
    shared.append("".join(t.text or "" for t in si.iter("{%s}t" % NS["m"])))
root = ET.fromstring(z.read("xl/worksheets/sheet1.xml"))
rows = []
for row in root.iter("{%s}row" % NS["m"]):
    cells = {}
    for c in row.findall("m:c", NS):
        v = c.find("m:v", NS)
        val = v.text if v is not None else ""
        if c.get("t") == "s" and val != "":
            val = shared[int(val)]
        cells[c.get("r")] = val
    rows.append((row.get("r"), cells))
lo, hi = int(sys.argv[2]), int(sys.argv[3])
for r, cells in rows[lo:hi]:
    print(r, {k: v for k, v in cells.items() if v != ""})
