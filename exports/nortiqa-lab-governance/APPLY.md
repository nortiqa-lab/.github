# APPLY — crear `nortiqa-lab/governance` desde este seed

Estado: DEV / Borrador

No es documentación oficial. Requiere auditoría de Claude / ARCHITECT-001
y ratificación de Gio para pasar a PROD.

## Por qué existe este paquete

El 2026-08-02, el Cloud Agent intentó:

```bash
gh repo create nortiqa-lab/governance --private
```

Resultado: `403 Resource not accessible by integration (createRepository)`.

Prompt KNOW-001 ajustado:  
https://app.notion.com/p/3b0e4fe3bfea81c6acc2e485bdcf6558

## Camino rápido (script)

Desde un clone actualizado de `nortiqa-lab/.github` (identidad con permiso org):

```bash
cd /path/to/nortiqa-lab-.github
bash exports/nortiqa-lab-governance/apply.sh
```

El script crea el repo privado, copia el seed (excepto `APPLY.md` / `apply.sh`) y hace push inicial a `main`.

Alternativa sin crear repo (si Gio ya lo creó vacío):

```bash
bash exports/nortiqa-lab-governance/scripts/pack-for-remote.sh /path/to/governance-clone
cd /path/to/governance-clone
git checkout -b cursor/import-seed-from-dotgithub
git add .
git commit -m "docs(governance): import seed from nortiqa-lab/.github"
git push -u origin HEAD
# Open PR → Gio merges
```

## Camino manual

```bash
gh repo create nortiqa-lab/governance --private \
  --description "Documentación PROD multi-entidad (gobernanza de almacenamiento)"

git clone https://github.com/nortiqa-lab/governance.git
SEED=/path/to/nortiqa-lab-.github/exports/nortiqa-lab-governance
cd governance
rsync -a --exclude APPLY.md --exclude apply.sh "$SEED/" .
# Prefer .github/CODEOWNERS; root CODEOWNERS also present as compat
git add .
git commit -m "docs(governance): seed estructura multi-entidad + matriz de almacenamiento"
git push -u origin main
```

## Post-apply (Gio / admin org)

1. Visibility: **Private**
2. Protect `main` (PR required, ≥1 approval)
3. Completar Teams + CODEOWNERS
4. Autorizar lotes de migración (inventarios en `docs/nortiqa-lab/logs/`)
5. Autorizar redirects Centro Doc Madre — PAO/OT si aplica

## No incluido a propósito

- Cuerpos Valent / LLA (hasta inventario Gio + repo privado)
- Writes / deletes en Notion Centro Doc Madre
- Branch protection automatizado
