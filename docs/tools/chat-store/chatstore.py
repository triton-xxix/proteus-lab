#!/usr/bin/env python3
"""chatstore: turn Claude Code transcripts into one SQLite file you own.

Claude Code keeps every session as a JSONL file under
~/.claude/projects/<project-slug>/<session-id>.jsonl. Each line is a record;
the ones that matter here have "type" user or assistant and a "message" with a
role, a model, a list of content blocks (text, thinking, tool_use, tool_result)
and, for assistant turns, token usage. This script reads every such file under
one or more directories and writes a structured SQLite database:

    sessions(session_id, path, project, first_ts, last_ts, records, rows)
    turns(session_id, uuid, block_index, parent_uuid, ts, role, kind, model,
          text, tool_name, tool_use_id, input_tokens, output_tokens,
          cache_read_tokens, cache_write_tokens, request_id)

One row per content block. The primary key is (uuid, block_index), so a
record that appears twice (streamed partials are re-written as they grow)
keeps the last copy. Re-running on the same database is safe: rows are
replaced, not duplicated.

Keyless, stdlib only, read-only on the transcripts. The output database holds
everything you ever typed to the assistant and everything it answered, so keep
it out of any public repository.

Usage:
    python3 chatstore.py --out chats.sqlite ~/.claude/projects/my-project
    python3 chatstore.py --out chats.sqlite --summary summary.json DIR [DIR ...]
"""
import argparse
import json
import os
import sqlite3
import sys
import time

SCHEMA = """
CREATE TABLE IF NOT EXISTS sessions (
    session_id TEXT PRIMARY KEY,
    path TEXT,
    project TEXT,
    first_ts TEXT,
    last_ts TEXT,
    records INTEGER,
    rows INTEGER
);
CREATE TABLE IF NOT EXISTS turns (
    uuid TEXT NOT NULL,
    block_index INTEGER NOT NULL,
    session_id TEXT,
    parent_uuid TEXT,
    ts TEXT,
    role TEXT,
    kind TEXT,
    model TEXT,
    text TEXT,
    tool_name TEXT,
    tool_use_id TEXT,
    input_tokens INTEGER,
    output_tokens INTEGER,
    cache_read_tokens INTEGER,
    cache_write_tokens INTEGER,
    request_id TEXT,
    PRIMARY KEY (uuid, block_index)
);
CREATE INDEX IF NOT EXISTS turns_session_ts ON turns(session_id, ts);
CREATE INDEX IF NOT EXISTS turns_role_kind ON turns(role, kind);
"""


def block_text(block):
    """The readable text of one content block, whatever its kind."""
    if isinstance(block, str):
        return block
    kind = block.get("type")
    if kind == "text":
        return block.get("text") or ""
    if kind == "thinking":
        return block.get("thinking") or ""
    if kind == "tool_use":
        return json.dumps(block.get("input"), ensure_ascii=False)
    if kind == "tool_result":
        content = block.get("content")
        if isinstance(content, list):
            return "\n".join(block_text(b) for b in content)
        return content if isinstance(content, str) else json.dumps(content)
    return json.dumps(block, ensure_ascii=False)


def rows_from_record(rec):
    """Yield one tuple per content block of a user or assistant record."""
    msg = rec.get("message")
    if not isinstance(msg, dict):
        return
    role = msg.get("role") or rec.get("type")
    content = msg.get("content")
    if isinstance(content, str):
        content = [{"type": "text", "text": content}]
    if not isinstance(content, list):
        return
    usage = msg.get("usage") or {}
    model = msg.get("model")
    for i, block in enumerate(content):
        kind = block.get("type") if isinstance(block, dict) else "text"
        tool_name = block.get("name") if isinstance(block, dict) else None
        tool_use_id = None
        if isinstance(block, dict):
            tool_use_id = block.get("id") or block.get("tool_use_id")
        yield (
            rec.get("uuid"), i, rec.get("sessionId"), rec.get("parentUuid"),
            rec.get("timestamp"), role, kind, model, block_text(block),
            tool_name, tool_use_id,
            usage.get("input_tokens") if i == 0 else None,
            usage.get("output_tokens") if i == 0 else None,
            usage.get("cache_read_input_tokens") if i == 0 else None,
            usage.get("cache_creation_input_tokens") if i == 0 else None,
            rec.get("requestId"),
        )


