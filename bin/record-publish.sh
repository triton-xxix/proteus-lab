#!/usr/bin/env bash
# Copy the finished Sixteen Nights page, engine, assets, record and film into docs/record/ for
# GitHub Pages. Raw generations (lab/), the HyperFrames project (film/), node_modules and the
# build scripts stay out of docs. Idempotent; run after page.py and the film render.
set -euo pipefail
B=/Users/triton/PROTEUS/sites/builds/sixteen-nights
D=/Users/triton/PROTEUS/docs/record
mkdir -p "$D/assets" "$D/fonts"
cp "$B/index.html" "$B/scrollcraft.js" "$B/scrollcraft.css" "$B/record.json" "$D/"
cp "$B"/assets/*.mp4 "$B"/assets/*.jpg "$B"/assets/*.png "$D/assets/"
if [ -f "$B/film/out/film-web.mp4" ]; then cp "$B/film/out/film-web.mp4" "$D/film.mp4"; fi
if [ -d "$B/film/fonts" ]; then cp "$B"/film/fonts/*.woff2 "$B/film/fonts/fonts.css" "$D/fonts/" 2>/dev/null || true; fi
du -sh "$D"; ls -la "$D" "$D/assets"
