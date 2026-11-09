"""P-0376: fees.py saw 0 new blocks in 1,211 s. Was that the chain or my script?

Lists the last 8 blocks' timestamps and gaps, and the same blocks' fee extras, so the watch window can be
checked against the chain itself. Written after the watch ended; compares no recommendation with any block.
"""
import datetime as dt
import json
import pathlib
import urllib.request

HERE = pathlib.Path(__file__).parent
req = urllib.request.Request("https://mempool.space/api/v1/blocks", headers={"User-Agent": "proteus-lab/0.1"})
with urllib.request.urlopen(req, timeout=30) as r:
    blocks = json.load(r)
now = dt.datetime.now(dt.timezone.utc)
rows = []
for b, older in zip(blocks[:8], blocks[1:9]):
    ex = b.get("extras") or {}
    rows.append({"height": b["height"],
                 "mined_utc": dt.datetime.fromtimestamp(b["timestamp"], dt.timezone.utc).strftime("%H:%M:%S"),
                 "age_min": round((now.timestamp() - b["timestamp"]) / 60, 1),
                 "gap_to_previous_min": round((b["timestamp"] - older["timestamp"]) / 60, 1),
                 "median_fee": ex.get("medianFee"), "fee_range_min": (ex.get("feeRange") or [None])[0]})
out = {"checked_utc": now.isoformat(), "blocks": rows}
(HERE / "tipcheck.json").write_text(json.dumps(out, indent=1))
print(json.dumps(out, indent=1))
