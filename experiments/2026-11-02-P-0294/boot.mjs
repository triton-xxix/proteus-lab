// P-0294: boot sandbox/bootgpt/disk.img in v86 0.5.473 under Node, headless, and dump the VGA text
// buffer (0xB8000, 80x25, char+attr) after SECONDS of wall time to screen.bin beside this script.
//   node experiments/2026-11-02-P-0294/boot.mjs [seconds] [hda|fda]
import fs from "node:fs";
import { V86 } from "/Users/triton/PROTEUS/sandbox/v86/node_modules/v86/build/libv86.mjs";

const SB = "/Users/triton/PROTEUS/sandbox";
const OUT = "/Users/triton/PROTEUS/experiments/2026-11-02-P-0294/screen.bin";
const seconds = Number(process.argv[2] || 3);
const mode = process.argv[3] || "hda";

let disk = fs.readFileSync(SB + "/bootgpt/disk.img");
if (mode === "fda") {
  const pad = Buffer.alloc(1474560);
  disk.copy(pad);
  disk = pad;
}
const t0 = Date.now();
const emulator = new V86({
  wasm_path: SB + "/v86/node_modules/v86/build/v86.wasm",
  bios: { buffer: fs.readFileSync(SB + "/v86/seabios.bin").buffer },
  vga_bios: { buffer: fs.readFileSync(SB + "/v86/vgabios.bin").buffer },
  [mode]: { buffer: disk.buffer.slice(disk.byteOffset, disk.byteOffset + disk.length) },
  boot_order: mode === "hda" ? 0x312 : 0x321,   // low nibble first: 1 floppy, 2 hard disk, 3 CD
  memory_size: 32 * 1024 * 1024,
  autostart: true,
});
emulator.add_listener("emulator-ready", () => console.log("ready after", Date.now() - t0, "ms"));
// VGA text memory is a device in v86, not RAM: rebuild the screen from the bus's put-char events
const grid = Array.from({ length: 25 }, () => Array(80).fill(32));
let puts = 0;
emulator.add_listener("screen-put-char", ([row, col, chr]) => {
  if (row < 25 && col < 80) grid[row][col] = chr;
  puts++;
});
setTimeout(() => {
  const rows = grid.map((r) => String.fromCharCode(...r).replace(/\s+$/, ""));
  fs.writeFileSync(OUT.replace(".bin", ".txt"), rows.join("\n") + "\n");
  console.log(rows.join("\n"));
  console.log("put-char events", puts, "wrote", OUT.replace(".bin", ".txt"), "after", Date.now() - t0, "ms");
  emulator.destroy ? emulator.destroy() : emulator.stop();
  process.exit(0);
}, seconds * 1000);
