# Apply Cursor kit → `giovanyalbea-dotcom/nortiqa-lab`

Estado: DEV / Borrador

No es documentación oficial. Requiere auditoría de Claude / ARCHITECT-001
y ratificación de Gio para pasar a PROD.

## Why this package exists

On 2026-08-01, `cursor[bot]` **could not push** to `giovanyalbea-dotcom/nortiqa-lab` (HTTP 403).  
The kit was prepared here so Gio (or an identity with write access) can apply it in one shot.

Source of truth for the org kit remains: `nortiqa-lab/.github`.

## Fastest path (script)

```bash
# 1) Clone both repos (or pull latest .github main)
git clone https://github.com/nortiqa-lab/.github.git nortiqa-org-profile
git clone https://github.com/giovanyalbea-dotcom/nortiqa-lab.git nortiqa-lab
cd nortiqa-lab
bash ../nortiqa-org-profile/exports/nortiqa-lab-product-cursor-kit/apply.sh .
git push -u origin cursor/mirror-cursor-kit-3d56
# Open PR on GitHub UI → merge
python3 tools/mission-compiler/compile.py --self-test
```

## One-shot apply (from a clone of the product repo)

```bash
# From a writable clone of giovanyalbea-dotcom/nortiqa-lab
ORG_KIT=/path/to/nortiqa-lab-.github/exports/nortiqa-lab-product-cursor-kit

git checkout -b cursor/mirror-cursor-kit-3d56

cp -a "$ORG_KIT/.cursor" .
cp -a "$ORG_KIT/agents" .
mkdir -p docs/dev docs/shared-ai-memory/handoffs tools
cp -a "$ORG_KIT/docs/dev/." docs/dev/
cp "$ORG_KIT/docs/shared-ai-memory/handoffs/"*.md docs/shared-ai-memory/handoffs/
cp -a "$ORG_KIT/tools/mission-compiler" tools/
cp "$ORG_KIT/AGENTS.md" AGENTS.md
cp "$ORG_KIT/CLAUDE.md" CLAUDE.md

git add .cursor agents docs/dev docs/shared-ai-memory/handoffs tools/mission-compiler AGENTS.md CLAUDE.md
git commit -m "feat(cursor): mirror Nortiqa Cursor kit, NL-* team, Gen5 dry-run compiler"
git push -u origin cursor/mirror-cursor-kit-3d56
# open PR → merge when satisfied
python3 tools/mission-compiler/compile.py --self-test
```

## Grant bot write access (alternative)

If you want Cloud Agents to maintain the product repo directly:

1. Add the Cursor GitHub App / `cursor[bot]` with **write** on `giovanyalbea-dotcom/nortiqa-lab`
2. Re-run a Cloud Agent with: “apply exports/nortiqa-lab-product-cursor-kit to this repo”

## Contents

| Path | Action |
|------|--------|
| `.cursor/` | Create / refresh |
| `agents/` | Create / refresh (NL-* kit mirror) |
| `docs/dev/` | DEV docs incl. Vanguard, Gen4 closeout, Gen5 Mission Control |
| `tools/mission-compiler/` | Gen5 dry-run compiler (NL → contract; no side effects) |
| `AGENTS.md` | Replace with integrated product version |
| `CLAUDE.md` | Replace with integrated version + Cursor pointers |

Refresco: 2026-08-02 — incluye Gen4/Gen5/Vanguard + mission-compiler tras merge #6/#7/#10/#12.
