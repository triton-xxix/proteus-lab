# P-0160 mcd-saver-strategist

Fetched the repo tarball into sandbox/mcd-saver-strategist (Python script, no git clone).

- `selftest.py`: 19 passed, 0 failed (12 groups: price overrides, threshold discounts, bundle price, gift thresholds, exclusivity, end-to-end, budget, calories, determinism, channel filter, delivery fee).
- `optimizer.py` on the bundled sample: Big Mac meal 47.00 -> 21.90 yuan (saves 25.10, 53%) using the 1+1 bundle coupon, 13 feasible plans evaluated, top five shown. Matches the README claim exactly.
- Caveat: sample data only. The live menu and coupons need the vendor's MCP token, so the real-world saving is untested. A self-test asserts 22.0 as the best price while the optimiser prints 21.90 on the sample, a different fixture.
- Not run: perturbing the coupons to test exclusivity beyond the shipped selftests.
