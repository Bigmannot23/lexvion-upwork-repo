#!/usr/bin/env bash
set -euo pipefail
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp -n .env.example .env || true
python build_index.py
python app.py tests/test_job_post.txt
echo "Output -> proposal.md"