from __future__ import annotations
from .tool_parser import parse_action

class BudgetEnv:
    """Applies one action and records failures instead of dropping them."""
    def __init__(self, max_calls: int, crop_fn):
        self.max_calls, self.crop_fn, self.calls = max_calls, crop_fn, 0
    def step(self, text: str) -> dict:
        p = parse_action(text)
        if p.kind == "answer":
            return {"status": "answer", "answer": p.answer}
        if p.kind == "invalid":
            return {"status": "failed", "reason": p.error}
        if self.calls >= self.max_calls:
            return {"status": "failed", "reason": "over_budget"}
        self.calls += 1
        return {"status": "observed", "observation_id": self.crop_fn(p.bbox), "bbox": p.bbox}
