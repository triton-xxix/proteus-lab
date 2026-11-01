# P-0288 huashu-bird-sticker: 11,064 records, 43 languages, a sticker each?

Source: github.com/alchaincyf/huashu-bird-sticker (496 stars), 1 Nov 2026. `check.py` reads the
full git tree (not truncated, 11,114 files) and downloads `data/species.json` (33.7 MB) raw.

Measured (`results.json`):
- `data/species.json` holds 11,064 records, matching the claim. Fields: id, ids, scientificName,
  authority, names, zh, taxonomy, traits, range, conservation, subspecies, sticker.
- `stickers/` holds 11,064 files, all .webp, and every record's id matches a sticker file name:
  11,064 of 11,064.
- Names: 46 distinct language keys across the `names` objects (the claim says 43; the extra keys
  may be script or regional variants, not checked). Per record the median is 28 languages; only 50
  records carry all 46, and 1,192 carry fewer than 26.

Verdict: works. Counts hold exactly; "names in 43 languages" is true of the set, not of each bird.
Licence note from the README: stickers under PolyForm Shield (no bird-ID or field-guide app), data MIT.
