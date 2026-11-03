"""Parse crop and answer actions. Format stays adjustable until the Qwen template is confirmed."""
from __future__ import annotations
import json, re
from dataclasses import dataclass
from typing import Optional
TOOL_RE = re.compile(r"<grounding>\s*(\{.*?\})\s*</grounding>", re.S)
ANSWER_RE = re.compile(r"<answer>(.*?)</answer>", re.S)

@dataclass
class ParsedAction:
    kind: str
    bbox: Optional[tuple] = None
    answer: Optional[str] = None
    error: Optional[str] = None

def parse_action(text: str) -> ParsedAction:
    a, t = ANSWER_RE.search(text), TOOL_RE.search(text)
    if a and t:
        return ParsedAction("invalid", error="tool_and_answer")
    if a:
        return ParsedAction("answer", answer=a.group(1).strip())
    if not t:
        return ParsedAction("invalid", error="no_action")
    try:
        x0, y0, x1, y1 = map(float, json.loads(t.group(1))["bbox_2d"])
    except Exception:
        return ParsedAction("invalid", error="bad_json")
    if not (0 <= x0 < x1 <= 1 and 0 <= y0 < y1 <= 1):
        return ParsedAction("invalid", error="bad_bbox")
    return ParsedAction("crop", bbox=(x0, y0, x1, y1))
