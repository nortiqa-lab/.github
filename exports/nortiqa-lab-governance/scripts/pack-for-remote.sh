#!/usr/bin/env bash
# Pack this seed into a staging directory ready to push once Gio creates
# nortiqa-lab/governance. Does NOT create the remote repo.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUT="${1:-/tmp/nortiqa-lab-governance-pack}"
rm -rf "$OUT"
mkdir -p "$OUT/docs"
# Prefer rsync; fall back to cp (Cloud Agent images may lack rsync)
if command -v rsync >/dev/null 2>&1; then
  rsync -a --exclude APPLY.md --exclude scripts/ "$ROOT/docs/" "$OUT/docs/"
else
  cp -a "$ROOT/docs/." "$OUT/docs/"
fi
cp "$ROOT/README.md" "$ROOT/CODEOWNERS" "$OUT/"
find "$OUT/docs" -type f -name '*.md' | sort > "$OUT/MIRROR-MANIFEST.txt"
echo "Packed → $OUT"
echo "Files: $(wc -l < "$OUT/MIRROR-MANIFEST.txt")"
cat "$OUT/MIRROR-MANIFEST.txt"
