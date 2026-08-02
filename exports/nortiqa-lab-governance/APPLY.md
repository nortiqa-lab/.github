# APPLY — crear `nortiqa-lab/governance` desde este seed

**Estado:** DEV / Borrador  
**No oficial** hasta auditoría Claude + ratificación Gio.

## Por qué seed y no create desde Cloud Agent

```bash
gh repo create nortiqa-lab/governance --private
→ 403 Resource not accessible by integration (createRepository)
```

El seed vive aquí para que Gio (o admin org) lo aplique.

Notion: https://app.notion.com/p/3b0e4fe3bfea81c6acc2e485bdcf6558  
Plan: `docs/migration/PLAN-NL-STORAGE-MIGRATION-001.md` (repo `.github`)

## Camino A — UI + import (recomendado si ya elegiste opción 1)

1. Creá el repo Private `nortiqa-lab/governance` en la UI
2. Avisá al agente `repo listo` **o** corré:

```bash
# desde clone de nortiqa-lab/.github (branch con este seed)
bash exports/nortiqa-lab-governance/scripts/pack-for-remote.sh /tmp/gov-pack
# clonar governance y copiar /tmp/gov-pack → PR import
```

## Camino B — un solo script (identidad con permiso org)

```bash
cd /path/to/nortiqa-lab-.github
bash exports/nortiqa-lab-governance/apply.sh
```

El script crea el repo, copia el seed (sin APPLY/apply.sh), commit a `main`.  
**Falla si el repo ya existe** (no overwrite).

## Post-apply (Gio)

1. Verificar Private
2. Protect `main` (PR required)
3. Completar Teams / CODEOWNERS
4. Autorizar lotes (inventarios Lot A/B)
5. Redirects Notion solo con auth explícita — nunca delete-first
6. SQL staging: `exports/sql/APPLY.md` (separado; no parte del repo governance)

## Contenido del seed

| Path | Rol |
|------|-----|
| `README.md` | Matriz, naming, diagrama |
| `docs/**` | Árbol por entidad + mirrors Nortiqa |
| `CODEOWNERS` / `.github/CODEOWNERS` | Ownership por carpeta |
| `docs/.../specs/NOTION-REDIRECT-TEMPLATE.md` | Redirect stub |
| `docs/.../logs/INV-*-LOTE-A/B.md` | Inventarios |
| `apply.sh` | Create+push (Gio only) |
| `scripts/pack-for-remote.sh` | Pack sin create |

## No incluido a propósito

- Cuerpos Valent/LLA
- Writes Centro Doc Madre
- Apply SQL a VPS
- Branch protection automatizado

## Relación con PR #15

Este paquete **consolida** el seed de `cursor/governance-storage-seed-42d9` (PR #15) + mirrors SQL/Lot A de PR #16. Preferir este branch como canónico; cerrar #15 tras merge.
