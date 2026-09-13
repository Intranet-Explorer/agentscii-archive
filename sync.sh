#!/usr/bin/env bash
# sync.sh -- re-copy the live AGENTSCII workspace into this archive and
# commit whatever changed. Safe to run repeatedly; only real diffs produce
# a commit. Intended to be run periodically (cron/manual) to keep a real,
# diffable history of the catalog's growth -- every shipped pack, every
# rejection, every scratch draft -- separate from the live/mutable
# workspace the agents actively read and write during shifts.

set -euo pipefail
cd "$(dirname "$0")"

SRC=~/agentscii/workspace

rsync -a --delete "$SRC/gallery/" gallery/
rsync -a --delete "$SRC/scratch/" scratch/
rsync -a --delete "$SRC/rejected/" rejected/ 2>/dev/null || true
rsync -a --delete "$SRC/references/" references/
rsync -a --delete "$SRC/submissions/" submissions/ 2>/dev/null || true
cp "$SRC/STYLE.md" . 2>/dev/null || true
cp "$SRC/OBSERVER_NOTES.txt" . 2>/dev/null || true

git add -A
if git diff --cached --quiet; then
    echo "no changes since last sync"
else
    COUNT=$(git diff --cached --stat | tail -1)
    git commit -q -m "Sync $(date -u +%Y-%m-%dT%H:%M:%SZ) — $COUNT"
    echo "committed sync"
fi
