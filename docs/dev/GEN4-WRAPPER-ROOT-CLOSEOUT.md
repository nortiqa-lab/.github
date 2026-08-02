Estado: DEV / Borrador

No es documentación oficial. Requiere auditoría de Claude / ARCHITECT-001
y ratificación de Gio para pasar a PROD.

Fecha: 2026-08-02  
Actor: Cursor / `NL-OPS` (+ continuidad `NL-BUILDER`)  
Fuente: handoff verbal de Codex (Generación 4 parcial)  
Verificación: este cloud agent **no** tiene SSH al VPS; no pudo ejecutar el `sudo install`.

# Generación 4 — cierre del wrapper root

## Hechos (reportados por Codex; no re-verificados aquí)

- Lenguaje natural: salud, cancelación, métricas, respaldo, recuperación, autorreparación, reinicios permitidos.
- El bot indica “decime detenete” (no exige `/cancelar`).
- 75/75 pruebas OK antes y después del reinicio.
- Servicio `active/running`, PID nuevo, `NRestarts=0`.
- Manifiesto, ADR-040 y L3 actualizados en staging VPS.
- Wrapper versionado reconciliado y validado en staging.
- Previews deliberadamente en **loopback** (sin abrir puertos).

## Bloqueo único restante (red zone — Gio)

Instalar el wrapper root en el VPS:

```bash
sudo install -o root -g root -m 0755 \
  /home/deploy/sc2027-staging/deploy/bot-permissions/sc2027-botctl \
  /usr/local/sbin/sc2027-botctl
```

Después: responder al agente con **ya está**.

## Post-install — healthcheck (SSH en VPS; no desde este cloud agent)

Ejecutar en el host (usuario `deploy` / sesión con sudo según corresponda):

```bash
# 1) Binario root instalado
ls -l /usr/local/sbin/sc2027-botctl
test -x /usr/local/sbin/sc2027-botctl && echo OK_EXECUTABLE
# Esperado: owner root:root, mode 0755

# 2) Servicio bot (ajustar unit name si el host usa otro)
systemctl is-active --quiet nortiqa-assistant.service \
  || systemctl is-active --quiet sc2027-bot.service \
  || systemctl --user is-active --quiet nortiqa-assistant.service
systemctl show -p ActiveState -p SubState -p MainPID -p NRestarts --value \
  nortiqa-assistant.service 2>/dev/null \
  || systemctl show -p ActiveState -p SubState -p MainPID -p NRestarts --value \
  sc2027-bot.service 2>/dev/null

# 3) Wrapper smoke (solo lectura / help — no reiniciar prod)
/usr/local/sbin/sc2027-botctl --help 2>&1 | head -40
# o el subcomando documentado en ADR-040 / L3 para status

# 4) Suite local si sigue disponible en staging
cd /home/deploy/sc2027-staging
# comando de tests reportado por Codex (75/75) — re-ejecutar el mismo entrypoint del manifiesto
```

Health público (sin SSH; no prueba el wrapper):

```bash
curl -sS -o /dev/null -w "%{http_code} %{url_effective}\n" https://nortiqalab.com/
curl -sS -o /dev/null -w "%{http_code} %{url_effective}\n" https://api.nortiqalab.com/health
curl -sS -o /dev/null -w "%{http_code} %{url_effective}\n" https://n8n.nortiqalab.com/
curl -sS -o /dev/null -w "%{http_code} %{url_effective}\n" https://mcp.nortiqalab.com/
```

## Post-install — punto de restauración real

Antes de cerrar Generación 4, crear un punto de restauración **real** en el VPS (no inventar nombres de snapshot). Preferir el procedimiento ya usado en staging/ops del host; si se usa Hetzner snapshot u otro, dejar evidencia (ID + hora) en el handoff.

No abrir puertos de preview. Canal remoto seguro (auth + vencimiento) queda **fuera** de este cierre — decisión pendiente de Gio.

## Riesgos / gaps

| Item | Nota |
|------|------|
| Artefactos Gen 4 no están en `giovanyalbea-dotcom/nortiqa-lab` (GitHub) | Inferencia: trabajo vive en `/home/deploy/sc2027-staging/`; conviene versionar wrapper + ADR-040 + L3 al product repo después del closeout |
| Cloud agent sin SSH | No puede instalar ni validar wrapper; solo documentar + health público |
| Unit name del servicio | Codex no pegó el unit exacto; healthcheck local debe descubrirlo |
| Notion | MCP `needsAuth` — este doc es draft |

## Próximo paso

Gio ejecuta el `sudo install` arriba y responde **ya está** (idealmente pegando `ls -l /usr/local/sbin/sc2027-botctl`).
