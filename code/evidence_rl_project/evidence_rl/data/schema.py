"""Sample validation and leakage-safe group splits."""
from __future__ import annotations
import hashlib
REQUIRED = ["sample_id", "image_group_id", "question", "answer", "answer_type", "thumbnail", "candidates", "structure_tag"]

def validate_sample(s: dict) -> list:
    errs = [f"missing:{k}" for k in REQUIRED if k not in s]
    if errs:
        return errs
    ids = [c.get("id") for c in s["candidates"]]
    if len(ids) != len(set(ids)):
        errs.append("duplicate_candidate_id")
    if not any(c.get("gold") for c in s["candidates"]):
        errs.append("no_gold_candidate")
    return errs

def assign_split(group_id: str, salt: str = "icml2027-v1", train=.6, dev=.2) -> str:
    h = int(hashlib.sha256(f"{salt}:{group_id}".encode()).hexdigest()[:12], 16) / 16**12
    return "train" if h < train else "dev" if h < train + dev else "test"
