"""Read the BoE MPC voting xlsx with zipfile + xml only. Print sheets, header rows, and the date column."""
import datetime as dt
import re
import sys
import zipfile
import xml.etree.ElementTree as ET

path = sys.argv[1]
z = zipfile.ZipFile(path)
names = z.namelist()
print("members:", [n for n in names if n.startswith("xl/")][:20])
NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
shared = []
if "xl/sharedStrings.xml" in names:
    root = ET.fromstring(z.read("xl/sharedStrings.xml"))
    for si in root.findall("m:si", NS):
        shared.append("".join(t.text or "" for t in si.iter("{%s}t" % NS["m"])))
wb = ET.fromstring(z.read("xl/workbook.xml"))
sheets = [(s.get("name"), s.get("{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id")) for s in wb.find("m:sheets", NS)]
print("sheets:", sheets)
rels = ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
rmap = {r.get("Id"): r.get("Target") for r in rels}

def excel_date(v):
    try:
        f = float(v)
    except Exception:
        return None
    if 20000 < f < 60000:
        return (dt.datetime(1899, 12, 30) + dt.timedelta(days=f)).date()
    return None

for name, rid in sheets:
    target = rmap[rid]
    if not target.startswith("/"):
        target = "xl/" + target
    else:
        target = target.lstrip("/")
    root = ET.fromstring(z.read(target))
    rows = []
    for row in root.iter("{%s}row" % NS["m"]):
        cells = []
        for c in row.findall("m:c", NS):
            v = c.find("m:v", NS)
            val = v.text if v is not None else ""
            if c.get("t") == "s" and val != "":
                val = shared[int(val)]
            cells.append(val)
        rows.append(cells)
    print("\n== sheet", name, "rows", len(rows))
    for r in rows[:8]:
        print("  ", r[:12])
    # find date-like cells in column A or any column
    dates = []
    for r in rows:
        for cell in r[:3]:
            d = excel_date(cell)
            if d:
                dates.append(d)
                break
    dates = sorted(set(dates))
    print("  date cells:", len(dates), "first", dates[:3], "last", dates[-3:])
    since09 = [d for d in dates if d >= dt.date(2009, 1, 1)]
    print("  since 2009-01-01:", len(since09))
    by_year = {}
    for d in since09:
        by_year[d.year] = by_year.get(d.year, 0) + 1
    print("  per year:", by_year)
    if since09 and name == "Bank Rate Decisions":
        out = sys.argv[2] if len(sys.argv) > 2 else None
        if out:
            with open(out, "w") as f:
                f.write("\n".join(d.isoformat() for d in since09) + "\n")
            print("  wrote", out)
