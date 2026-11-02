// bootgpt taken apart: the 512-byte boot sector's network, one character per step, every number on screen
// read from the same integer forward pass that picks the character.
import {runSim} from 'teardown-kit/runtime.js';
import {run, vocab, C, H, V} from './net.js';

const SEED = 0x9e75;      // the seed P-0294 recovered from a real v86 boot
const N = 400;
const PER_STEP = 0.075;   // seconds of page time per character

const show = (ch) => (ch === '\n' ? '⏎' : ch === ' ' ? '·' : ch);

runSim(
  {duration: N * PER_STEP + 4, theme: 'light', accent: '#d9480f', hud: {enabled: false}, director: {enabled: false}},
  ({canvas}) => {
    const {steps, text} = run(SEED, N);
    window.BOOTGPT = {seed: SEED, text, steps: steps.length};
    const g = canvas.getContext('2d');
    const resize = () => {
      canvas.width = innerWidth * devicePixelRatio;
      canvas.height = innerHeight * devicePixelRatio;
      canvas.style.width = innerWidth + 'px';
      canvas.style.height = innerHeight + 'px';
    };
    return {
      resize,
      render(t) {
        const s = Math.min(N - 1, Math.floor(t / PER_STEP));
        const st = steps[s];
        const W = canvas.width, Hh = canvas.height, u = Math.min(W / 1600, Hh / 900);
        g.setTransform(u, 0, 0, u, 0, 0);
        g.fillStyle = '#f6f4ef';
        g.fillRect(0, 0, 1600, 900);
        g.fillStyle = '#222';
        g.font = '600 26px "JetBrains Mono", monospace';
        g.fillText(`bootgpt, step ${s + 1} of ${N}: 8 chars in, 96 hidden, 64 logits, one char out`, 40, 50);
        // context
        g.font = '700 40px "JetBrains Mono", monospace';
        for (let k = 0; k < C; k++) {
          g.strokeStyle = '#999';
          g.strokeRect(40 + k * 60, 90, 52, 60);
          g.fillText(show(vocab[st.ctx[k]]), 52 + k * 60, 135);
        }
        // hidden units, -64..64
        g.font = '400 16px "JetBrains Mono", monospace';
        g.fillText('hidden (Q6, clipped to ±64)', 40, 200);
        for (let j = 0; j < H; j++) {
          const v = st.y[j];
          g.fillStyle = v >= 0 ? '#555' : '#aaa';
          g.fillRect(40 + j * 7.5, 300 - Math.max(0, v) * 1.4, 6, Math.abs(v) * 1.4);
        }
        // logits and noisy scores
        g.fillStyle = '#222';
        g.fillText('logits (Q8) and the pick after LCG noise ×8', 40, 420);
        const mx = Math.max(...st.scores.map(Math.abs), 1);
        for (let v = 0; v < V; v++) {
          const x = 40 + v * 23;
          const hgt = (st.logits[v] / mx) * 150;
          g.fillStyle = v === st.pick ? getComputedStyle(document.documentElement).getPropertyValue('--accent') || '#d9480f' : '#888';
          g.fillRect(x, 600 - Math.max(0, hgt), 18, Math.abs(hgt));
          g.fillStyle = '#222';
          g.fillText(show(vocab[v]), x + 3, 630);
        }
        // output so far
        g.font = '400 18px "JetBrains Mono", monospace';
        const lines = text.slice(0, s + 1).split('\n').slice(-8);
        lines.forEach((l, i) => g.fillText(l.slice(-80), 40, 690 + i * 24));
        return {};
      },
    };
  },
);
