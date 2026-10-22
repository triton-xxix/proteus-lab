"""P-0195: time molanim's protein_motion on a structure its tests do not use (2HHB haemoglobin, chain A)
and measure how well it keeps bond lengths, the same check as its own test on 9GO1.
Usage: <venv>/bin/python3 move.py
"""
import json
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path('/Users/triton/PROTEUS/sandbox/p0195/repo')
sys.path.insert(0, str(ROOT))
from molanim import dynamics as D  # noqa: E402
from molanim import structure as St  # noqa: E402

out = {}
for pdb, cif in (('2HHB', ROOT / 'projects/website/pdb/2HHB.cif'), ('9GO1', ROOT / 'assets/pdb/9GO1.cif')):
    t0 = time.time()
    t, _ = St.read_mmcif(cif)
    t = St.select(t, t['chain'] == t['chain'][0])
    X = t['xyz']
    read_s = time.time() - t0
    times, rate = D.clock(96, 1.0 / 24)
    t1 = time.time()
    m = D.protein_motion(np.random.default_rng(8), X, t['resn'], t['resi'], t['name'], t['chain'], times, rate * 2)
    motion_s = time.time() - t1
    edges = St.bonds(t)
    length = lambda P: np.linalg.norm(P[edges[:, 0]] - P[edges[:, 1]], axis=1)  # noqa: E731
    strain = np.array([np.abs(length(X + D.displacement(m, X, f)) - length(X)) for f in range(0, 96, 8)])
    rms = [float(np.sqrt((D.displacement(m, X, f) ** 2).sum(1).mean())) for f in range(0, 96, 8)]
    out[pdb] = {
        'atoms': int(len(X)), 'residues': int(len(np.unique(t['resi']))), 'chain': str(t['chain'][0]),
        'read_s': round(read_s, 2), 'motion_s_96_frames': round(motion_s, 2),
        'bond_strain_p99_A': round(float(np.percentile(strain, 99)), 3), 'bond_strain_max_A': round(float(strain.max()), 3),
        'rms_displacement_A_mean': round(float(np.mean(rms)), 3),
        'report': {k: v for k, v in m['report'].items() if isinstance(v, (int, float, str))},
    }
json.dump(out, open('/Users/triton/PROTEUS/experiments/2026-10-22-P-0195/move.json', 'w'), indent=2)
print(json.dumps(out, indent=1))
