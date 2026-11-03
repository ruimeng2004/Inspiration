"""Bernoulli Gittins index by binary search on a retirement reward."""
from __future__ import annotations
from functools import lru_cache

def gittins_index(a, b, gamma=.99, horizon=80, tol=1e-4):
    def wins(lam):
        retire = lam / (1 - gamma)
        @lru_cache(None)
        def v(x, y, t):
            if t == 0:
                return retire
            p = x / (x + y)
            return max(retire, p * (1 + gamma * v(x + 1, y, t - 1)) + (1 - p) * gamma * v(x, y + 1, t - 1))
        return v(a, b, horizon) > retire + 1e-12
    lo, hi = a / (a + b), 1.
    while hi - lo > tol:
        mid = (lo + hi) / 2
        if wins(mid):
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2
