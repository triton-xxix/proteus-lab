// bootgpt's forward pass with the exact integer arithmetic of boot.asm (as P-0294's match.py has it).
// One input, the step index, poses everything: context, hidden units, logits, the noisy pick.
import B64 from './weights.js';

export const V = 64, C = 8, E = 6, H = 96;
const A1SHIFT = -4, A2SHIFT = 1, NS = 8;
export const SEED_CTX = [11, 0, 0, 0, 2, 10, 2, 2];

const bytes = Uint8Array.from(atob(B64), (c) => c.charCodeAt(0));
const i8 = new Int8Array(bytes.buffer);
const i16 = (off, n) => Array.from({length: n}, (_, k) => new DataView(bytes.buffer).getInt16(off + 2 * k, true));
export const vocab = Array.from(bytes.slice(0, 64), (b) => String.fromCharCode(b));
const emb = i8.slice(64, 64 + V * E);
const W1 = i8.slice(448, 448 + H * C * E);
const W2 = i8.slice(5056, 5056 + V * H);
const b1 = i16(11200, H);
const b2 = i16(11392, V);

export function forward(ctx) {
  const xin = [];
  for (let k = 0; k < C; k++) for (let r = 0; r < E; r++) xin.push(emb[ctx[k] * E + r]);
  const y = new Array(H);
  for (let j = 0; j < H; j++) {
    let a1 = 0;
    for (let i = 0; i < C * E; i++) a1 += W1[j * C * E + i] * xin[i];
    let p = (A1SHIFT >= 0 ? a1 >> A1SHIFT : a1 * (1 << -A1SHIFT)) + b1[j];
    const v = Math.trunc((p * 64) / (4096 + Math.abs(p)));   // x86 idiv truncates toward zero
    y[j] = Math.max(-64, Math.min(64, v));
  }
  const logits = new Array(V);
  for (let v = 0; v < V; v++) {
    let a2 = 0;
    for (let h = 0; h < H; h++) a2 += W2[v * H + h] * y[h];
    logits[v] = (A2SHIFT >= 0 ? a2 >> A2SHIFT : a2 * (1 << -A2SHIFT)) + b2[v];
  }
  return {y, logits};
}

/** The whole run from one seed: per step the context, hidden, logits, noisy scores and the pick. */
export function run(seed, n) {
  let rnd = seed & 0xffff || 1;
  let ctx = SEED_CTX.slice();
  const steps = [];
  let text = '';
  for (let s = 0; s < n; s++) {
    const {y, logits} = forward(ctx);
    let best = -(1 << 30), bi = 0;
    const scores = new Array(V);
    for (let v = 0; v < V; v++) {
      rnd = (rnd * 25173 + 13849) & 0xffff;
      let r8 = (rnd >> 8) & 0xff;
      if (r8 >= 128) r8 -= 256;
      scores[v] = logits[v] + r8 * NS;
      if (scores[v] > best) { best = scores[v]; bi = v; }
    }
    steps.push({ctx: ctx.slice(), y, logits, scores, pick: bi});
    text += vocab[bi];
    ctx = ctx.slice(1).concat([bi]);
  }
  return {steps, text};
}
