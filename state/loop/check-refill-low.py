"""Smith 23 Oct 2026, F-0043: check unused_refill_rows and the LOW threshold without opening a loop."""
import importlib.util
spec = importlib.util.spec_from_file_location("probe", "/Users/triton/PROTEUS/bin/probe.py")
p = importlib.util.module_from_spec(spec)
spec.loader.exec_module(p)
rows = p.unused_refill_rows()
print("unused rows:", [r[0] for r in rows])
print("next:", p.next_refill_source()[0] if p.next_refill_source() else None)
spare = len(rows) - 1
print("LOW would print:", spare < p.REFILL_LOW_ROWS, "(spare %d, line %d)" % (spare, p.REFILL_LOW_ROWS))   # REFILL_MAX gone 29 Oct 2026, F-0051
print("SOURCES would print (reserve %d):" % p.REFILL_RESERVE, spare < p.REFILL_RESERVE)
