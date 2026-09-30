# P-0044: motion-video-kit, do frozen-time and loudness run keyless and give numbers?

Run 30 Sep 2026, scheduled nightly, attempt 1 of 3. Repo `echris6/motion-video-kit` pulled as a
codeload tarball (git clone is not an unattended verb), 29 entries. Both scripts are short ffmpeg
pipelines, read in full before running. Wrapper: `sandbox/mvk_probe.sh` (copied below).

## Test video with known answers, written before the run

6 s, 640x360, 25 fps: 3 s of `testsrc2` (moving pattern) then 3 s of a still colour frame. Audio
is a 440 Hz mono sine at ffmpeg's default amplitude of 1/8. Predicted: about 3.0 s near-frozen;
integrated loudness about -21.8 LUFS (sine RMS -21.1 dBFS, minus 0.691), peak about -18.1 dBFS.

## Measured

| check | predicted | script said | time |
|---|---|---|---|
| near-frozen | about 3.0 s, from 3.0 | 29 samples, 2.9 s, first at 3.1 | 0.22 s |
| integrated loudness | -21.8 LUFS | -21.8 LUFS | 0.17 s |
| loudness range | 0 LU | 0.0 LU | |
| peak | -18.1 dBFS | -17.7 dBFS (true peak) | |

- The 0.1 s shortfall on frozen time is how the script counts: `tblend` compares each frame with
  the one before, and the last sample falls off the end.
- The 0.4 dB peak difference is true-peak oversampling on the AAC-encoded sine, not a script error.
- Minor flaw: the short-term column is blank for seconds 0 to 2. Short-term loudness has a 3 s
  window and the script's pattern does not match what ffmpeg prints before it fills.

## Verdict

Works: keyless, needs only ffmpeg (on this Mac at /usr/local/bin), exact on the loudness and within
a sample on the freeze. Worth lifting both checks into the HyperFrames render QA as they stand.

## Wrapper

```bash
ffmpeg -f lavfi -i "testsrc2=size=640x360:rate=25:duration=3" \
  -f lavfi -i "color=c=0x336699:size=640x360:rate=25:duration=3" \
  -f lavfi -i "sine=frequency=440:duration=6:sample_rate=48000" \
  -filter_complex "[0:v][1:v]concat=n=2:v=1:a=0[v]" -map "[v]" -map 2:a \
  -c:v libx264 -pix_fmt yuv420p -c:a aac -b:a 192k mvk-test.mp4
bash scripts/frozen-time.sh mvk-test.mp4
bash scripts/loudness.sh mvk-test.mp4
```
