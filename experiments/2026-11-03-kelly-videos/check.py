"""Check the numbers in five Kelly explainer videos, by formula and by simulation."""
import math, random

def kelly(p, b):
    return p - (1 - p) / b

def g(f, p, b):
    return p * math.log(1 + f * b) + (1 - p) * math.log(1 - f)

print("Mutual Information: p 0.7, odds 4 to 6 (b=2/3)")
b = 2 / 3
f = kelly(0.7, b)
print(f"  Kelly f {f:.3f}, growth {g(f,0.7,b)*100:.2f}% a flip, $50 after 100 flips {50*math.exp(100*g(f,0.7,b)):.0f}")
print(f"  bet $5 of $50 fixed fraction 0.1: growth {g(0.1,0.7,b)*100:.2f}% a flip")
print("Mind Math Money and GG Easy: p 0.6, b 1 ->", round(kelly(0.6, 1), 3))
print("Financial Wisdom: boxer p 0.55 b 0.9 ->", round(kelly(0.55, 0.9), 4),
      "| trader p 0.59 b 4.04 ->", round(kelly(0.59, 4.04), 4), "| p 0.5 b 2 ->", kelly(0.5, 2))

random.seed(7)
def sim(frac, p, b, n=100, trials=20000, halve=0.5):
    ruinish = 0
    finals = []
    for _ in range(trials):
        w, peak, hit = 1.0, 1.0, False
        for _ in range(n):
            w *= (1 + frac * b) if random.random() < p else (1 - frac)
            peak = max(peak, w)
            if w <= peak * halve:
                hit = True
        ruinish += hit
        finals.append(w)
    finals.sort()
    return ruinish / trials, finals[trials // 2], sum(x < 1 for x in finals) / trials

print("p 0.6, b 1, 100 bets, 20,000 runs: share that ever fall 50% from a peak, median final, share ending below start")
for name, fr in [("full Kelly 20%", 0.2), ("half Kelly 10%", 0.1), ("fifth Kelly 4%", 0.04), ("double Kelly 40%", 0.4)]:
    dd, med, below = sim(fr, 0.6, 1)
    print(f"  {name:17s} {dd*100:5.1f}%  median x{med:6.2f}  below start {below*100:4.1f}%")

print("Edge misjudged: true p 0.55 while you bet Kelly for 0.6 (20%)")
dd, med, below = sim(0.2, 0.55, 1)
print(f"  full Kelly at true 0.55: fall 50% {dd*100:.1f}%, median x{med:.2f}, below start {below*100:.1f}%")
dd, med, below = sim(0.1, 0.55, 1)
print(f"  half Kelly at true 0.55: fall 50% {dd*100:.1f}%, median x{med:.2f}, below start {below*100:.1f}%")
