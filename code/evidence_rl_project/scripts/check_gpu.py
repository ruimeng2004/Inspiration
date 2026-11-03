#!/usr/bin/env python3
"""Read-only GPU gate. It never starts a GPU workload."""
import argparse, json, shutil, subprocess
p = argparse.ArgumentParser(); p.add_argument("--min-free-gb", type=float, default=40); a = p.parse_args()
if not shutil.which("nvidia-smi"):
    print(json.dumps({"gpu_test": "skip", "reason": "nvidia-smi not found"}, ensure_ascii=False)); raise SystemExit(0)
q = "index,name,memory.total,memory.used,memory.free,utilization.gpu"
out = subprocess.check_output(["nvidia-smi", f"--query-gpu={q}", "--format=csv,noheader,nounits"], text=True)
gpus = []
for line in out.strip().splitlines():
    i, name, total, used, free, util = [x.strip() for x in line.split(",")]
    gpus.append(dict(index=int(i), name=name, total_mb=int(total), used_mb=int(used), free_mb=int(free), util=util))
best = max(gpus, key=lambda g: g["free_mb"]) if gpus else None
ready = bool(best and best["free_mb"] >= a.min_free_gb * 1024)
print(json.dumps({"gpus": gpus, "gpu_test": "eligible_after_user_approval" if ready else "skip", "reason": None if ready else "insufficient_free_memory"}, ensure_ascii=False, indent=2))
