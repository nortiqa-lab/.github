# NORTIQA Vanguard — visión de plataforma operativa

Estado: DEV / Borrador

No es documentación oficial. Requiere auditoría de Claude / ARCHITECT-001
y ratificación de Gio para pasar a PROD.

| Campo | Valor |
|-------|--------|
| Fecha | 2026-08-02 |
| Actor | Cursor / `NL-BUILDER` (captura) · fuente: visión Gio |
| Canon Notion | unavailable — bootstrap usado |
| Alcance | Nortiqa Lab only |
| Nombre interno | **NORTIQA Vanguard** |

## 1. Tesis

**Hecho (sesión):** Gio define el objetivo no como “un bot de Telegram con muchos modelos”, sino como el prototipo de la plataforma operativa más avanzada de Nortiqa.

**Inferencia:** la ventaja competitiva no viene de enchufar cada modelo nuevo, sino de cerrar el ciclo:

```text
entender misión → diseñar plan → ejecutar bajo límites
→ verificar resultado → aprender sin perder control humano
```

**Recomendación estratégica (Gio):** cada generación debe aumentar **simultáneamente** capacidad, verificabilidad y control. Si solo sube autonomía → riesgo. Si solo agrega modelos → demo. Si logra las tres → obra de arte tecnológica.

## 2. Qué no es / qué sí es

| No es | Sí es |
|-------|--------|
| Chat wrapper multi-modelo | Compilador de intención + ejecución gobernada |
| Agente todopoderoso | Células especializadas con árbitro e evidencia |
| Memoria = historial de chats | Cuatro memorias operativas con gate de promoción |
| “Listo” conversacional | Cierre verificable con pruebas observables |
| Dependencia de un proveedor | Motores reemplazables + modo soberano degradado |

Relación con el kit actual (`agents/`): los roles `NL-*` son el germen de las células; `AUTONOMY.md` es el germen de los niveles 0–5; los handoffs son el germen de la memoria episódica. Vanguard **extiende** ese contrato; no inventa un segundo canon.

## 3. Arquitectura objetivo

```text
Pedido humano
    ↓
Compilador de intención
    ↓
Contrato de misión verificable
    ↓
Planificador
    ↓
Célula de agentes especializados
    ↓
Simulación / vista previa
    ↓
Ejecución gobernada
    ↓
Verificación independiente
    ↓
Evidencia + aprendizaje operativo
```

### 3.1 De mensajes a contratos de misión

Cada pedido natural se convierte en una estructura con:

| Campo | Propósito |
|-------|-----------|
| Objetivo + criterio de éxito | Qué cuenta como “terminado” |
| Archivos, servicios y datos autorizados | Boundary de blast radius |
| Riesgo y permisos requeridos | Clasificación de autonomía |
| Plan, rollback y pruebas | Camino ejecutable y reversible |
| Presupuesto (tiempo, tokens, dinero) | Límite económico/operativo |
| Evidencia necesaria para cerrar | Checklist observable |
| Acciones con aprobación humana | Gate explícito |

Así, “mejorá el README” y “recuperá el servidor” dejan de ser prompts sueltos: son misiones trazables.

### 3.2 Células de agentes (no un agente único)

Para trabajos importantes:

| Función | Rol kit actual (mapa, no rename) | Nota |
|---------|----------------------------------|------|
| Planifica | `NL-ORCH` | Diseña contrato + plan |
| Implementa | `NL-BUILDER` | Ejecuta cambios reversibles |
| Prueba | (capacidad a formalizar; hoy embebida en BUILDER/OPS) | Evidencia positiva/negativa |
| Revisa seguridad | `NL-AUDITOR` (postura) | Gates, no auto-certificación |
| Opera infra | `NL-OPS` | Staging/prod con gates |
| Árbitro | `NL-AUDITOR` / orquestación | Compara resultados independientes |
| Aprobación final | **Gio** | Cuando el nivel lo exige |

**Regla dura:** el ejecutor nunca certifica solo su propio trabajo.

**Inferencia:** los perfiles SC2027 / roles del kit permiten empezar la separación sin esperar Gen6 completa.

### 3.3 Simulación antes de actuar (gemelo digital operativo)

Salto tecnológico prioritario post–Mission Control:

- Predecir servicios y archivos afectados
- Mostrar diff esperado
- Ensayar migraciones sobre base restaurada
- Simular reinicios y dependencias
- Calcular blast radius
- Preparar rollback y restore point automáticamente

Respuesta tipo de interfaz:

> Entendí la misión. Afectará 3 archivos y un servicio. Preparé backup, prueba y rollback. Riesgo medio. ¿Autorizás la ejecución?

### 3.4 Autonomía adaptativa (niveles 0–5)

| Nivel | Capacidad | Control |
|-------|-----------|---------|
| 0 | Responder / analizar | Solo lectura cognitiva |
| 1 | Inspeccionar y diagnosticar | Lectura + evidencias |
| 2 | Modificar archivos reversibles en staging | Diff + rollback de archivos |
| 3 | Operar servicios permitidos con rollback | Restore point obligatorio |
| 4 | Migraciones, red o integraciones externas | Autorización humana |
| 5 | Producción | Siempre gobernada + aprobación humana |

**Regla:** bajar autonomía automáticamente ante incertidumbre, drift, señales contradictorias o falta de evidencia.

**Mapa con kit actual (borrador):** green ≈ 0–2; yellow ≈ 2–3 con notify; red ≈ 4–5 / `AUTONOMY.md` red zone. Afinar en Gen5.

### 3.5 Verificación basada en evidencia

Para declarar misión terminada, exigir pruebas observables (según tipo):

