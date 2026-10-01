#!/usr/bin/env bash
# P-0044: build a 6 s test video with known answers, run motion-video-kit's frozen-time.sh and loudness.sh on it.
# Known answers, written before the run: seconds 3-6 are a still colour frame, so about 3.0 s near-frozen;
# audio is ffmpeg's sine at default amplitude 1/8 (peak -18.1 dBFS), 440 Hz mono, so integrated about -21.8 LUFS.
set -uo pipefail
EXP=/Users/triton/PROTEUS/experiments/2026-09-30-P-0044
KIT=/Users/triton/PROTEUS/sandbox/motion-video-kit/motion-video-kit-HEAD/business-motion-film/scripts
VID=/Users/triton/PROTEUS/sandbox/mvk-test.mp4
mkdir -p "$EXP"
echo "ffmpeg: $(command -v ffmpeg || echo MISSING)"
ffmpeg -hide_banner -loglevel error -y \
  -f lavfi -i "testsrc2=size=640x360:rate=25:duration=3" \
  -f lavfi -i "color=c=0x336699:size=640x360:rate=25:duration=3" \
  -f lavfi -i "sine=frequency=440:duration=6:sample_rate=48000" \
  -filter_complex "[0:v][1:v]concat=n=2:v=1:a=0[v]" -map "[v]" -map 2:a -c:v libx264 -pix_fmt yuv420p -c:a aac -b:a 192k "$VID"
echo "video: $(ls -l "$VID" | awk '{print $5}') bytes"
echo "== frozen-time.sh"
time bash "$KIT/frozen-time.sh" "$VID"
echo "== loudness.sh"
time bash "$KIT/loudness.sh" "$VID"
