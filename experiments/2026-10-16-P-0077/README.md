# P-0077, Keen's Minsky model rebuilt

Question: does private debt alone, in a rebuilt Goodwin-Keen model, produce the crash Keen says it predicted?

Method: `keen.py` integrates the three-variable model (wage share, employment, debt ratio) with scipy, 200 years, eight starting points, stopping at d=50 or employment 0.02. Parameters are the Grasselli and Costa Lima 2012 set as I remember them; I did not fetch the paper, so this is a rebuild, not a replication.

Numbers (`results.json`): five starts with d from 0.1 to 2.0 all settle at the same good equilibrium (wage share 0.836, employment 0.969, d about 0.07). d=4 settles too (d 0.197). d=6 and d=10 diverge, d past 50 at year 46 and year 23, employment down to 0.42 to 0.46.
So a crash needs a start of roughly 6 times annual output in debt; the called shot of d=2 was wrong.

Not done: the bad-equilibrium basin boundary between d=4 and 6, the paper's own parameters, any fit to real data (the 2008 prediction claim is untested).
