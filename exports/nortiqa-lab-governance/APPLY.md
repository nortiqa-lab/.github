# APPLY — seed → `nortiqa-lab/governance`

## Prerrequisitos
- Gio crea el repo privado `nortiqa-lab/governance` en la org.
- Branch protection en `main` (PRs only).
- Teams/CODEOWNERS los completa Gio.

## Pasos
```bash
# From a clean clone of nortiqa-lab/governance
rsync -a --exclude APPLY.md ./docs/ /path/to/governance/docs/
cp README.md CODEOWNERS /path/to/governance/
cd /path/to/governance
git checkout -b cursor/import-seed-from-dotgithub
git add docs README.md CODEOWNERS
git commit -m "Import governance docs seed from nortiqa-lab/.github exports"
git push -u origin HEAD
# Open PR → Gio merges
```

If this Cloud Agent cannot create the remote repo, leave this seed here until Gio applies it.
