"""P-0408: P-0397's key-discovery rules on two more public SQLite samples, Northwind and Sakila.

Same rules as experiments/2026-11-10-P-0397/overlap.py: for every ordered pair (integer child
column, another table's single integer primary key), containment = share of the child's distinct
non-null values found in the parent key. Truth = declared foreign keys (PRAGMA foreign_key_list).

The databases are downloaded as data into their own folders under sandbox/ (gitignored) and opened
read-only; nothing in them is executed. Usage: two.py fetch | two.py score
"""
import hashlib, json, os, sqlite3, sys, urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
SANDBOX = Path("/Users/triton/PROTEUS/sandbox")
DBS = {
    "northwind": ("https://github.com/jpwhite3/northwind-SQLite3/raw/main/dist/northwind.db", SANDBOX / "p0408-northwind" / "northwind.db"),
    "sakila": ("https://github.com/bradleygrant/sakila-sqlite3/raw/main/sakila_master.db", SANDBOX / "p0408-sakila" / "sakila_master.db"),
}


def fetch():
    for name, (url, path) in DBS.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        data = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "proteus-research/1.0"}), timeout=120).read()
        path.write_bytes(data)
        print(name, len(data), "bytes", hashlib.sha256(data).hexdigest()[:16], data[:15])


def one(name, path):
    con = sqlite3.connect("file:" + str(path) + "?mode=ro", uri=True)
    tables = [r[0] for r in con.execute("select name from sqlite_master where type='table' and name not like 'sqlite_%'")]
    cols, pks, raw_fk, all_pk = {}, {}, [], {}
    for t in tables:
        info = con.execute(f'pragma table_info("{t}")').fetchall()
        pk = [r[1] for r in info if r[5]]
        all_pk[t] = pk
        for r in info:
            if "INT" in (r[2] or "").upper():
                vals = {v[0] for v in con.execute(f'select distinct "{r[1]}" from "{t}" where "{r[1]}" is not null')}
                cols[(t, r[1])] = vals
        if len(pk) == 1 and (t, pk[0]) in cols:
            pks[t] = pk[0]
        for fk in con.execute(f'pragma foreign_key_list("{t}")'):
            raw_fk.append((t, fk[3], fk[2], fk[4]))
    # a foreign key declared without a parent column points at the parent's primary key; table
    # names in a REFERENCES clause are case-insensitive in SQLite
    by_lower = {t.lower(): t for t in tables}
    truth = set()
    for ct, cc, pt, pc in raw_fk:
        pt = by_lower.get(pt.lower(), pt)
        if pc is None and len(all_pk.get(pt, [])) == 1:
            pc = all_pk[pt][0]
        truth.add((ct, cc, pt, pc))
    pairs = []
    for (ct, cc), cv in cols.items():
        if not cv:
            continue
        for pt, pc in pks.items():
            if pt == ct:
                continue
            cont = len(cv & cols[(pt, pc)]) / len(cv)
            pairs.append({"child": f"{ct}.{cc}", "parent": f"{pt}.{pc}", "containment": round(cont, 3),
                          "name_match": cc.lower() == pc.lower(), "child_is_own_pk": pks.get(ct) == cc,
                          "true_fk": (ct, cc, pt, pc) in truth})

    def score(label, pred):
        tp = sum(1 for p in pairs if pred(p) and p["true_fk"])
        fp = sum(1 for p in pairs if pred(p) and not p["true_fk"])
        fn = sum(1 for p in pairs if not pred(p) and p["true_fk"])
        return {"rule": label, "flagged": tp + fp, "true": tp, "false": fp, "missed": fn,
                "precision": round(tp / (tp + fp), 3) if tp + fp else None,
                "recall": round(tp / (tp + fn), 3) if tp + fn else None}

    return {
        "db": name, "tables": len(tables), "integer_columns": len(cols), "single_column_integer_keys": len(pks),
        "candidate_pairs": len(pairs), "declared_fks_total": len(truth),
        "declared_fks_in_pairs": sum(p["true_fk"] for p in pairs),
        "declared_fks_outside_pairs": sorted(".".join(map(str, x[:2])) + " -> " + ".".join(map(str, x[2:])) for x in truth
                                             if not any(p["true_fk"] and p["child"] == f"{x[0]}.{x[1]}" and p["parent"] == f"{x[2]}.{x[3]}" for p in pairs)),
        "full_overlap": sum(1 for p in pairs if p["containment"] == 1.0),
        "accidental_full_overlap": sum(1 for p in pairs if p["containment"] == 1.0 and not p["true_fk"]),
        "rules": [
            score("containment 1.0 only", lambda p: p["containment"] == 1.0),
            score("containment 1.0 and child is not its own table's key", lambda p: p["containment"] == 1.0 and not p["child_is_own_pk"]),
            score("containment 1.0 and same column name", lambda p: p["containment"] == 1.0 and p["name_match"]),
            score("same column name only", lambda p: p["name_match"]),
        ],
        "true_fk_below_full_overlap": [p for p in pairs if p["true_fk"] and p["containment"] < 1.0],
        "missed_by_name_rule": [p for p in pairs if p["true_fk"] and not p["name_match"]],
        "false_by_name_rule": [p for p in pairs if p["name_match"] and not p["true_fk"]],
    }


if sys.argv[1:] == ["fetch"]:
    fetch()
else:
    out = {name: one(name, path) for name, (_, path) in DBS.items()}
    (HERE / "results.json").write_text(json.dumps(out, indent=1))
    print(json.dumps(out, indent=1))
