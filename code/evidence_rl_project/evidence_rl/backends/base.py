from __future__ import annotations

class SyntheticBackend:
    """CPU-only stand-in with known evidence structure."""
    def __init__(self, required, base=.2, single=.25, full=.9):
        self.required, self.base, self.single, self.full = set(required), base, single, full
        self.calls = 0
    def utility(self, s):
        self.calls += 1
        hits = len(self.required & set(s))
        return self.full if hits == len(self.required) else self.single if hits else self.base
