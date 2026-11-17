"""Builds docs/tools/pump-trades/index.html from committed files, never typed numbers:
- run-2026-11-17.json: the tool's own run on live pump.fun transactions;
- experiments/2026-11-17-P-0464/results.json and experiments/2026-11-17-P-0465/results.json: the probes.
Exits if the run's rows disagree with its own summary, any tail failed to decode, or a paid fee fails.
python3 -I /Users/triton/PROTEUS/docs/tools/pump-trades/build.py"""
import json
import sys
from collections import Counter

R = "/Users/triton/PROTEUS/"
D = R + "docs/tools/pump-trades/"
RUN = json.load(open(D + "run-2026-11-17.json"))
P464 = json.load(open(R + "experiments/2026-11-17-P-0464/results.json"))["summary"]
P465 = json.load(open(R + "experiments/2026-11-17-P-0465/results.json"))["summary"]
rows, s = RUN["rows"], RUN["summary"]

if len(rows) != s["trades"]:
    sys.exit("rows %d v summary %d" % (len(rows), s["trades"]))
if dict(Counter(r["fee_class"] for r in rows)) != s["fee_classes"]:
    sys.exit("fee classes differ from the summary")
if s["tails"] != {"ok": len(rows)}:
    sys.exit("tails not all ok: %s" % s["tails"])
if s["fee_ok_paid"] != s["paid"]:
    sys.exit("%d of %d paid fees fail" % (s["paid"] - s["fee_ok_paid"], s["paid"]))

N, FREE, PAID, MAY = s["trades"], s["no_fee"], s["paid"], s["mayhem"]
MF, MP = s["mayhem_no_fee"], s["mayhem_paid"]
free_not_mayhem = FREE - MF
p464_zero = P464["fee_bps_seen"].get("0", 0)
p465_zero, p465_zero_may = P465["zero_fee"]["n"], P465["zero_fee"]["mayhem"].get("True", 0)
p465_paid, p465_paid_may = P465["paid_fee"]["n"], P465["paid_fee"]["mayhem"].get("True", 0)
quote_rows = [r for r in rows if not r["sol_quote"]]
quote_paid = [r for r in quote_rows if r["fee_class"] != "no fee"]


def esc(x):
    return str(x).replace("&", "&amp;").replace("<", "&lt;").replace('"', "&quot;")


def cls(r):
    return "nf" if r["fee_class"] == "no fee" else ("p2" if r["creator_fee_bps"] != 30 else "pd")


# 1. a square per trade, mayhem marked with a ring
sq = "".join('<i class="%s%s" title="%s %s, %s, %s%s"></i>'
             % (cls(r), " my" if r.get("mayhem") else "", esc(r.get("ix_name", "-")),
                "%.4f SOL" % (r["sol_amount"] / 1e9) if r["sol_amount"] else "%d quote units" % r.get("quote_amount", 0),
                esc(r["fee_class"]), "mayhem" if r.get("mayhem") else "normal",
                "" if r["sol_quote"] else ", non-SOL quote")
             for r in sorted(rows, key=lambda r: (cls(r), not r.get("mayhem"), r["timestamp"])))

# 2. mayhem by fee, as 100% bars
def bar(label, free, paid):
    t = free + paid
    return ('<div class="row"><span class="nm">%s</span><span class="tr">'
            '<b class="nf" style="width:%.1f%%" title="no fee %d"></b><b class="pd" style="width:%.1f%%" title="paid %d"></b>'
            '</span><span class="ct">%d</span></div>' % (label, 100.0 * free / t if t else 0, free,
                                                            100.0 * paid / t if t else 0, paid, t))


bars = bar("Mayhem mode", MF, MP) + bar("Normal", free_not_mayhem, PAID - MP)
p_bars = (bar("P-0465 mayhem", p465_zero_may, p465_paid_may)
          + bar("P-0465 normal", p465_zero - p465_zero_may, p465_paid - p465_paid_may))

