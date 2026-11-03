#!/usr/bin/env python3
"""End-to-end CPU smoke using synthetic evidence."""
import argparse, json, math, pathlib, sys, time
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from evidence_rl.backends.base import SyntheticBackend
from evidence_rl.env.budget_env import BudgetEnv
from evidence_rl.evidence.credit import evidence_group, group_credit, trace_turn_credit
from evidence_rl.logging_utils import RunWriter
p = argparse.ArgumentParser(); p.add_argument("--runs", required=True); a = p.parse_args()
order = ["a", "c", "b"]; bk = SyntheticBackend({"a", "b"}); it = iter(order)
env = BudgetEnv(3, lambda _b: next(it))
for _ in order:
    assert env.step('<grounding>{"bbox_2d":[0.1,0.1,0.5,0.5]}</grounding>')["status"] == "observed"
group, loo = evidence_group(order, bk.utility)
credit = group_credit(order, group, loo)
prefix = [math.log(bk.utility(frozenset(order[:i]))) for i in range(4)]
w = RunWriter(a.runs, f"cpu_smoke_{int(time.time())}", {"backend": "synthetic", "gpu": False})
result = {"group": sorted(group), "credit": credit, "trace_k3": dict(zip(order, trace_turn_credit(prefix))), "reader_calls": bk.calls}
w.write(result); w.close({"status": "passed"})
print(json.dumps(result, ensure_ascii=False, indent=2))
assert group == {"a", "b"} and credit["c"] < 0 < credit["a"]
