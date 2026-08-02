#!/usr/bin/env bash
# Copy this versionable kit onto the staging host path.
# Default: DRY RUN. Set APPLY=1 to copy.
# Never targets production paths.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
TARGET="${STAGING_BRIDGE_PATH:-/home/deploy/sc2027-staging/telegram-bridge}"
APPLY="${APPLY:-0}"

echo "source: $ROOT"
echo "target: $TARGET"
echo "APPLY:  $APPLY"

if [[ "$TARGET" == *"/prod"* ]] || [[ "$TARGET" == *"/production"* ]]; then
  echo "refusing production-looking target: $TARGET" >&2
  exit 2
fi

if [[ "$TARGET" != *"/sc2027-staging/"* && "$APPLY" == "1" ]]; then
  echo "refusing APPLY outside sc2027-staging path: $TARGET" >&2
  exit 2
fi

ITEMS=(
  nl
  sync-nl-kit.sh
  env.example
  README.md
  APPLY.md
)

echo "planned copy:"
for item in "${ITEMS[@]}"; do
  echo "  $ROOT/$item -> $TARGET/$item"
done

if [[ "$APPLY" != "1" ]]; then
  echo "dry-run only. Re-run with APPLY=1 on the staging host after review."
  exit 0
fi

mkdir -p "$TARGET"
for item in "${ITEMS[@]}"; do
  rm -rf "$TARGET/$item"
  cp -a "$ROOT/$item" "$TARGET/$item"
done

# Keep existing bot token/env; only install env.example beside it
if [[ ! -f "$TARGET/.env" ]]; then
  echo "note: no .env at target (expected — token stays host-managed)"
fi

echo "copied. Next:"
echo "  1) merge manifest keys from agents/channels/telegram-bridge.manifest.proposed.yaml"
echo "  2) set TELEGRAM_ALLOWED_USER_IDS / CHAT_IDS in unit env"
echo "  3) cd $TARGET && ./sync-nl-kit.sh   # needs repo checkout or adjusted REPO_ROOT"
echo "  4) wire adapter: from nl.adapter import handle_telegram_text"
echo "  5) restart sc2027-telegram-agent.service (staging only)"
echo "  6) telegram: /help /status /ops health /audit promote prod"
