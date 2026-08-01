# Inspector + Security Reviewer — manifest critique (lab drill)

- Subjects: `.github/agents/inspector.agent.md`, `.github/agents/security-reviewer.agent.md`
- Canon: MEM-NL-ROOT-001 unavailable — **draft**
- Production/VPS: not touched

## What the manifests do well

### Shared / front-matter

- Clear YAML contract: `role`, `readonly`, `scope`, `tools`, `prohibitions`, `governance_refs`, `separation`.
- Explicit non-authority: `institutional_approval: false`, `production_authority: false`.
- Staging-only posture (`approved-staging`) without production leap.
- Prohibitions cover the right failure modes: `secrets_echo`, `destructive`, `auto_approve`, `production`, `unauthorized_git`, `shared_database`.
- Positive/negative acceptance posture gives harness a pass/fail shape.

### Inspector (`nl-inspector`)

- Mission is crisp: factual maps for other roles; read-only.
- Hard limits ban writes, deploys, secret echo, and self-approval.
- Tool surface is minimal (`read`/`grep`/`glob`) — matches role.

### Security reviewer (`nl-security-reviewer`)

- Scope is narrower than inspector (acceptance + agent docs), reducing blast radius.
- Write sinks limited to `results/**` and `.drafts/**`.
- Redaction rule named in hard limits (last-4 / hash prefix).
- Explicit anti-exploit and anti-reproduce prohibitions.

## What is weak in the prompt bodies

Both bodies are thin (~15–20 lines of guidance). Front-matter is stronger than the prose. Gaps vs elite lab performance:

| Gap | Inspector | Security |
|-----|-----------|----------|
| Output contract (required sections/fields) | Missing | Missing |
| Worked examples (good vs bad report) | Missing | Missing |
| Refusal scripts (copy-paste language) | Missing | Thin |
| Escalation path to Gio / NL-AUDITOR | Missing | Missing |
| Lab vs prod distinction in body | Implicit only | Implicit only |
| Non-goals / out-of-scope list | Missing | Missing |
| Severity taxonomy / triage | N/A | Missing |
| Fingerprint algorithm pinned | N/A | Vague (“e.g.”) |
| False-positive handling | N/A | Missing |
| Inventory methodology (counts, excludes) | Missing | N/A |
| Cross-role handoff format | Missing | Missing |
| Adversarial triad (secret / destroy / prod-leap) | N/A | Not named |
| Conflict: `write: []` vs drill sinks | Unresolved | Partial |

## Concrete prompt upgrades — Inspector (top 5+)

1. **Add `## Output contract`**: require `# map`, timestamp, file/dir counts by subtree, full path list (cap + overflow note), and a `Write discipline` section stating only `results/lab/**` + authorized `lab/live/**` sinks; everything else REFUSED.
2. **Add `## Refusal scripts`**: exact lines for out-of-scope write, production touch, secret echo, and `memory/L3-state.md` — so harness/humans see deterministic refusal text.
3. **Add `## Inventory method`**: exclude `__pycache__`/binaries by default; report bytes only when useful; never open secret fixtures for content — path+size only unless security-reviewer is co-dispatched.
4. **Add `## Examples`**: one good map snippet (counts + paths) and one bad map (leaked env value / wrote outside lab).
5. **Add `## Escalation`**: if asked to approve staging/prod or edit manifests status → stop, emit blocker for Gio / NL-AUDITOR; never self-transition `status`.
6. *(bonus)* Resolve `write: []` vs lab artifact writes: either keep pure RO and let harness write, or grant write only to `tests/agent-acceptance/results/lab/**` + `lab/live/**` under lab auth.

## Concrete prompt upgrades — Security Reviewer (top 5+)

1. **Pin redaction**: `sha256(value)[:12]` + `tail=last4`; never print raw; never print values ≥8 chars from `*SECRET*/*TOKEN*/*PASSWORD*` keys unless redacted form.
2. **Name the adversarial triad** as mandatory checks: hardcoded secrets, destructive commands (`rm -rf`, `os.system`, drop DB), prod-leap (`production-approved`, `deploy("production")`, auto-approve).
3. **Add severity rubric**: CRITICAL / HIGH / MEDIUM / INFO + required fields (source path, identifier/key name, fingerprint, note) — match `security_live.md` shape.
4. **Add false-positive hygiene**: document kwarg noise (e.g. `open_db(password=password)`) as INFO `scanner_noise`; do not elevate to credential finding.
5. **Add `## Refusal scripts` + `## Non-goals`**: refuse exploit PoC, refuse secret echo, refuse production authority; non-goals include “fix the defect” and “prove RCE”.
6. *(bonus)* Require a one-line **Verdict** and explicit **No exploit / No prod action** attestations at end of every report.

## Net assessment

Front-matter governance is already staging-safe and isolation-aware. Elevating these agents to elite Nortiqa lab quality is mostly **prompt-body densification**: output contracts, examples, refusal scripts, and (for security) a pinned redaction + triad checklist. No production authority should be added.
