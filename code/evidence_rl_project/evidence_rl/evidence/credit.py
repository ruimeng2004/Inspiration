"""Credit baselines and evidence groups."""
from __future__ import annotations
import math, random

def trace_turn_credit(gold_logprobs, k=3, gamma=.8, eps=.1):
    """TRACE Eq. 7-9 without terminal fill. Input: mean gold logprob for S_0...S_T."""
    if k < 1:
        raise ValueError("k must be >=1")
    d = [-l + eps for l in gold_logprobs]
    delta = [math.log(d[i] / d[i + 1]) for i in range(len(d) - 1)]
    out = []
    for i in range(len(delta)):
        h = min(i + k - 1, len(delta) - 1)
        w = [gamma ** (u - i) for u in range(i, h + 1)]
        out.append(sum(x * delta[u] for x, u in zip(w, range(i, h + 1))) / sum(w))
    return out

def prefix_delta(utilities):
    return [utilities[i + 1] - utilities[i] for i in range(len(utilities) - 1)]

def leave_one_out(obs, utility):
    full_set = frozenset(obs)
    full = utility(full_set)
    return {o: full - utility(full_set - {o}) for o in full_set}

def evidence_group(obs, utility, delta=.05):
    """Backward elimination: approximate minimal sufficient evidence group."""
    group = frozenset(obs)
    base = utility(group)
    loo = leave_one_out(group, utility)
    for o in sorted(group, key=lambda x: (loo[x], x)):
        cand = group - {o}
        if utility(cand) >= base - delta:
            group = cand
    return group, loo

def group_credit(obs, group, harm=None, alpha=1., rho=.2, eta=.3):
    harm = harm or {}
    return {o: alpha if o in group else -rho - (eta if harm.get(o, 0) < 0 else 0) for o in obs}

def shuffled(credit, seed):
    """Marginal-matched placebo control."""
    keys, vals = list(credit), list(credit.values())
    random.Random(seed).shuffle(vals)
    return dict(zip(keys, vals))

def bounded_lambda(outcome_adv, credit_range, lam0=.2, share=.5):
    """Keep process credit below half of the smallest outcome-advantage gap."""
    vals = sorted(set(round(a, 9) for a in outcome_adv))
    if credit_range <= 0:
        return 0.
    if len(vals) < 2:
        return lam0
    gap = min(b - a for a, b in zip(vals, vals[1:]))
    return min(lam0, share * gap / credit_range)
