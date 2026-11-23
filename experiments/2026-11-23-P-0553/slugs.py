"""List name, slug and param of every contract in one or more Smarkets contracts JSON files."""
import json, sys
for f in sys.argv[1:]:
    for c in sorted(json.load(open(f))["contracts"], key=lambda c: (c["market_id"], c["slug"])):
        flag = ""
        n = c["name"].replace("°C", "").split()[0]
        if n.startswith("-") and not c["slug"].startswith(("minus", "-", "neg", "m")):
            flag = "  <- minus sign in name, not in slug"
        print(c["market_id"], repr(c["name"]), c["slug"], c["contract_type"]["param"], c["state_or_outcome"], flag)
