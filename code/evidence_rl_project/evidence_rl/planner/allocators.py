from __future__ import annotations
import math, random
from dataclasses import dataclass
from .gittins import gittins_index

@dataclass
class Arm:
    name: str
    cost: float = 1.
    alpha: float = 1.
    beta: float = 1.
    pulls: int = 0
    variance: float = .25

def allocate(arms, budget, method="gittins", seed=0, gamma=.99):
    """Batch allocation for one training step. Posterior updates happen after evaluation."""
    counts = {a.name: 0 for a in arms}
    rng = random.Random(seed)
    used = 0.
    planned = {a.name: 0 for a in arms}
    while True:
        ok = [a for a in arms if used + a.cost <= budget]
        if not ok:
            return counts
        if method == "uniform":
            arm = min(ok, key=lambda a: (counts[a.name], a.name))
        elif method == "random":
            arm = rng.choice(ok)
        elif method == "gittins":
            arm = max(ok, key=lambda a: gittins_index(max(1, round(a.alpha)), max(1, round(a.beta + planned[a.name])), gamma) / a.cost)
        elif method == "ucb":
            t = sum(a.pulls for a in arms) + sum(planned.values()) + 2
            arm = max(ok, key=lambda a: (a.alpha / (a.alpha + a.beta) + math.sqrt(2 * math.log(t) / (a.pulls + planned[a.name] + 1))) / a.cost)
        elif method == "neyman":
            w = {a.name: math.sqrt(max(a.variance, 1e-9) / a.cost) for a in ok}
            total, n = sum(w.values()), sum(counts.values()) + 1
            arm = max(ok, key=lambda a: w[a.name] / total - counts[a.name] / n)
        else:
            raise ValueError(method)
        counts[arm.name] += 1
        planned[arm.name] += 1
        used += arm.cost
