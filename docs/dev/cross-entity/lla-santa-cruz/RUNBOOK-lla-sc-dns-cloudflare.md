Estado: DEV / Borrador

No es documentación oficial. Requiere auditoría de Claude / ARCHITECT-001
y ratificación de Gio para pasar a PROD.

# Runbook — Delegar `llasantacruz.com.ar` a Cloudflare Free

Relacionado: [`DEC-LLA-SC-DNS-001-cloudflare.md`](./DEC-LLA-SC-DNS-001-cloudflare.md)

Operador: humano con acceso a Cloudflare + NIC Argentina (Gio).  
Agentes: solo lectura / documentación; **no** ejecutar cambios de DNS.

## RACI (este flujo)

| Actividad | A | R | C | I |
|-----------|---|---|---|---|
| Decisión Cloudflare Free (no Hostinger NS) | Gio | Cursor/docs (`NL-BUILDER`) | `NL-AUDITOR` | `NL-MEMORY` |
| Add domain Free + obtener NS | Gio | Claude Chrome o Gio en dashboard | Cursor (brief) | Auditor |
| Delegar NS en NIC | Gio | Claude Chrome o Gio en nic.ar | Cursor (texto exacto) | Auditor |
| Registro `A portal` | Gio | Claude Chrome / Gio | Cursor, OPS | Memory |
| Nginx + TLS | Gio | OPS / humano en servidor | Auditor | Memory |
| Verify `dig` | Gio | Cursor (check público) | Claude Chrome | Memory |

RACI global de modelos/roles: [`../../RACI-MODELS-AND-ROLES.md`](../../RACI-MODELS-AND-ROLES.md).

## Precondiciones

- [ ] Dominio `llasantacruz.com.ar` visible y administrable en NIC Argentina.
- [ ] Cuenta Cloudflare disponible (o lista para crear).
- [ ] IP pública del servidor propio conocida (para el registro `A` del portal).
- [ ] Confirmado: **no** se usará Hostinger como DNS de este dominio.
- [ ] Confirmado: **no** modificar DNS de `nortiqalab.com`.

## Pasos

### 1. Cloudflare — alta de dominio

1. Iniciar sesión en Cloudflare.
2. **Add a domain**.
3. Ingresar exactamente: `llasantacruz.com.ar`.
4. Elegir plan **Free**.
5. Continuar hasta que Cloudflare muestre **dos nameservers** propios (ej. `*.ns.cloudflare.com`).
6. Copiar los **valores exactos** del dashboard (no inventar ni reutilizar NS de otro dominio).

### 2. NIC Argentina — delegación

1. Iniciar sesión en https://nic.ar/
2. Abrir `llasantacruz.com.ar`.
3. Seleccionar **Delegar**.
4. Reemplazar la delegación actual por los **dos** nameservers de Cloudflare.
5. Guardar / **Ejecutar cambios** según el flujo de NIC.
6. No usar nameservers Hostinger (`dns-parking`, `horizon`/`orbit.dns-parking.com`, etc.).

### 3. Esperar activación

1. En Cloudflare, esperar estado de dominio activo (hasta ~24–48 h típico).
2. Verificar desde una máquina con red:

```bash
dig NS llasantacruz.com.ar +short
# Esperado: los dos NS de Cloudflare (ya no NXDOMAIN)
```

### 4. Registro del portal

En Cloudflare DNS, crear:

```text
Tipo: A
Nombre: portal
Destino: <IP pública del servidor propio>
TTL: Auto
Proxy status: DNS only (gris) hasta validar Nginx + certificado
```

Verificar:

```bash
dig A portal.llasantacruz.com.ar +short
# Esperado: la IP pública del servidor
```

### 5. Servidor (fuera de DNS; OPS separado)

1. Configurar Nginx como reverse proxy para `portal.llasantacruz.com.ar`.
2. Emitir/renovar TLS (p. ej. Let’s Encrypt) en el servidor.
3. Solo después de HTTPS estable, evaluar Cloudflare proxy naranja si se desea.

## Rollback

Si algo falla tras cambiar NIC:

1. No improvisar NS de Hostinger parking.
2. Volver a los NS anteriores **solo si** estaban documentados y la zona existía.
3. Si el estado previo era sin delegación (NXDOMAIN), el rollback es restaurar la delegación NIC anterior registrada en captura/screenshot, o dejar Cloudflare y corregir registros.

## Criterios de listo

- [ ] `dig NS llasantacruz.com.ar` muestra NS Cloudflare.
- [ ] `dig A portal.llasantacruz.com.ar` muestra la IP del servidor.
- [ ] `nortiqalab.com` sigue con sus NS Hostinger sin cambios.
- [ ] Notion `DEC-LLA-SC-DNS-001` actualizado con NS reales (sin secretos) tras la ejecución.

## Contacto / escalamiento

Cualquier duda de producción, correo, o cruce con infra Nortiqa → escalar a Gio. No mezclar entidades.
