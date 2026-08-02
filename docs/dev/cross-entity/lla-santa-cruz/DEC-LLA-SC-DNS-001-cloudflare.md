Estado: DEV / Borrador

No es documentación oficial. Requiere auditoría de Claude / ARCHITECT-001
y ratificación de Gio para pasar a PROD.

# DEC-LLA-SC-DNS-001 — DNS autoritativo Cloudflare Free

Fecha: 2026-08-02  
Actor: Cursor Cloud / `NL-ORCH` + `NL-BUILDER`  
Cruce de entidad: **autorizado por Gio** en esta sesión, solo para documentar DNS de LLA Santa Cruz. No mezclar secretos, datos ni ops de Nortiqa Lab.

Canon Notion (borrador hijo):  
https://app.notion.com/p/3b0e4fe3bfea81d1b55ac3a7043ec6a1  

Padre: `DOM-LLA-SC-001` — https://app.notion.com/p/3afe4fe3bfea81f49a3be9a6012108df

## RACI

| Actividad | A | R | C | I |
|-----------|---|---|---|---|
| Decisión de arquitectura DNS | Gio | Cursor (doc) | Auditor | Memory |
| Ejecución Cloudflare / NIC | Gio | Claude Chrome o Gio | Cursor | Auditor |
| Hosting + Nginx/TLS | Gio | OPS / humano servidor | Auditor | Memory |

Detalle: [`../../RACI-MODELS-AND-ROLES.md`](../../RACI-MODELS-AND-ROLES.md) §4 · Runbook: [`RUNBOOK-lla-sc-dns-cloudflare.md`](./RUNBOOK-lla-sc-dns-cloudflare.md).

## Decisión

| Componente | Proveedor |
| --- | --- |
| Registro y renovación | NIC Argentina |
| DNS autoritativo | Cloudflare Free |
| Alojamiento | Servidor propio |
| SSL y proxy inverso | Nginx en el servidor |

Separación explícita:

| Dominio | DNS |
| --- | --- |
| `llasantacruz.com.ar` | Cloudflare Free (camino definitivo) |
| `nortiqalab.com` | Hostinger — **sin cambios** |

## Hechos verificados (lectura pública, 2026-08-02)

| Chequeo | Resultado |
| --- | --- |
| `dig @8.8.8.8 NS llasantacruz.com.ar` | `NXDOMAIN` (SOA `com.ar` / NIC.AR) |
| `dig @1.1.1.1 NS llasantacruz.com.ar` | `NXDOMAIN` |
| `dig @8.8.8.8 A portal.llasantacruz.com.ar` | `NXDOMAIN` |
| `dig NS nortiqalab.com` | `horizon.dns-parking.com` / `orbit.dns-parking.com` |

### Inferencias (no hechos)

- Notion `DOM-LLA-SC-001` indica el dominio como **registrado**; la ausencia de NS públicos sugiere falta de delegación efectiva en NIC, o delegación no publicada aún.
- No se evidenció zona DNS Hostinger operativa para `llasantacruz.com.ar`.

### Recomendación

No apuntar NIC a nameservers Hostinger genéricos de parking. Usar Cloudflare Free y solo entonces crear `A portal`.

## Por qué no Hostinger como DNS

Documentación Hostinger (NIC.AR → Hostinger):

1. nic.ar no gestiona zona DNS; se delegan nameservers.
2. El dominio `.ar` / `.com.ar` debe estar **previamente agregado a un plan de hosting** en hPanel.
3. Recién ahí hPanel muestra los nameservers específicos del dominio.
4. Los dominios externos aparecen en External domains cuando ya están apuntados, pero el flujo documentado sigue ligado a hosting activo.

Fuentes:

- https://support.hostinger.com/en/articles/8041102-how-to-point-a-domain-from-nic-ar-to-hostinger
- https://support.hostinger.com/en/articles/1583408-can-external-domains-be-hosted-at-hostinger

En este caso:

- no hay hosting Hostinger contratado para LLA;
- el portal irá a servidor propio;
- cambiar NS sin zona previa puede dejar el dominio sin resolución.

**Prohibido:** usar `ns1.dns-parking.com` / `ns2.dns-parking.com` (u otros parking Hostinger) sin que hPanel haya creado y reconocido la zona.

## Qué no hizo este agente

- No cambió nameservers en NIC Argentina (zona roja: DNS).
- No creó cuenta/zona Cloudflare (requiere login humano).
- No tocó Nginx, VPS, secretos ni `nortiqalab.com`.

## Procedimiento humano

Ver runbook: [`RUNBOOK-lla-sc-dns-cloudflare.md`](./RUNBOOK-lla-sc-dns-cloudflare.md)

## Próximo paso seguro (uno)

Gio: en Cloudflare → **Add a domain** → `llasantacruz.com.ar` → plan **Free** → anotar los dos NS exactos → recién entonces **Delegar** en NIC Argentina.
