#!/usr/bin/env bash
# Bootstrap empty nortiqa-lab/governance from this seed (run by Gio / admin).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TARGET="${1:-}"
if [[ -z "$TARGET" ]]; then
  echo "Usage: $0 /path/to/governance-clone" >&2
  exit 1
fi
mkdir -p "$TARGET"
rsync -a --exclude '.git' "$ROOT/" "$TARGET/"
echo "Seed copied to $TARGET"
echo "Next: create private repo nortiqa-lab/governance, push branch, set protection + Teams."
