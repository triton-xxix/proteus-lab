// Seeded cases for loop-detective's Detector, written before looking at fingerprint.ts's normalising rules.
import { Detector } from '/Users/triton/PROTEUS/sandbox/p0156-mods/loop-detective/hooks/core/detector.ts'

const bash = (d: Detector, command: string, answer: unknown) => d.finish(d.begin('Bash', { command }, undefined, '/repo'), answer)
const err = (text: string) => ({ isError: true, text })
const out: Record<string, unknown> = {}

// A: the same pytest failure three times, identical text.
let d = new Detector()
let opened = 0
for (let i = 0; i < 3; i++) opened += bash(d, 'pytest -q', err('FAILED test_x.py::test_a - AssertionError: 2 != 1')).length
out.A_identical_x3 = { opened, active: d.snapshot().active.length }

// B: same failure, but each run prints a different timestamp and duration (real-world noise).
d = new Detector(); opened = 0
const stamps = ['2026-10-14T23:50:01Z in 0.41s', '2026-10-14T23:50:09Z in 0.39s', '2026-10-14T23:50:17Z in 0.44s']
for (const s of stamps) opened += bash(d, 'pytest -q', err(`FAILED test_x.py::test_a - AssertionError: 2 != 1 at ${s}`)).length
out.B_noisy_timestamps_x3 = { opened, active: d.snapshot().active.length }

// C: tonight's real Proteus pattern: three different commands each refused by a hook (should not be one loop).
d = new Detector(); opened = 0
for (const c of ['npm --prefix /x test', 'node --test /x/a.mjs', 'node /x/run.mjs'])
  opened += bash(d, c, { deny: 'not allowed unattended' }).length
out.C_three_different_denials = { opened, active: d.snapshot().active.length }

// D: same command denied three times by a hook (a verbatim retry, what Proteus's rules forbid).
d = new Detector(); opened = 0
for (let i = 0; i < 3; i++) opened += bash(d, 'npm --prefix /x test', { deny: 'not allowed unattended' }).length
out.D_same_denial_x3 = { opened, active: d.snapshot().active.length }

// E: same failure twice only (under threshold).
d = new Detector(); opened = 0
for (let i = 0; i < 2; i++) opened += bash(d, 'pytest -q', err('FAILED test_x.py::test_a')).length
out.E_twice = { opened, active: d.snapshot().active.length, threshold: d.snapshot().threshold }

console.log(JSON.stringify(out, null, 1))
