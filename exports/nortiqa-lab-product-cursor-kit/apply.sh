#!/usr/bin/env bash
# Apply Cursor kit into a writable clone of giovanyalbea-dotcom/nortiqa-lab
# Usage (from product repo root):
#   bash /path/to/nortiqa-lab-.github/exports/nortiqa-lab-product-cursor-kit/apply.sh
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET_ROOT="${1:-.}"

if [[ ! -d "$TARGET_ROOT/.git" ]]; then
  echo "ERROR: $TARGET_ROOT is not a git repo root (pass product clone path as \$1)"
  exit 1
fi

cd "$TARGET_ROOT"
BRANCH="cursor/mirror-cursor-kit-3d56"
git fetch origin
git checkout -B "$BRANCH" origin/main 2>/dev/null || git checkout -B "$BRANCH" main

mkdir -p docs/dev docs/shared-ai-memory/handoffs
cp -a "$SCRIPT_DIR/.cursor" .
cp -a "$SCRIPT_DIR/agents" .
cp -a "$SCRIPT_DIR/docs/dev/." docs/dev/
cp -a "$SCRIPT_DIR/docs/shared-ai-memory/handoffs/." docs/shared-ai-memory/handoffs/
cp "$SCRIPT_DIR/AGENTS.md" AGENTS.md
cp "$SCRIPT_DIR/CLAUDE.md" CLAUDE.md

git add .cursor agents docs/dev docs/shared-ai-memory/handoffs AGENTS.md CLAUDE.md
git status --short
git commit -m "feat(cursor): mirror Nortiqa Cursor kit and NL-* agent team"
echo
echo "Next:"
echo "  git push -u origin $BRANCH"
echo "  # then open a PR into main"
