#!/usr/bin/env bash
# Mirror the shipped gallery from the live AGENTSCII workspace, rebuild the
# GitHub Pages site, and push. Only gallery/ and docs/ are published.
set -euo pipefail
cd "$(dirname "$0")"

SRC=~/agentscii/workspace

rsync -a --delete --exclude='__pycache__/' "$SRC/gallery/" gallery/

git add gallery
if git diff --cached --quiet; then
    exit 0
fi

python3 gen_gallery.py
git add -A gallery docs

# Never push something that looks like a credential.
if git diff --cached -U0 | grep -E '^\+' | grep -qE 'sk-ant-[A-Za-z0-9_-]{20}|ghp_[A-Za-z0-9]{30}|github_pat_[A-Za-z0-9_]{30}|AKIA[0-9A-Z]{16}|-----BEGIN [A-Z ]*PRIVATE KEY-----|xox[baprs]-[A-Za-z0-9-]{10}'; then
    echo "sync.sh: possible credential in staged changes; not committing"
    git reset -q
    exit 1
fi

git commit -q -m "Sync gallery $(date -u +%Y-%m-%d)"
git push -q origin main
