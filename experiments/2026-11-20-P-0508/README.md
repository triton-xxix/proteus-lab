# P-0508: when did the mayhem burn sweep after 12:05Z run?

Question: P-0507 found 0 of 19 P-0491 coins burned by 13:00Z on 20 Nov at ages 24.3 to 24.4 hours, with
sweeps seen at 00:03:52Z (19 Nov) and 12:05:10Z (20 Nov). Re-read the 19 after 14:00Z: when did the
next sweep run, and is it twice a day?

Called shot (8f2c1ab2): works at 0.6, 17 or more of 19 burned in one sweep at about 00:04Z on 21 Nov,
none between 14:00 and 23:59Z. Made blind: I had not read the coins since P-0507's 12:58Z read.

## Method

`reread.py`: P-0507's `burns.py` check (newest signature of each mint, is it a burn) on the 19 mints in
P-0507's `recheck.json`, keyless Solana RPC. I meant it to wait until 00:09Z on 21 Nov; the script caps
its sleep at 600 s, so it read at 23:58:04Z on 20 Nov instead, before any 00:04Z sweep. That is fine for
the question asked (after 14:00Z) and is said here so the time is not misread.

## Numbers

- **18 of 19 burned, all in one 81-second cluster, 13:03:46 to 13:05:07Z on 20 Nov**, at ages 24.41 to
  24.52 hours. 19 of 19 had a newer signature than at 12:58Z.
- The one not burned (`Fszpxn44...`) has a newest signature at 19:08:42Z, age 30.5 hours, not a burn.
- Sweeps now on file: 00:03:52Z (19 Nov), 12:05:10Z (20 Nov), 13:03:46Z (20 Nov). So not twice a day:
  13:04 is an hour after 12:05. The fits so far say a sweep near four or five minutes past the hour
  that takes coins older than about 24.25 hours. Three sweeps; the hours between are unread.

Shot: the count held (18 against 17 or more) but the time was wrong by eleven hours; scored as a miss
on the sweep time.

## Not done

Did not read any hour other than these three, so "hourly" is a guess from two sweeps an hour apart.
Did not check what the 19:08Z transaction on the unburned coin was.
