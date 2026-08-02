# APPLY — crear `nortiqa-lab/governance` desde este seed

Estado: DEV / Borrador

No es documentación oficial. Requiere auditoría de Claude / ARCHITECT-001
y ratificación de Gio para pasar a PROD.

## Por qué existe este paquete

El 2026-08-02, el Cloud Agent (`cursor[bot]`) intentó:

```bash
gh repo create nortiqa-lab/governance --private
```

Resultado: `403 Resource not accessible by integration (createRepository)`.

El seed queda versionado aquí para que Gio (o una identidad con permiso de org) lo aplique en un solo paso.

Prompt KNOW-001 ajustado en Notion:  
https://app.notion.com/p/3b0e4fe3bfea81c6acc2e485bdcf6558

## Camino rápido (script)

Desde un clone actualizado de `nortiqa-lab/.github`:

```bash
cd /path/to/nortiqa-lab-.github
bash exports/nortiqa-lab-governance/apply.sh
```

El script:

1. Crea el repo privado `nortiqa-lab/governance` (requiere permiso org)
2. Copia el contenido del seed (excepto `APPLY.md` / `apply.sh`)
3. Hace commit inicial en rama `main`
4. Abre instrucción para configurar branch protection + Teams

## Camino manual

```bash
# 1) Crear repo (UI o gh) — PRIVATE
gh repo create nortiqa-lab/governance --private \
  --description "Documentación PROD multi-entidad (gobernanza de almacenamiento)"

# 2) Clonar y copiar seed
git clone https://github.com/nortiqa-lab/governance.git
SEED=/path/to/nortiqa-lab-.github/exports/nortiqa-lab-governance
cd governance
rsync -a --exclude APPLY.md --exclude apply.sh "$SEED/" .
git add .
git commit -m "docs(governance): seed estructura multi-entidad + matriz de almacenamiento"
git push -u origin main
```

## Post-apply (Gio / admin org)

1. Settings → General → Visibility: **Private** (verificar)
2. Settings → Branches → Protect `main` (PR required, ≥1 approval)
3. Completar Teams y `.github/CODEOWNERS`
4. Autorizar lotes de migración (ver `MIGRATION-INVENTORY.md`)
5. Autorizar redirects en Centro Doc Madre (Notion) — PAO/OT si aplica

## Contenido del seed

| Path | Rol |
|---|---|
| `README.md` | Matriz, naming, diagrama, supersesión |
| `docs/**` | Árbol por entidad + `.gitkeep` |
| `.github/CODEOWNERS` | Plantilla de ownership por carpeta |
| `templates/notion-redirect.md` | Stub de redirección Notion |
| `MIGRATION-INVENTORY.md` | Inventario lote 1 + bloqueos |
| `docs/nortiqa-lab/dictamenes/DICT-NL-GOBERNANZA-ALMACENAMIENTO-001.md` | Stub DEV del dictamen (fuente Notion pendiente) |

## No incluido a propósito

- Cuerpos completos de docs Valent / LLA (evitar contaminar el org-profile público hasta existir el repo privado)
- Writes en Notion Centro Doc Madre
- Branch protection automatizado
