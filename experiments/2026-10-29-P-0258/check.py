"""Count what chatstore skipped, by record type, and spot-check the database."""
import collections
import json
import os
import sqlite3
import sys

src = sys.argv[1]
db = sys.argv[2]
types = collections.Counter()
for name in os.listdir(src):
    if not name.endswith(".jsonl"):
        continue
    with open(os.path.join(src, name), encoding="utf-8", errors="replace") as fh:
        for line in fh:
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                types["<bad json>"] += 1
                continue
            t = rec.get("type")
            if t in ("user", "assistant") and not rec.get("uuid"):
                t = t + " (no uuid)"
            types[t] += 1
print("record types:", json.dumps(types.most_common(), indent=1))

con = sqlite3.connect(db)
print("sessions with no rows:", con.execute("SELECT COUNT(*) FROM sessions WHERE rows=0").fetchone()[0])
print("output tokens by model:", con.execute(
    "SELECT model, SUM(output_tokens), COUNT(*) FROM turns WHERE output_tokens IS NOT NULL GROUP BY 1 ORDER BY 2 DESC").fetchall())
print("top tools:", con.execute(
    "SELECT tool_name, COUNT(*) FROM turns WHERE kind='tool_use' GROUP BY 1 ORDER BY 2 DESC LIMIT 8").fetchall())
print("longest user text chars:", con.execute(
    "SELECT MAX(LENGTH(text)) FROM turns WHERE role='user' AND kind='text'").fetchone()[0])
print("rows with empty text:", con.execute("SELECT COUNT(*) FROM turns WHERE text='' OR text IS NULL").fetchone()[0])
print("duplicate request ids collapsed:", con.execute(
    "SELECT COUNT(*) - COUNT(DISTINCT request_id) FROM turns WHERE request_id IS NOT NULL AND block_index=0").fetchone()[0])