def load_file(path, con):
    """Read one transcript file into the database; return (records, rows, first_ts, last_ts, skipped)."""
    records = rows = skipped = 0
    first_ts = last_ts = None
    session_id = os.path.splitext(os.path.basename(path))[0]
    batch = []
    with open(path, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                skipped += 1
                continue
            if rec.get("type") not in ("user", "assistant") or not rec.get("uuid"):
                skipped += 1
                continue
            records += 1
            ts = rec.get("timestamp")
            if ts:
                first_ts = ts if first_ts is None or ts < first_ts else first_ts
                last_ts = ts if last_ts is None or ts > last_ts else last_ts
            for row in rows_from_record(rec):
                batch.append(row if row[2] else row[:2] + (session_id,) + row[3:])
                rows += 1
            if len(batch) >= 2000:
                con.executemany("INSERT OR REPLACE INTO turns VALUES (" + ",".join("?" * 16) + ")", batch)
                batch = []
    if batch:
        con.executemany("INSERT OR REPLACE INTO turns VALUES (" + ",".join("?" * 16) + ")", batch)
    con.execute(
        "INSERT OR REPLACE INTO sessions VALUES (?,?,?,?,?,?,?)",
        (session_id, path, os.path.basename(os.path.dirname(path)), first_ts, last_ts, records, rows),
    )
    return records, rows, first_ts, last_ts, skipped


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("dirs", nargs="+", help="directories holding <session>.jsonl transcripts (searched one level deep)")
    ap.add_argument("--out", required=True, help="SQLite file to write (created or updated)")
    ap.add_argument("--summary", help="optional JSON file for the run's counts")
    args = ap.parse_args()

    t0 = time.time()
    for p in (args.out, args.summary):
        if p and os.path.dirname(p):
            os.makedirs(os.path.dirname(p), exist_ok=True)
    con = sqlite3.connect(args.out)
    con.executescript(SCHEMA)
    files = []
    for d in args.dirs:
        d = os.path.expanduser(d)
        if not os.path.isdir(d):
            print(f"not a directory: {d}", file=sys.stderr)
            continue
        for name in sorted(os.listdir(d)):
            if name.endswith(".jsonl"):
                files.append(os.path.join(d, name))
    tot_rec = tot_rows = tot_skip = 0
    for path in files:
        rec, rows, _, _, skipped = load_file(path, con)
        tot_rec += rec
        tot_rows += rows
        tot_skip += skipped
        con.commit()
    con.commit()
    n_sessions = con.execute("SELECT COUNT(*) FROM sessions").fetchone()[0]
    n_turns = con.execute("SELECT COUNT(*) FROM turns").fetchone()[0]
    by_kind = dict(con.execute("SELECT role || ':' || kind, COUNT(*) FROM turns GROUP BY 1 ORDER BY 2 DESC").fetchall())
    span = con.execute("SELECT MIN(first_ts), MAX(last_ts) FROM sessions").fetchone()
    con.close()
    summary = {
        "files": len(files), "sessions": n_sessions, "records": tot_rec, "rows_written": tot_rows,
        "turns_in_db": n_turns, "skipped_lines": tot_skip, "by_role_kind": by_kind,
        "first_ts": span[0], "last_ts": span[1],
        "db_bytes": os.path.getsize(args.out), "seconds": round(time.time() - t0, 2),
    }
    print(json.dumps(summary, indent=2))
    if args.summary:
        with open(args.summary, "w", encoding="utf-8") as fh:
            json.dump(summary, fh, indent=2)


if __name__ == "__main__":
    main()
