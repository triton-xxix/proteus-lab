# P-0294: bootgpt booted in v86, checked char for char

**Question.** P-0285 built bootgpt's disk (12 KB: a 512-byte MBR that runs a tiny char-level network, plus
weights) but never booted it. The README claims the asm reproduces train.py's integer sim exactly. Does it?

**Method.** `npm --prefix sandbox/v86 install v86@0.5.473 --ignore-scripts` (no dependencies; the package
has no BIOS, so SeaBIOS and the VGA BIOS came from the v86 repo's `bios/` by curl). `boot.mjs` boots
`sandbox/bootgpt/disk.img` as a hard disk under Node, headless, and rebuilds the 80x25 screen from the bus's
`screen-put-char` events (VGA memory is a device in v86, so `read_memory(0xB8000)` reads blank); the
6-second screen is `screen.txt`. `match.py` rebuilds the integer sim from `weights.bin` and `params.inc`.

The disk seeds its LCG from the PIT clock (`int 0x1A`, then `or dx, 1`), and train.py prints its sample
at seed 0x1234, which is even, so the printed sample can never appear on a real boot. Instead the seed is
recovered: the logits depend only on the context, which the screen gives, so all 32,768 odd seeds are
stepped at once and filtered by each printed character.

**Numbers.** Boot to header in under 6 s wall time (SeaBIOS 1.16.2, "Booting from Hard Disk").
The first 9 printed characters leave exactly one seed, 0x9e75. From it the sim generates text that matches
the screen on all 9 full rows (0 differing) and the timer-cut last row as a prefix: 397 printed characters,
388 of them after the 9 used to find the seed.

**Traps.** `boot_order` nibbles read from the low end (0x123 boots the CD first; 0x312 is hard disk first).
`/usr/local/bin/node` is denied by the unattended hook, bare `node` on an absolute script path is allowed.

**Not done.** One boot, about 400 characters; no floppy boot; no keypress-reboot path; no real hardware.
