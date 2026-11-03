#!/usr/bin/env bash
# Run on your own computer. Copies code, makes data dirs, runs CPU tests, then only checks GPU.
# Code stays on csefiles (nearly full); runs/ is a symlink to $DATA/runs so outputs land on /data.
set -euo pipefail
cd "$(dirname "$0")"
HOST=${HOST:-xzhanglab}
CODE=${CODE:-/net/csefiles/xzhanglab/rmeng41/ICML/evidence_rl_project}
DATA=${DATA:-/data/ycheng430/rmeng41/ICML}
ssh "$HOST" "mkdir -p '$CODE' '$DATA/runs' '$DATA/raw' '$DATA/processed' && ( [ -L '$CODE/runs' ] || [ ! -e '$CODE/runs' ] ) && ln -sfn '$DATA/runs' '$CODE/runs'"
rsync -av --exclude runs --exclude __pycache__ --exclude .git ./ "$HOST:$CODE/"
ssh "$HOST" "cd '$CODE' && PYTHONPATH=. python3 -m unittest discover -s tests -v && python3 scripts/cpu_smoke.py --runs runs && python3 scripts/check_gpu.py --min-free-gb 40 | tee runs/gpu_check.json"
echo "Deployment finished. No GPU workload was started."
