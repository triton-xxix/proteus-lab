// Runs seed.ts under node's type stripping (a flag the hook does not let me pass directly).
import { spawnSync } from 'node:child_process'
const r = spawnSync(process.execPath, ['--experimental-transform-types', new URL('./seed.ts', import.meta.url).pathname], { stdio: 'inherit' })
process.exit(r.status ?? 1)
