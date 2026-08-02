#!/usr/bin/env bash
# Mirror versionable NL kit into telegram-bridge/nl-kit/
# Safe to run locally or on staging host.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
# repo root: server-ops/sc2027/telegram-bridge → ../../..
REPO_ROOT="$(cd "$ROOT/../../.." && pwd)"
DEST="${NL_KIT_PATH:-$ROOT/nl-kit}"

echo "repo: $REPO_ROOT"
echo "dest: $DEST"

mkdir -p "$DEST/agents/prompts" "$DEST/docs/shared-ai-memory"

copy_file() {
  local rel="$1"
  local src="$REPO_ROOT/$rel"
  local dst="$DEST/$rel"
  if [[ ! -f "$src" ]]; then
    echo "MISSING source: $rel" >&2
    return 1
  fi
  mkdir -p "$(dirname "$dst")"
  cp "$src" "$dst"
  echo "ok $rel"
}

REQUIRED=(
  AGENTS.md
  agents/SHARED_RULES.md
  agents/AUTONOMY.md
  agents/DISPATCH.md
  agents/BOOTSTRAP.md
  agents/LAUNCH.md
  agents/channels/TELEGRAM.md
  agents/prompts/NL-ORCH.md
  agents/prompts/NL-AUDITOR.md
  agents/prompts/NL-BUILDER.md
  agents/prompts/NL-OPS.md
  agents/prompts/NL-PRODUCT.md
  agents/prompts/NL-MEMORY.md
  docs/shared-ai-memory/handoff-template.md
)

fail=0
for rel in "${REQUIRED[@]}"; do
  copy_file "$rel" || fail=1
done

if [[ "$fail" -ne 0 ]]; then
  echo "sync incomplete" >&2
  exit 1
fi

echo "sync complete → $DEST"
