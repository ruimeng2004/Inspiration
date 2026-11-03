from __future__ import annotations
import json, os
from pathlib import Path

class RunWriter:
    """Create-only run directory; never overwrite history."""
    def __init__(self, root, experiment_id, config):
        self.path = Path(root) / experiment_id
        self.path.mkdir(parents=True, exist_ok=False)
        (self.path / "config.json").write_text(json.dumps(config, ensure_ascii=False, indent=2))
        self.f = open(self.path / "samples.jsonl", "a", encoding="utf8")
    def write(self, record):
        self.f.write(json.dumps(record, ensure_ascii=False) + "\n")
        self.f.flush(); os.fsync(self.f.fileno())
    def close(self, summary):
        (self.path / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2))
        self.f.close()
