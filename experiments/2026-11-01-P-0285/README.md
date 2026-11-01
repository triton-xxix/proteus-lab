# P-0285 bootgpt: does the MBR fit and how big is the image?

Source: github.com/kerlenton/bootgpt (HN 50315782), fetched raw into `sandbox/bootgpt/`, 1 Nov 2026.

What I ran: the repo's `corpus_gen.py` and `train.py` unchanged on the project venv (numpy), then
`boot.asm` through the official NASM 2.16.03 macOS release (nasm.us, into `sandbox/nasm/`), then the
same `cat boot.bin weights.bin` that `build.sh` does. `build.py` here does all of it without a `cd`.

Measured (`results.json`):
- corpus 3,079,543 bytes; training reached loss 0.641 at step 40,000; about a minute on this Intel Mac.
- weights.bin 11,776 bytes, 23 sectors, as the README says (11.5 KB).
- boot.bin exactly 512 bytes with the 55AA signature; at most 491 bytes before the zero padding, so
  19 bytes spare of the 510.
- disk.img 12,288 bytes.
- train.py's integer simulation printed max |logit| 18,289 against the int16 limit of 32,767, and at
  noise 8 the samples read like dmesg lines; at noise 24 and up they fall apart.

Not run: booting it. QEMU is not on this Mac and `brew` is off the safe list, so whether the asm's
output matches the Python simulation char for char (the README's claim) is unchecked.

Verdict: works, on the size question. The claim the image boots and matches is for a night with QEMU.
