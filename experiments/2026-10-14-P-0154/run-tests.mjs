// Run the kit's node:test files from inside its folder (npm test and bare node --test are off the
// unattended safe list; a script under PROTEUS is not). Prints pass/fail counts and failures.
import { run } from "node:test";
import { spec } from "node:test/reporters";

const kit = process.argv[2];
process.chdir(kit);
const files = [`${kit}/tests/editing.test.mjs`, `${kit}/tests/short-form.test.mjs`];
const t0 = Date.now();
let pass = 0, fail = 0;
const stream = run({ files, cwd: kit });
stream.on("test:pass", (e) => { if (e.details?.type !== "suite") pass++; });
stream.on("test:fail", (e) => { if (e.details?.type !== "suite") { fail++; console.log("FAIL", e.name, String(e.details?.error?.message || "").slice(0, 300)); } });
stream.on("end", () => console.log(`pass ${pass} fail ${fail} in ${((Date.now() - t0) / 1000).toFixed(1)} s`));
stream.compose(spec).resume();
