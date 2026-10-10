"""P-0110: pre-listing, shorter hold. experiments/2026-10-09-prelisting/backtest.py run unchanged except:
- only three signals: bybit_spot, coinbase_trading, binance_spot_announce (every other signal left out);
- a signal is active for 7 days, not 14.
Same fit (TRAIN 9 Oct 2025 to 31 Mar 2026), same TEST (1 Apr to 24 Sep 2026), same costs, same
benchmarks (universe and 200 random lists). Fixed before the run. Inputs copied into this folder so
yesterday's backtest.json is not overwritten; writes backtest.json here.
"""
import os
import sys

sys.path.insert(0, "/Users/triton/PROTEUS/experiments/2026-10-09-prelisting")
import backtest as B  # noqa: E402

KEEP = {"bybit_spot", "coinbase_trading", "binance_spot_announce"}


class AllBut:
    def __contains__(self, name):
        return name not in KEEP


B.LEFT_OUT = AllBut()
B.ACTIVE = 7 * B.DAY
B.HERE = os.path.dirname(os.path.abspath(__file__))
B.run()
