Estado: DEV / Borrador

No es documentación oficial. Requiere auditoría de Claude / ARCHITECT-001
y ratificación de Gio para pasar a PROD.

Fecha: 2026-08-02  
Actor: Cursor / `NL-OPS` (continuidad post-Codex)  
Fuente: evidencia host pegada por Gio + reporte Codex  
Verificación host: vía paste de Gio (este cloud agent no tiene SSH).

# Generación 4 — cierre del wrapper root

## Estado

**Wrapper root instalado + restore point creado.**  
Generación 4 (carril botctl / permisos) queda **cerrable en DEV** con un residual opcional de reload de `intent_router.py`.

No confundir con otros “cierres staging” del host (portal MVP A14, E6C estabilización, matriz permisos portal). Esos son carriles aparte.

## Hechos verificados (paste Gio 2026-08-02 ~00:16 UTC)

| Check | Resultado |
|-------|-----------|
| `/usr/local/sbin/sc2027-botctl` | `-rwxr-xr-x` `root:root` mode `755`, size 6239, mtime `Aug 2 00:14` |
| SHA256 root vs staging | **match** `27e083fcde5b35a7ea64d2d3382fc8eadc146a6fea3776a500f40a5450b1c116` |
| `sc2027-botctl --help` | `Accion no permitida.` (esperado: wrapper restrictivo; `--help` no es acción allowlisted) |
| `nortiqa-assistant-pilot.service` | `active` / `running`, MainPID `1069240`, `NRestarts=0` (up desde `2026-08-01 23:03:02 UTC`) |
| `nortiqa-assistant-oauth-callback.service` | `active` / `running` |
| Restore point | `/home/deploy/sc2027-staging/backups/gen4-closeout-20260802T001611Z` (botctl + `bot-permissions/` + install script + NOTES) |

Health público (cloud agent, no valida botctl): site/api/n8n `200`, mcp `401`.

## Hechos reportados por Codex (no re-ejecutados aquí)

- NL: salud, cancelación (“decime detenete”), métricas, respaldo, recuperación, autorreparación, reinicios permitidos.
- 75/75 pruebas OK pre/post reinicio previo.
- Manifiesto, ADR-040, L3 actualizados en staging.
- Previews en **loopback** (sin abrir puertos) — se mantiene.

## Comando privilegiado (ya ejecutado)

```bash
sudo install -o root -g root -m 0755 \
  /home/deploy/sc2027-staging/deploy/bot-permissions/sc2027-botctl \
  /usr/local/sbin/sc2027-botctl
```

## Residual (opcional, no bloquea el wrapper)

`install-nortiqa-assistant-pilot.sh` reportó `DEPLOY_DIFF:changed intent_router.py` y “servicios no iniciados”, pero el unit ya estaba `active` con PID de **23:03**. Inferencia: el proceso en memoria puede ser anterior al último copy de `intent_router.py`.

Para cargar el archivo en disco (solo si Gio quiere forzar reload Gen 4 NL):

```bash
# Preferir acción allowlisted del wrapper si existe (status/restart documentado en ADR-040).
# Si no: restart controlado del pilot únicamente — no tocar oauth salvo necesidad.
sudo systemctl restart nortiqa-assistant-pilot.service
systemctl show nortiqa-assistant-pilot.service -p ActiveState -p MainPID -p NRestarts --no-pager
```

No abrir puertos de preview. Canal remoto seguro (auth + vencimiento) = decisión aparte.

## Fuera de alcance de este cierre

- Aceptación portal MVP (`A14`)
- Plan E6C / limpieza Budibase / volúmenes
- Matriz fina de permisos del portal (datos sintéticos)
- Drift Compose / cookies Secure / Metabase SKIP

## Próximo paso recomendado (uno)

Ratificación Gio/auditoría del cierre Gen 4 wrapper; opcionalmente restart del pilot si se quiere garantizar `intent_router.py` en caliente.
