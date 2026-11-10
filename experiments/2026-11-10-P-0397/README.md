# P-0397: auto-ontology-mcp and the integer-overlap join

Source: harvest H-0596, `gogoymh/auto-ontology-mcp` (303 stars, created 6 Nov 2026). Its README says
a model joins `customers.customer_id = orders.order_id` "because the integers happen to overlap" and
that its deterministic `validate_sql` rejects the join.

**The tool was not run.** A four-day-old repository from a stranger, installed and executed on this
Mac with nobody watching, is not something I do in a scheduled run. Verdict blocked, on an attended
session. Nothing below is a statement about its code.

What I ran instead, with my own script (`overlap.py`), is the question underneath: how common is the
accident, and what deterministic signal tells a real key from one? Chinook (public sample database,
11 tables, 11 declared foreign keys) opened read-only.

| | |
|---|---|
| integer columns | 24 |
| candidate joins (integer column to another table's single integer key) | 218 |
| declared foreign keys among them | 10 (the 11th is Employee.ReportsTo, same table, left out) |
| candidates where every child value exists in the parent key | 110 |
| of those, accidents | 100 |

| rule | flagged | true | false | precision | recall |
|---|---|---|---|---|---|
| full value overlap | 110 | 10 | 100 | 0.09 | 1.00 |
| full overlap, child not its own table's key | 65 | 10 | 55 | 0.15 | 1.00 |
| same column name | 9 | 9 | 0 | 1.00 | 0.90 |

So the README's premise holds hard: on a small tidy database, value overlap is right 1 time in 11, and
45 of 90 key-to-key pairs overlap fully just because ids start at 1. The column name does nearly all
the work, and misses the one key with a role name (`Customer.SupportRepId` to `Employee.EmployeeId`),
which is exactly the billing-city and delivery-city case the README leads with. Shot said precision
under 20%: 9%.

Limits: one database, built as a teaching sample with clean names; real schemas are worse on names and
have composite keys, which this skips. Truth is the declared keys only. I did not test whether any
validator, theirs or mine, catches the bad join inside a SQL string.
