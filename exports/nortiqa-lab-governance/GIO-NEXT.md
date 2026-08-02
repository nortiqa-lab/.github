# Gio — siguiente paso (1 acción)

El seed ya está en PR: https://github.com/nortiqa-lab/.github/pull/16  

El bot **no puede** crear el repo (`403 createRepository`).

## Opción recomendada (UI, 2 min)

1. Abrí https://github.com/organizations/nortiqa-lab/repositories/new  
2. Owner: **nortiqa-lab** · Name: **governance** · **Private** · Create  
3. (Opcional) Protect `main` → Require PR  
4. En el chat del agente: **`repo listo`**

El agente importa el seed por PR.

## Opción script (tu máquina con `gh` admin)

```bash
cd /path/to/nortiqa-lab-.github   # branch con el seed (o main tras merge #16)
bash exports/nortiqa-lab-governance/apply.sh
```

## Después

- Merge PR #16 · cerrar PR #15 (duplicado)  
- SQL staging / redirects Notion: **solo con tu OK explícito**