- Diff final
- Tests positivos y negativos
- Estado anterior / posterior
- PID / reinicio cuando corresponda
- Respuesta HTTP o resultado funcional real
- Captura o aceptación humana si interviene UI
- Confirmación de no contaminación de archivos compartidos por pruebas/agentes

“Terminado” = significado técnico, no conversacional.

### 3.6 Memoria operativa (cuatro capas)

| Memoria | Contenido | Promoción |
|---------|-----------|-----------|
| Semántica | Arquitectura, decisiones, reglas | Canon / docs versionables |
| Episódica | Qué ocurrió en cada misión | Handoffs / caja negra |
| Procedimental | Recetas verificadas | Solo tras repetición exitosa + revisión |
| Predictiva | Patrones que anticipan fallos | Desde episodios + evals |

**Nunca** aprender comandos arbitrarios desde mensajes sueltos.

### 3.7 Caja negra y reproducción

Cada misión genera registro con:

- Decisiones de routing
- Agentes y modelos usados
- Herramientas invocadas
- Aprobaciones
- Evidencias
- Costos y tiempos
- Fallos, reintentos, fallback
- Resultado y rollback disponible

Reproducción en modo simulación para forensia (“por qué funcionó / falló”).

### 3.8 Evaluación continua

Campo de pruebas propio (benchmark versionado), incluyendo:

- Cientos de misiones sintéticas
- Prompt injection
- Secretos simulados
- Fallos de red / APIs / modelos
- Cambio de intención mid-task
- Usuarios concurrentes
- Locks, timeouts, cancelaciones
- Modelos contradictorios
- Degradación cuando desaparece un proveedor

**Gate de deploy:** cada nueva generación debe superar el benchmark anterior.

### 3.9 Independencia de modelos

Los modelos (Codex, Claude, Cursor, Groq, Gemini, locales, etc.) son **motores reemplazables**.

Router selecciona por: capacidad en evals propias, riesgo, herramientas, latencia, privacidad, costo, estado del proveedor, calidad histórica por tipo de tarea.

Para decisiones críticas: dos modelos en paralelo + tercero que arbitra; la mayoría **no** sustituye evidencia.

### 3.10 Modo degradado y soberano

Cuando falla Internet o un proveedor, seguir útil:

- Diagnóstico determinístico local
- Procedimientos de recuperación compilados
- Caché de documentación operativa
- Modelo local pequeño para clasificación
- Cola de misiones pendientes + sync posterior
- **Nunca** degradar seguridad para mantener disponibilidad

## 4. Roadmap de generaciones

| Gen | Nombre | Enfoque |
|-----|--------|---------|
| **Gen4** | (cierre previo) | Lenguaje natural operativo + aceptación humana |
| **Gen5** | Mission Control | Contrato de misión, permisos, plan, evidencia, cierre verificable |
| **Gen6** | Agent Cells | Planificador, implementador, tester, security reviewer, árbitro |
| **Gen7** | Digital Twin | Simulación, blast radius, backups, rollback ensayado |
| **Gen8** | Operational Intelligence | Memoria procedimental, predictiva, evaluaciones continuas |
| **Gen9** | Sovereign NORTIQA | Independencia de proveedores + operación local degradada |
| **Gen10** | Governed Autonomy | Autonomía prolongada con autoridad humana, límites criptográficos, prod separada |

**Orden recomendado (Gio):** cerrar Gen4 primero; luego Gen5→Gen10 en secuencia.

### Criterio de avance entre generaciones

Una generación solo avanza si mejora **las tres** dimensiones:

1. Capacidad (qué puede hacer)
2. Verificabilidad (cómo se prueba que lo hizo bien)
3. Control (quién autoriza, qué límites, qué rollback)

## 5. Relación con este repositorio

| Superficie | Rol respecto a Vanguard |
|------------|-------------------------|
| `agents/` kit `NL-*` | Semilla de células y autonomía |
| `docs/shared-ai-memory/` | Semilla de memoria episódica / handoffs |
| `docs/dev/` (este doc) | Visión DEV versionable |
| Product repo `giovanyalbea-dotcom/nortiqa-lab` | Implementación runtime / Gen4+ (fuera de este org-profile salvo exports) |
| Notion `MEM-NL-ROOT-001` | Canon; este doc no lo reemplaza |
| Telegram / bot actual | Canal de entrada posible; **no** la arquitectura |

## 6. Fuera de alcance de esta captura

- Implementar Gen5+ en código
- Escribir a Notion canon
- Cambios en VPS / prod / secretos
- Renombrar roles `NL-*` ni host SC2027
- Declarar Gen4 cerrado (estado Gen4: **PENDIENTE DE VALIDACIÓN** en el repo de producto/ops)

## 7. Verificación de esta captura (2026-08-02)

| Check | Resultado |
|-------|-----------|
| Notion `MEM-NL-ROOT-001` | unavailable (`needsAuth`) — draft |
| Paths `agents/`, `docs/dev/`, handoffs | existen |
| Docs Gen4/Telegram/Vanguard previos en este repo | no encontrados (0 matches) |
| Secretos en el diff | ninguno |
| Prod / DNS / VPS tocados | no |

## 8. Próximo paso recomendado (uno)

Cerrar **Gen4** en el repo de producto/ops. Schema Gen5: [`GEN5-MISSION-CONTROL.md`](./GEN5-MISSION-CONTROL.md). Dry-run compiler en kit: [`GEN5-MISSION-COMPILER-DRY-RUN.md`](./GEN5-MISSION-COMPILER-DRY-RUN.md) (`python3 tools/mission-compiler/compile.py --self-test`).
