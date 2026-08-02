# Canal Telegram → equipo NL-*

Status: **proposed design / draft**  
Bot: [@NortiqaServidorOpsBot](https://t.me/NortiqaServidorOpsBot) (`ServidorOpsNortiqaBot`)  
Runtime (VPS, out of git): `/home/deploy/sc2027-staging/telegram-bridge/`  
Unit: `sc2027-telegram-agent.service`  
Manifest: `/home/deploy/sc2027-staging/docs/bots/telegram-bridge.yaml`  

This document does **not** assume VPS access and must not be treated as a deploy.  
Token stays only on the VPS (env/secret). Never commit it.

## Role of the bot

Telegram is an **ingress + notify channel**, not a second brain.

| Layer | Owns |
|-------|------|
| Bot / bridge (VPS) | Auth, parse, route, timeouts, reply formatting, local OPS tools |
| NL-* kit (this repo) | Roles, autonomy, dispatch, prompts, handoff contract |
| Notion | Canon when available |
| Cursor Cloud | Heavy versionable work when a human/agent opens a session |

Default personality of the bot name is OPS, but routing must still honor the full roster.

## Target architecture (staging first)

```
Gio (Telegram)
    │
    v
@NortiqaServidorOpsBot
    │  webhook or long-poll
    v
telegram-bridge  (sc2027-telegram-agent.service)
    │
    ├─ auth allowlist (Gio chat/user ids only)
    ├─ classify message → class A–E + NL role
    │
    ├─ GREEN local OPS ──► run staging-safe scripts / public health
    ├─ GREEN docs/kit ───► optional: write draft handoff on VPS staging docs
    ├─ BUILDER/PRODUCT ──► emit "Cursor brief" + optional Ollama draft reply
    ├─ AUDITOR/D/red ────► refuse or ask exact Gio gate; never auto-promote
    └─ always ───────────► reply with NL output contract + persist handoff stub
```

Production promote of this bot remains a **separate PAO** (existing hard stop in SC2027 promote checklist).

## Message → role routing

### Explicit commands (preferred)

| Command | Role | Notes |
|---------|------|-------|
| `/orch <goal>` | `NL-ORCH` | Default for free text too |
| `/ops <goal>` | `NL-OPS` | Health, staging checks, privileged command drafts |
| `/build <goal>` | `NL-BUILDER` | Returns brief/PR plan; no silent prod writes |
| `/product <goal>` | `NL-PRODUCT` | Public surface briefs |
| `/audit <goal>` | `NL-AUDITOR` | Gate only |
| `/memory` | `NL-MEMORY` | Last handoff summary / continuity |
| `/status` | bridge | Unit health, last job, role map (no secrets) |
| `/help` | bridge | Short command list |

### Free text

Treat as `/orch <text>` unless the text clearly matches a single OPS verb (`healthcheck`, `backup`, `certs`, `login portal`) → `NL-OPS`.

### Prefix override

`NL-OPS: …`, `NL-BUILDER: …` etc. force that role.

## Autonomy mapping on the bridge

Reuse `agents/AUTONOMY.md` zones:

| Zone | Bridge behavior |
|------|-----------------|
| Green | Execute locally if the action is staging-safe / read-only; reply with evidence |
| Yellow | Execute minimal adjacent step; flag in reply |
| Red | Do **not** run. Reply with exact human/root command or decision needed |

Red examples for this bot especially:

- promote staging→prod
- nginx reload / privileged file writes as root
- docker.sock experiments
- printing tokens / `.env`
- any Valent / ERP / client content

## Reply contract (Telegram)

Keep messages short. Mirror the NL output contract:

```
ROLE: NL-OPS
CANON: bootstrap-draft
DONE: public health OK (site/api/n8n 200, mcp 401)
VERIFY: curl evidence …
BLOCKED: none
NEXT: …
```

If truncated by Telegram length, send:

1. summary (≤3500 chars)
2. `HANDOFF: <path-or-id>` for the rest

## How the bridge should load NL-* brain

Do **not** fork a parallel prompt set on the VPS long-term.

Proposed sync (staging):

1. Versionable source of truth: this repo `agents/prompts/NL-*.md` + `SHARED_RULES.md` + `AUTONOMY.md` + `DISPATCH.md`.
2. Bridge config points to a local mirror path, e.g.  
   `/home/deploy/sc2027-staging/telegram-bridge/nl-kit/`  
   updated by a pull/copy job from `nortiqa-lab/.github` (read-only deploy key) **or** a manual sync until automation exists.
3. Manifest references those files as `system_prompt_paths` per role (see proposed YAML).

Until sync exists, bridge may embed a thin stub that says: “load kit from mirror; if missing, reply that kit sync is required”.

## Suggested split of responsibilities inside `telegram-bridge/`

```
telegram-bridge/
  app/                  # existing bot runtime
  nl/
    router.py           # NEW: command/free-text → NL role
    contracts.py        # NEW: output contract formatter
    autonomy.py         # NEW: green/yellow/red gates
  nl-kit/               # NEW: mirrored prompts (not secrets)
  README.md             # mention NL integration
```

No token in git. Token only in unit env / existing secret location.

## Security requirements (non-negotiable)

1. Allowlist Telegram `user_id` / `chat_id` for Gio only (staging).
2. Drop/ignore messages from others with no sensitive detail in logs.
3. Never echo env, tokens, or `.env` paths contents.
4. Rate-limit commands (e.g. 1 heavy OPS job / 30s).
5. Separate staging unit from any future prod unit.
6. Disable dangerous shell interpolation; allow only enumerated scripts for `NL-OPS` green actions.

## What Gio can do from Telegram after integration

- Ask `/ops health` and get live staging/public evidence.
- Ask `/orch …` and get a classified plan + NEXT.
- Get BLOCKED items as copy-paste root commands.
- Not: silent production changes, Notion protected writes, cross-entity ERP work.

## Out of scope for this proposal

- Deploying/restarting `sc2027-telegram-agent.service`
- Reading or rotating the bot token
- Wiring Cursor Cloud API launches (optional later)
- Promoting bot to production
