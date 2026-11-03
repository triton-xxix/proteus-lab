// P-0306: how fast does bootgpt dream in v86 0.5.473 under Node. Boots sandbox/bootgpt/disk.img (as P-0294),
// timestamps every screen-put-char and reads the instruction counter at each one, then saves state after
// SECONDS, restores it into the same emulator and times the first char after the restore.
//   node experiments/2026-11-03-P-0306/speed.mjs [seconds]
import fs from "node:fs";
import { V86 } from "/Users/triton/PROTEUS/sandbox/v86/node_modules/v86/build/libv86.mjs";

const SB = "/Users/triton/PROTEUS/sandbox";
const HERE = "/Users/triton/PROTEUS/experiments/2026-11-03-P-0306";
const seconds = Number(process.argv[2] || 10);
const disk = fs.readFileSync(SB + "/bootgpt/disk.img");

const t0 = performance.now();
const emulator = new V86({
  wasm_path: SB + "/v86/node_modules/v86/build/v86.wasm",
  bios: { buffer: fs.readFileSync(SB + "/v86/seabios.bin").buffer },
  vga_bios: { buffer: fs.readFileSync(SB + "/v86/vgabios.bin").buffer },
  hda: { buffer: disk.buffer.slice(disk.byteOffset, disk.byteOffset + disk.length) },
  boot_order: 0x312,
  memory_size: 32 * 1024 * 1024,
  autostart: true,
});

const ev = [];          // [ms since start, instruction counter, row, col, char]
let phase = "boot";
let restoreAt = null, afterRestore = [];
emulator.add_listener("screen-put-char", ([row, col, chr]) => {
  const t = performance.now() - t0;
  const ic = emulator.get_instruction_counter ? emulator.get_instruction_counter() : null;
  if (phase === "boot") ev.push([t, ic, row, col, chr]);
  else if (phase === "restored") afterRestore.push([t - restoreAt, ic, row, col, chr]);
});

setTimeout(async () => {
  phase = "saving";
  const s0 = performance.now();
  const state = await emulator.save_state();
  const saveMs = performance.now() - s0;
  const r0 = performance.now();
  await emulator.restore_state(state);
  const restoreMs = performance.now() - r0;
  restoreAt = performance.now() - t0;
  phase = "restored";
  setTimeout(() => {
    const out = { seconds, events: ev, save_ms: saveMs, restore_ms: restoreMs,
                  state_bytes: state.byteLength, after_restore: afterRestore.slice(0, 20),
                  after_restore_count: afterRestore.length };
    fs.writeFileSync(HERE + "/raw.json", JSON.stringify(out));
    console.log("events", ev.length, "save_ms", saveMs.toFixed(1), "restore_ms", restoreMs.toFixed(1),
                "state_bytes", state.byteLength, "after_restore", afterRestore.length,
                "first_after_restore_ms", afterRestore.length ? afterRestore[0][0].toFixed(1) : null);
    emulator.destroy ? emulator.destroy() : emulator.stop();
    process.exit(0);
  }, 2000);
}, seconds * 1000);
