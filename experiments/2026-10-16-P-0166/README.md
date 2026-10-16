# P-0166, the retest rule on two years of NQ 1h bars (16 Oct 2026)

Queued tonight by the harvest from a vault thread (H-0294): rerun the @grandmasterbey retest rule on
two years of hourly Nasdaq futures bars and see whether it still beats 95% of random-entry runs.

Not run, for two reasons found in this folder before writing any code:

1. **Luke has already said no to this test.** The vault side's brief of today,
   `briefs/2026-10-16-bey-retest-forward-paper.md`, records that he does not want a two-year backtest
   ("what was working years ago may not work today") and agreed a forward paper test instead: the rules
   frozen as in `briefs/2026-10-16-bey-retest/bey_bt.py`, logged from now, about 30 trades in four weeks.
   The harvest child judged the thread without that brief, so it queued the test he declined.
2. **The rule is a 15-minute rule.** Swings, the close beyond them and the 8-bar retest window are all
   counted in 15-minute bars, with exits on 5-minute bars. On 1-hour bars every one of those changes
   meaning, so a pass or a fail would be about a different rule. yfinance serves 15m bars for about 60
   days only, which is why the vault's run stopped at 10 weeks.

Verdict: not worth it. The useful version is the forward paper book the brief describes. It needs a
frozen rule file, a pass mark and a due date committed before its first trade (the
preregister-a-book skill), and a scheduled logger; that is a book to start in a daytime slot, not a
probe to squeeze into the nightly. Left for a daytime slot through tonight's run log; not written into
BACKLOG.md, which another session has open with uncommitted changes.
