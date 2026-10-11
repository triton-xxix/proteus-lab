"""P-0127: does kolscan.io/leaderboard serve, keyless, 10+ wallets with a PnL figure in the raw HTML?

Reads the saved page (no JS run), looks for Solana wallet addresses and PnL-shaped numbers near them,
and writes result.json beside this script.
"""
import json
import re
import sys
from pathlib import Path

src = Path(sys.argv[1])
html = src.read_text(errors="replace")
out = Path(__file__).with_name("result.json")

addr_re = re.compile(r"(?<![1-9A-HJ-NP-Za-km-z])[1-9A-HJ-NP-Za-km-z]{32,44}(?![1-9A-HJ-NP-Za-km-z])")
addrs = []
for m in addr_re.finditer(html):
    a = m.group(0)
    if a not in addrs and re.search(r"\d", a) and re.search(r"[a-z]", a) and re.search(r"[A-Z]", a):
        addrs.append(a)

# Next.js pages often carry data in an escaped JSON blob; find records with a wallet and a pnl/profit field.
records = []
for m in re.finditer(r'\\?"(wallet_address|wallet|address)\\?"\s*:\s*\\?"([1-9A-HJ-NP-Za-km-z]{32,44})\\?"', html):
    window = html[m.start(): m.start() + 600]
    pnl = re.search(r'\\?"(pnl|profit|realized_profit|total_pnl|sol_pnl|usd_pnl)\\?"\s*:\s*(-?[\d.]+)', window)
    name = re.search(r'\\?"(name|twitter|username)\\?"\s*:\s*\\?"([^"\\]{1,40})', window)
    records.append({
        "wallet": m.group(2),
        "pnl_field": pnl.group(1) if pnl else None,
        "pnl": float(pnl.group(2)) if pnl else None,
        "name": name.group(2) if name else None,
    })

seen = set()
uniq = []
for r in records:
    if r["wallet"] in seen:
        continue
    seen.add(r["wallet"])
    uniq.append(r)

with_pnl = [r for r in uniq if r["pnl"] is not None]
visible_sol = re.findall(r"[+-]\s?[\d,.]+\s?Sol", html)

result = {
    "bytes": len(html),
    "has_next_data": "__NEXT_DATA__" in html or "self.__next_f" in html,
    "distinct_addresses_in_html": len(addrs),
    "wallet_records": len(uniq),
    "wallet_records_with_pnl": len(with_pnl),
    "visible_sol_figures": len(visible_sol),
    "sample": with_pnl[:10] or uniq[:10],
    "sample_visible": visible_sol[:10],
    "answer_10_plus_with_pnl": len(with_pnl) >= 10 or (len(addrs) >= 10 and len(visible_sol) >= 10),
}
out.write_text(json.dumps(result, indent=1))
print(json.dumps({k: v for k, v in result.items() if k != "sample"}, indent=1))
print("sample:", json.dumps(result["sample"][:5]))
