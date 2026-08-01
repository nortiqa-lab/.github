# Autorización de laboratorio — agentes NORTIQA

## Texto de autorización (Gio)

Fecha: 2026-08-01  

> Te doy permiso para que los pruebes en el laboratorio, usa toda tu potencia para extraer lo mejor de ellos.

## Alcance autorizado por este texto

| Acción | ¿Autorizado? |
|--------|----------------|
| Ejercer agentes en sandbox `tests/agent-acceptance/lab/` | Sí |
| Subir manifiestos a `approved-staging` para lab | Sí (este texto) |
| Marcar runtime de lab activo (`lab/ACTIVE`) | Sí |
| Mejorar manifiestos / harness con evidencia de lab | Sí |
| Activar servicios VPS staging/prod | **No** |
| `production-approved` / promote producción | **No** |
| Autoaprobación institucional sin Gio | **No** (este texto es lab, no prod) |

## Implicación de estado

Con este texto, el evaluador puede:

1. Asignar `status: approved-staging` en manifiestos bajo prueba de lab.
2. Operar el laboratorio aislado (no VPS).
3. Emitir dictámenes de **lab performance** y proponer mejoras.

No puede asignar `production-approved` ni desplegar producción.

## Revocación

Gio puede revocar borrando o enmendando este archivo y devolviendo manifiestos a `reviewed`/`draft`.
