from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import Any, Optional

@dataclass
class Step:
    step_id: int
    action_text: str
    tool_name: Optional[str] = None
    tool_args: Optional[dict] = None
    observation_id: Optional[str] = None
    token_span: Optional[tuple] = None
    status: str = "completed"

@dataclass
class Trajectory:
    trajectory_id: str
    sample_id: str
    adapter_step: int
    steps: list
    prediction: Optional[str] = None
    outcome: Optional[float] = None
    costs: dict = field(default_factory=dict)
    status: str = "completed"
    failure_reason: Optional[str] = None

@dataclass(frozen=True)
class EvidenceQuery:
    query_id: str
    trajectory_id: str
    kind: str
    subset: tuple
    replacement_seed: Optional[int] = None
    replay_mode: str = "evidence_only"

def to_record(x: Any) -> dict:
    return asdict(x)
