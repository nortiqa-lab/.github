Estado: DEV / Borrador

No es documentación oficial. Requiere auditoría de Claude / ARCHITECT-001
y ratificación de Gio para pasar a PROD.

# Apply — crear `nortiqa-lab/governance` desde este seed

## Prerrequisitos

- Permisos admin en org `nortiqa-lab`
- Dictamen Claude de alcance (recomendado: `DICT-NL-NOTION-GIT-001`)
- Teams/CODEOWNERS reales (reemplazar stubs)

## Pasos

```bash
# 1) Crear repo privado vacío en GitHub UI:
#    https://github.com/organizations/nortiqa-lab/repositories/new
#    Name: governance · Private · sin README remoto (o con y luego merge)

# 2) Desde un clone del org profile (.github) o copia de este export:
SEED=/path/to/nortiqa-lab-.github/exports/nortiqa-lab-governance
mkdir -p ~/src && cd ~/src
gh repo create nortiqa-lab/governance --private --confirm
git clone https://github.com/nortiqa-lab/governance.git
cd governance
bash "$SEED/scripts/bootstrap-repo.sh" .
# o: rsync -a --exclude .git "$SEED/" .

git checkout -b cursor/governance-seed-init
git add .
git commit -m "docs: seed governance multi-entity tree (DEV)"
git push -u origin cursor/governance-seed-init
# Abrir PR → merge humano
```

## Post-merge (solo Gio)

1. Branch protection en `main` (PR required, sin force-push).
2. Completar `.github/CODEOWNERS` con Teams reales por entidad.
3. Migrar lote P0 (Manifiesto, PAO, Prompt, Índice, MEM) vía PR — no dump masivo.
4. Opcional: redirects en Notion Centro Madre (autorización explícita + PAO).

## No hacer

- No push directo a `main` desde agentes sin política Gio.
- No copiar secretos ni `.env`.
- No mezclar entidades en una sola carpeta.
- No borrar páginas Notion al migrar (solo redirect cuando Gio autorice).
