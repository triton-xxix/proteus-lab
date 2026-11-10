"""P-0397 slice, my own code (auto-ontology-mcp itself was not run).

Its README says a model joins customers.customer_id = orders.order_id "because the integers happen to
overlap" and that a deterministic validator can reject that. Question underneath: on a public SQLite
database with declared foreign keys (Chinook), how often do integer columns overlap by accident, and
which deterministic signal separates a true key from an accident?

For every ordered pair (child column, parent primary key) of integer columns in different tables:
  containment = share of the child's distinct non-null values found in the parent key.
Truth = the declared foreign keys (PRAGMA foreign_key_list). Three rules are scored against it.
"""
import json, sqlite3, sys
from pathlib import Path

DB = sys.argv[1]
HERE = Path(__file__).resolve().parent
con = sqlite3.connect("file:" + DB + "?mode=ro", uri=True)
tables = [r[0] for r in con.execute("select name from sqlite_master where type='table' and name not like 'sqlite_%'")]

cols, pks, truth = {}, {}, set()
for t in tables:
    info = con.execute(f'pragma table_info("{t}")').fetchall()
    pk = [r[1] for r in info if r[5]]
    for r in info:
        if "INT" in (r[2] or "").upper():
            vals = {v[0] for v in con.execute(f'select distinct "{r[1]}" from "{t}" where "{r[1]}" is not null')}
            cols[(t, r[1])] = vals
    if len(pk) == 1 and (t, pk[0]) in cols:
        pks[t] = pk[0]
    for fk in con.execute(f'pragma foreign_key_list("{t}")'):
        truth.add((t, fk[3], fk[2], fk[4]))

pairs = []
for (ct, cc), cv in cols.items():
    if not cv:
        continue
    for pt, pc in pks.items():
        if pt == ct:
            continue
        pv = cols[(pt, pc)]
        cont = len(cv & pv) / len(cv)
        pairs.append({
            "child": f"{ct}.{cc}", "parent": f"{pt}.{pc}", "containment": round(cont, 3),
            "name_match": cc.lower() == pc.lower(),
            "child_is_own_pk": pks.get(ct) == cc,
            "true_fk": (ct, cc, pt, pc) in truth,
        })


def score(name, pred):
    tp = sum(1 for p in pairs if pred(p) and p["true_fk"])
    fp = sum(1 for p in pairs if pred(p) and not p["true_fk"])
    fn = sum(1 for p in pairs if not pred(p) and p["true_fk"])
    return {"rule": name, "flagged": tp + fp, "true": tp, "false": fp, "missed": fn,
            "precision": round(tp / (tp + fp), 3) if tp + fp else None,
            "recall": round(tp / (tp + fn), 3) if tp + fn else None}


rules = [
    score("containment 1.0 only", lambda p: p["containment"] == 1.0),
    score("containment >= 0.9", lambda p: p["containment"] >= 0.9),
    score("containment 1.0 and child is not its own table's key", lambda p: p["containment"] == 1.0 and not p["child_is_own_pk"]),
    score("containment 1.0 and same column name", lambda p: p["containment"] == 1.0 and p["name_match"]),
    score("same column name only", lambda p: p["name_match"]),
]
pk_to_pk = [p for p in pairs if p["child_is_own_pk"]]
res = {
    "db": "Chinook_Sqlite.sqlite (lerocha/chinook-database)", "tables": len(tables),
    "integer_columns": len(cols), "single_column_integer_keys": len(pks),
    "candidate_pairs": len(pairs), "declared_fks_in_pairs": sum(p["true_fk"] for p in pairs),
    "declared_fks_total": len(truth),
    "accidental_full_overlap": sum(1 for p in pairs if p["containment"] == 1.0 and not p["true_fk"]),
    "key_to_key_pairs": len(pk_to_pk),
    "key_to_key_full_overlap": sum(1 for p in pk_to_pk if p["containment"] == 1.0),
    "rules": rules,
    "accidents": [p for p in pairs if p["containment"] == 1.0 and not p["true_fk"]][:40],
    "missed_by_name_rule": [p for p in pairs if p["true_fk"] and not p["name_match"]],
}
(HERE / "results.json").write_text(json.dumps(res, indent=1))
for k, v in res.items():
    if k not in ("accidents",):
        print(k, json.dumps(v))
