#!/usr/bin/env bash
# Apply governance seed → nortiqa-lab/governance (private)
# Requires: gh authenticated with org create/admin rights (Gio / admin).
# Cloud Agent cursor[bot] gets 403 on createRepository — use this from Gio's machine.
set -euo pipefail

SEED_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ORG="${GITHUB_ORG:-nortiqa-lab}"
REPO_NAME="${GOVERNANCE_REPO:-governance}"
FULL="${ORG}/${REPO_NAME}"
WORK_DIR="${TMPDIR:-/tmp}/nortiqa-${REPO_NAME}-apply-$$"

cleanup() { rm -rf "${WORK_DIR}"; }
trap cleanup EXIT

echo "==> Target: ${FULL} (private)"
echo "==> Seed:   ${SEED_DIR}"

if ! command -v gh >/dev/null 2>&1; then
  echo "ERROR: gh CLI required" >&2
  exit 1
fi

copy_seed() {
  local dest="$1"
  if command -v rsync >/dev/null 2>&1; then
    rsync -a \
      --exclude 'APPLY.md' \
      --exclude 'apply.sh' \
      --exclude 'scripts/pack-for-remote.sh' \
      --exclude '.git' \
      "${SEED_DIR}/" "${dest}/"
  else
    # Cloud/minimal images may lack rsync
    (
      cd "${SEED_DIR}"
      tar -cf - \
        --exclude './APPLY.md' \
        --exclude './apply.sh' \
        --exclude './scripts/pack-for-remote.sh' \
        --exclude './.git' \
        . | tar -xf - -C "${dest}"
    )
  fi
}

if gh repo view "${FULL}" >/dev/null 2>&1; then
  echo "ERROR: ${FULL} already exists. Aborting to avoid overwrite." >&2
  echo "Hint: use scripts/pack-for-remote.sh + a PR import instead." >&2
  exit 1
fi

echo "==> Creating private repository..."
gh repo create "${FULL}" --private \
  --description "Documentación PROD multi-entidad (gobernanza de almacenamiento)"

mkdir -p "${WORK_DIR}"
gh repo clone "${FULL}" "${WORK_DIR}/repo"
cd "${WORK_DIR}/repo"

copy_seed "$(pwd)"

git add .
git status --short
git commit -m "docs(governance): seed estructura multi-entidad + mirrors Lot A/B + matriz"
git push -u origin HEAD:main

echo
echo "==> Done. Repo: https://github.com/${FULL}"
echo "==> Next (Gio): branch protection on main + Teams/CODEOWNERS + migration PRs"
echo "==> Notion task: https://app.notion.com/p/3b0e4fe3bfea81c6acc2e485bdcf6558"
