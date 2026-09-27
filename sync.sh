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
# Local-only material never enters this public repo, even on disk here.
rsync -a --delete --delete-excluded \
  --exclude='/ref/' --exclude='/refs/' --exclude='/_ref_*/' --exclude='__pycache__/' \
  "$SRC/scratch/" scratch/
rsync -a --delete "$SRC/rejected/" rejected/ 2>/dev/null || true
rsync -a --delete --delete-excluded \
  --include='/study/' --include='/study/_*' --include='/study/README.txt' --exclude='/study/*' \
  --include='/blockins/***' --include='/*.txt' --exclude='*' \
  "$SRC/references/" references/
rsync -a --delete "$SRC/submissions/" submissions/ 2>/dev/null || true
# archive/ and shelved/ added 2026-09-22: scratch/ now holds current work
# only, and the 916 archived files plus the reasoning in
# archive/README.md must be mirrored here or --delete on scratch/ would
# drop them from the archive with nowhere to land.
rsync -a --delete "$SRC/archive/" archive/ 2>/dev/null || true
rsync -a --delete "$SRC/shelved/" shelved/ 2>/dev/null || true
cp "$SRC/STYLE.md" . 2>/dev/null || true
cp "$SRC/OBSERVER_NOTES.txt" . 2>/dev/null || true
cp "$SRC/CATALOG.md" . 2>/dev/null || true

# Stage the raw sync first so we can tell whether anything real changed
# before paying the cost of re-rendering every piece to PNG.
git add gallery scratch rejected references submissions archive shelved STYLE.md OBSERVER_NOTES.txt CATALOG.md 2>/dev/null || true
if git diff --cached --quiet; then
    exit 0  # no changes — stay silent (no_agent cron: empty stdout sends nothing)
fi

# Something changed in the source data — regenerate the GitHub Pages
# gallery (docs/data.json + docs/images/*.png) so new/updated packs show
# up on the live site automatically, not just in the raw archive.
python3 gen_gallery.py

git add -A
# Never auto-push something that looks like a credential.
if git diff --cached -U0 | grep -E '^\+' | grep -qE 'sk-ant-[A-Za-z0-9_-]{20}|ghp_[A-Za-z0-9]{30}|github_pat_[A-Za-z0-9_]{30}|AKIA[0-9A-Z]{16}|-----BEGIN [A-Z ]*PRIVATE KEY-----|xox[baprs]-[A-Za-z0-9-]{10}'; then
    echo "sync.sh: possible credential in staged changes -- NOT committing or pushing"
    git reset -q
    exit 1
fi
COUNT=$(git diff --cached --stat | tail -1)
git commit -q -m "Sync $(date -u +%Y-%m-%dT%H:%M:%SZ) — $COUNT"
git push -q origin main
echo "synced, regenerated gallery, and pushed: $COUNT"
