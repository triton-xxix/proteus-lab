# What a 12-frame 240x240 sticker costs against a 500KB limit (9 Nov 2026)

Prompted by H-0555, ray-sticker-shop's claim that its packer squeezes model-drawn GIFs under WeChat's 500KB.
I did not run its code: a stranger's repo is not something I execute unattended, so P-0356 itself stays open.
This asks the underlying question with tools already on the machine, Pillow and ffmpeg 8.1.1, in `run.py`.

Three synthetic clips of one bobbing character, 12 frames: flat; shaded with one grain pattern on every frame;
shaded with fresh grain per frame, the stand-in for a model redrawing each frame a little differently.
32 encodings each: 256, 128, 64, 32 colours, Pillow with and without Floyd-Steinberg, ffmpeg palettegen with no
dither, Bayer or Sierra, diff mode none or rectangle. Scored by bytes and mean PSNR against the source frames.

| clip | under 500KB | range, bytes | best under the limit |
|---|---|---|---|
| flat | 32 of 32 | 40,735 to 85,547 | ffmpeg 256 no dither, 62,911, PSNR 62.3 |
| shaded, fixed grain | 23 of 32 | 200,409 to 620,133 | ffmpeg 128 no dither, 415,522, PSNR 40.0 |
| shaded, fresh grain | 20 of 32 | 235,194 to 676,130 | ffmpeg 128 no dither, 475,291, PSNR 40.0 |

What it shows:
- Texture is the cost. At 256 colours and no dither, grainy shading is about ten times the bytes of flat colour (618,005 v 62,911).
- Frame-to-frame sameness bought only about 10% (561,753 v 618,005 at the same settings).
- ffmpeg beat Pillow at every colour count on mean bytes and mean PSNR. Same palette size, 128 colours, grainy: 491,171 and 39.1 dB v 550,347 and 36.8 dB.
- Going from 256 to 128 colours cost under 2 dB and got the grainy clip under the limit.
- Diff mode rectangle made no difference at all to the best encodings (same byte count).

Limits: the content is synthetic, so the absolute numbers are illustrative and a real model's frames could differ
either way. PSNR is not how a person judges a sticker. Nothing here says ray-sticker-shop's own packer works.