ix_list = ", ".join("%s %d" % (esc(k), v) for k, v in s["ix_names"].items())
fee_list = ", ".join("%s %d" % (esc(k), v) for k, v in s["fee_classes"].items())
qp = quote_paid[0] if quote_paid else None
QUOTE = ""
if qp:
    QUOTE = (f"<p>One thing the first run caught. {len(quote_rows)} of {N} trades are quoted in a token other than SOL, so "
             f"<code>sol_amount</code> is 0 and the fee cannot be a share of it. On the paid one the fee is "
             f"{qp['fee']:,} and {qp['fee_bps']} bps of its <code>quote_amount</code> ({qp['quote_amount']:,}) is "
             f"{qp['quote_amount'] * qp['fee_bps'] / 10000:,.0f}: the fee is charged in the quote token. The tool now checks it that way, "
             f"and {s['fee_ok_paid']} of {PAID} paid fees agree to the unit.</p>")

page = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Pump Trades</title>
<meta name="description" content="Decode every pump.fun trade event from the public Solana RPC, keyless, and check each fee. One standard-library Python file.">
<style>
:root{{--bg:#fbfaf7;--fg:#1d1c1a;--mut:#6b675f;--line:#dedad2;--a:#2a6f97;--pd:#2a6f97;--p2:#7b5ea7;--nf:#c4622d;--ring:#1d1c1a;--card:#fff}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#151513;--fg:#ecebe6;--mut:#a29e95;--line:#34322e;--a:#6fb3d9;--pd:#6fb3d9;--p2:#b79be0;--nf:#e8935f;--ring:#ecebe6;--card:#1d1c1a}}}}
:root[data-theme="dark"]{{--bg:#151513;--fg:#ecebe6;--mut:#a29e95;--line:#34322e;--a:#6fb3d9;--pd:#6fb3d9;--p2:#b79be0;--nf:#e8935f;--ring:#ecebe6;--card:#1d1c1a}}
body{{background:var(--bg);color:var(--fg);font:16px/1.55 system-ui,-apple-system,sans-serif;margin:0}}
main{{max-width:820px;margin:0 auto;padding:24px 16px 60px}}
a{{color:var(--a)}} h1{{font-size:1.9rem;line-height:1.2;margin:.4em 0}} h2{{font-size:1.2rem;margin-top:2em}}
.mut{{color:var(--mut)}} .big{{font-size:1.15rem}}
.pd{{background:var(--pd)}} .p2{{background:var(--p2)}} .nf{{background:var(--nf)}}
.sq{{display:grid;grid-template-columns:repeat(19,1fr);gap:4px;margin:12px 0}}
.sq i{{display:block;aspect-ratio:1;border-radius:3px}}
.sq i.my{{box-shadow:inset 0 0 0 2px var(--ring)}}
.key i{{display:inline-block;width:11px;height:11px;border-radius:2px;vertical-align:-1px;margin:0 5px 0 12px}}
.key i:first-child{{margin-left:0}} .key i.my{{background:transparent;box-shadow:inset 0 0 0 2px var(--ring)}}
.row{{display:flex;align-items:center;gap:8px;margin:5px 0;font-size:14px}}
.nm{{flex:0 0 32%;min-width:0;overflow-wrap:anywhere}} .tr{{flex:1;display:flex;height:16px;min-width:0}}
.tr b{{display:block;height:100%}} .ct{{flex:0 0 3em;text-align:right;font-variant-numeric:tabular-nums}}
pre{{background:var(--card);border:1px solid var(--line);padding:12px;overflow-x:auto;font-size:13.5px}}
code{{overflow-wrap:anywhere}}
</style></head><body><main>
<p class="mut"><a href="../../index.html">Proteus lab</a> / tools / pump-trades</p>
<h1>Every pump.fun trade logs its own receipt. Here is how to read it.</h1>
<p class="big">Each trade on pump.fun writes an event into the transaction: what was paid, what came back, the fee in basis points and in lamports. This one file pulls the latest transactions from Solana's public RPC, no key, decodes every event, and checks each fee against the amount. On {esc(s["at"][:10])} at {esc(s["at"][11:16])} UTC, {s["transactions"]} transactions held {N} trades across {s["mints"]} tokens, and {FREE} of the {N} paid no fee at all.</p>

<div class="sq" role="img" aria-label="{N} trades: {PAID} paid a fee, {FREE} paid none; {MAY} in mayhem mode">{sq}</div>
<p class="key mut"><i class="pd"></i>paid 95 + 30 bps<i class="p2"></i>paid another split<i class="nf"></i>no fee<i class="my"></i>mayhem mode</p>
<p class="mut">One square per trade. Hover for the instruction, the size and the fee. Fee classes: {fee_list}. Instructions: {ix_list}.</p>

<h2>The free trades are all in mayhem mode</h2>
<p>{MF} of the {FREE} no-fee trades carry the event's <code>mayhem_mode</code> flag{"" if free_not_mayhem else ", every one"}. But mayhem mode does not mean free: {MP} of the {MAY} mayhem trades paid the normal fee. So the flag is necessary on this sample, not sufficient.</p>
{bars}
<p class="key mut"><i class="nf"></i>no fee<i class="pd"></i>paid</p>
<p>The probe that found it, a few hours earlier on a smaller sample, saw the same shape:</p>
{p_bars}
<p class="mut">The first probe (P-0464) saw {p464_zero} zero-fee trades out of {P464["paired"]} and could not say why; the second (P-0465) decoded past the instruction name and found the mayhem flag. Neither the event nor this tool can say whether the fee is truly waived or taken somewhere the event does not report. The SOL balance changes of those transactions would tell, and that is the next probe, not this page.</p>

<h2>The fee check</h2>
<p>For every trade that paid, the tool checks <code>fee</code> against amount × <code>fee_basis_points</code> / 10,000 and the creator fee the same way, to within one unit. {s["fee_ok_paid"]} of {PAID} agree.</p>
{QUOTE}
<p>{s["sol_volume"]:.2f} SOL traded on the SOL-quoted trades in the sample, {s["fees_sol"]:.4f} SOL of it fees. {s["fetch_failed"]} of the transactions the RPC listed could not be fetched (the public node drops recent ones and rate-limits); the tool skips them and says how many.</p>

<h2>Use it</h2>
<pre>python3 pump_trades.py
python3 pump_trades.py --n 300 --out run.json --csv trades.csv
python3 pump_trades.py --rpc https://your.rpc/ --n 1000
python3 pump_trades.py --from run.json</pre>
<p>Standard library only, no key. About a quarter of a second per transaction on the public RPC; give it your own RPC for more. <code>--from</code> re-scores a saved run without fetching. Every field is kept raw: the buyback field can read 5000 bps, which is a share of the fee and not half the trade, so the tool never adds the bps fields into one total.</p>
<p><a href="pump_trades.py">pump_trades.py</a> · <a href="run-2026-11-17.json">today's {N} trades</a> · <a href="README.md">README</a> · <a href="build.py">how this page is built</a></p>
<p class="mut">Checked: the page does not build unless the run's rows agree with its own summary, every event decoded to the end, and every paid fee checks. The layout is pump.fun's public IDL, read by probes P-0464 and P-0465. {N} trades from one minute is a small sample. Not yet checked at phone width in a real browser. A snapshot of {esc(s["at"][:10])}; nothing rebuilds it yet.</p>
</main></body></html>
"""
open(D + "index.html", "w").write(page)
print("built", len(page), "bytes | trades", N, "free", FREE, "mayhem free", MF, "mayhem paid", MP, "| fee ok", s["fee_ok_paid"], "of",
      PAID, "| non-SOL quote", len(quote_rows), "| p464 zero", p464_zero, "| p465", p465_zero, p465_zero_may)
