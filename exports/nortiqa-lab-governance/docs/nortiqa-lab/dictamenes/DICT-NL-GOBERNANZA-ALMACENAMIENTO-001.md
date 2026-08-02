# DICT-NL-GOBERNANZA-ALMACENAMIENTO-001

Estado: DEV / Borrador (stub)

No es documentación oficial. Requiere auditoría de Claude / ARCHITECT-001
y ratificación de Gio para pasar a PROD.

**Fecha stub:** 2026-08-02  
**Emisor stub:** Cursor / NL-BUILDER (desde instrucción Gio)  
**Bloqueo:** al crear este archivo, la página Notion `DICT-NL-GOBERNANZA-ALMACENAMIENTO-001` **no fue encontrada** vía búsqueda MCP. Este stub captura la matriz operativa comunicada por Gio hasta disponer del texto canónico.

## Objeto

Una sola política de almacenamiento documental para el ecosistema multi-entidad:

- Nortiqa Lab
- Valent Capital Group S.A.
- SC2027 (carpeta operativa / host)
- LLA Santa Cruz

## Matriz (según instrucción Gio 2026-08-02)

| Tipo | Destino |
|---|---|
| Documentos ratificados (PROD) | GitHub — repo privado `nortiqa-lab/governance` → `docs/[entidad]/[tipo]/` |
| Trabajo en curso (DEV) / tareas con estado | AppFlowy / Notion |
| Entregables externos + financieros/legales | Google Drive `90_COMPARTIR/POR_ENTIDAD/` |

## Diagrama de decisión

```text
¿El documento está ratificado (PROD)?
├── SÍ → GitHub (docs/[entidad]/[tipo]/)
└── NO (DEV) → ¿Es tarea/seguimiento con estados?
    ├── SÍ → AppFlowy/Notion (base de datos)
    └── NO → ¿Se comparte con externos?
        ├── SÍ → Google Drive (90_COMPARTIR/POR_ENTIDAD/)
        └── NO → AppFlowy/Notion (página)
```

## Relación con PLAN-NL-GITHUB-001

`PLAN-NL-GITHUB-001` / `DICT-NL-GITHUB-001` separan entidades por repositorio para código/datos/secretos.

**Propuesta de este dictamen:** superseder esa regla **solo para documentación PROD**, usando un repo privado multi-entidad con carpetas + CODEOWNERS/Teams. Código/datos/secretos permanecen separados por repo.

Pendiente: confirmación explícita de Gio en el texto canónico.

## Reglas universales

1. Naming existente (`DICT-[ENTIDAD]-…`, `REGLA-[ENTIDAD]-…`)
2. Separación de entidades por carpeta — nunca mezclar
3. Git flow por PRs — no commits directos a `main`
4. Notion: no borrar páginas migradas — solo redirect (con autorización)
5. Formato Markdown estándar
6. Migración progresiva de docs activos — no masiva sin aprobación
7. Prefijo de entidad ambiguo → preguntar a Gio

## Pendiente para cerrar stub → dictamen

- [ ] Pegar / vincular texto canónico ratificado por Gio
- [ ] URL Notion del dictamen (o confirmación de que nace en Git)
- [ ] Dictamen Claude / ARCHITECT-001
- [ ] Ratificación formal Gio
- [ ] Aplicar seed a repo `nortiqa-lab/governance` (ver `APPLY.md`)

## Referencias

- Prompt KNOW-001 ajustado: https://app.notion.com/p/3b0e4fe3bfea81c6acc2e485bdcf6558
- PLAN-NL-GITHUB-001 / DICT-NL-GITHUB-001 (canon previo de repos por entidad)
