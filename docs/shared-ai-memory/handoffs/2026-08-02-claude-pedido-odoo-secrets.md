# Pedido a Claude (VS Code) — secretos Odoo para Cloud Agent

## Metadata

- Date: 2026-08-02
- Project: Nortiqa Lab
- AI actor: `NL-OPS` (Cursor Cloud) → handoff a Claude en VS Code
- Responsible user: Gio
- State: blocked waiting on secret injection

## Canon Read

- MEM-NL-ROOT-001: unavailable
- Outputs: **draft**

## Context for Claude

Cursor Cloud Agent identity (`cursor[bot]`) **cannot** read GitHub Actions secret values (`403`). GitHub never returns decrypted secrets via API. No `ODOO_*` / `SSH_*` env vars are injected in the cloud run.

Gio will run you in **VS Code** (authenticated) to recover the credentials and get them into the Cursor Cloud Agent without pasting them in chat.

Target system: Nortiqa-owned production ERP

- URL: `https://erp.nortiqalab.com`
- Host label: `ERP-Nortiqa-Lab` (`157.90.163.94`)
- App: Odoo 18 / Nerva
- Not “ERP Gio+Edson”; not LLA/SC2027 portal

---

## Pedido (copy-paste prompt for Claude in VS Code)

```text
PEDIDO NORTIQA — secretos Odoo para Cursor Cloud Agent
Estado: DEV / operativo. No imprimas secretos en el chat ni los commits.

Contexto:
- El Cloud Agent en cursor.com necesita entrar a https://erp.nortiqalab.com (Odoo 18 / Nerva, host ERP-Nortiqa-Lab).
- Ese agente NO puede leer GitHub Actions secrets (403). Vos en VS Code sí tenés la sesión de Gio.
- No mezclar con ERP Gio+Edson ni con el portal LLA en sc2027.nortiqalab.com.

Tu trabajo:
1) Localizá las credenciales de acceso al ERP de producción Nortiqa (usuario/email + password Odoo). Buscá en:
   - GitHub Secrets / Environments / Variables del repo o la org (nortiqa-lab, giovanyalbea-dotcom/nortiqa-lab)
   - Archivos locales de Gio (.env, password manager export, 1Password CLI, etc.) si están en el workspace
   - Historial de deploy / docs OPS solo para NOMBRES de variables, no para pegar valores
2) NO muestres los valores en el chat. Confirmá solo: encontrados / no encontrados + dónde (path o nombre del secret).
3) Dejá listos estos nombres para inyección en Cursor Cloud Agent → Secrets / Environment:
   - ODOO_USER
   - ODOO_PASSWORD
   - ODOO_DB          (opcional; omitir si usa DB por defecto)
   - ODOO_URL         (opcional; default https://erp.nortiqalab.com)
   Opcional host OPS:
   - SSH_HOST         (157.90.163.94 o hostname ERP)
   - SSH_USER
   - SSH_KEY          (privada; no imprimir)
4) Preferido: cargalos vos en la UI de Cursor (Cloud Agent / Environment Secrets) del run “Conexión ERP producción”, o dejale a Gio un checklist de 3 clics sin pegar valores en chat.
5) Si no existen aún, creá/actualizá GitHub Secrets con esos nombres (valores desde la fuente de verdad de Gio) y además indicá que hay que espejarlos a Cursor Secrets porque el Cloud Agent no lee Actions secrets.
6) Entregable al final (sin valores):
   - Tabla: variable | fuente | cargada_en_cursor (sí/no)
   - Un mensaje de una línea para el Cloud Agent: “Secretos ODOO_* inyectados; podés continuar.”

Restricciones:
- No commits con secretos.
- No logs, screenshots ni diffs con passwords.
- No auth tests destructivos en producción.
```

## Next Safe Step (Cloud Agent)

Tras el mensaje de Claude/Gio de que `ODOO_USER` / `ODOO_PASSWORD` están inyectados: re-chequear `printenv` (solo nombres), login a Odoo, continuar checklist C en `agents/runbooks/erp-nortiqa-lab-readiness.md`.
