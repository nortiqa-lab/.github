#!/usr/bin/env bash
# Public healthcheck for ERP-Nortiqa-Lab (no SSH, non-destructive).
set -euo pipefail

fail=0

check_http() {
  local name="$1"
  local url="$2"
  local expect_code="$3"
  local code
  code="$(curl -sS -o /tmp/erp-nl-health.body -w '%{http_code}' --max-time 20 "$url" || true)"
  if [[ "$code" == "$expect_code" ]]; then
    echo "OK   $name ($code)"
  else
    echo "FAIL $name (got ${code:-none}, want $expect_code) — $url"
    head -c 120 /tmp/erp-nl-health.body 2>/dev/null | tr '\n' ' ' || true
    echo
    fail=1
  fi
}

check_body_contains() {
  local name="$1"
  local url="$2"
  local needle="$3"
  local code
  code="$(curl -sS -o /tmp/erp-nl-health.body -w '%{http_code}' --max-time 20 "$url" || true)"
  if [[ "$code" == "200" ]] && grep -Fq "$needle" /tmp/erp-nl-health.body; then
    echo "OK   $name"
  else
    echo "FAIL $name (http=${code:-none}, missing '$needle') — $url"
    head -c 120 /tmp/erp-nl-health.body 2>/dev/null | tr '\n' ' ' || true
    echo
    fail=1
  fi
}

echo "ERP-Nortiqa-Lab public health — $(date -u +%Y-%m-%dT%H:%M:%SZ)"

check_body_contains "Odoo health" "https://erp.nortiqalab.com/web/health" '"status": "pass"'
check_http "Odoo login" "https://erp.nortiqalab.com/web/login" "200"
check_body_contains "flow n8n healthz" "https://flow.nortiqalab.com/healthz" '"status":"ok"'

# Metabase: 200 healthy; 503 + paused message = degraded but named
bi_code="$(curl -sS -o /tmp/erp-nl-bi.body -w '%{http_code}' --max-time 20 https://bi.nortiqalab.com/ || true)"
if [[ "$bi_code" == "200" ]]; then
  echo "OK   Metabase (200)"
elif grep -Fq "Metabase paused on ERP-Nortiqa-Lab" /tmp/erp-nl-bi.body 2>/dev/null; then
  echo "FAIL Metabase paused on ERP-Nortiqa-Lab (503) — unpause on host"
  fail=1
else
  echo "FAIL Metabase (got ${bi_code:-none})"
  head -c 120 /tmp/erp-nl-bi.body 2>/dev/null | tr '\n' ' ' || true
  echo
  fail=1
fi

if curl -sS --max-time 20 https://erp.nortiqalab.com/jsonrpc \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","method":"call","params":{"service":"common","method":"version","args":[]},"id":1}' \
  | grep -Fq '"server_serie": "18.0"'; then
  echo "OK   Odoo version serie 18.0"
else
  echo "FAIL Odoo version probe"
  fail=1
fi

echo "---"
if [[ "$fail" -eq 0 ]]; then
  echo "RESULT: PASS"
else
  echo "RESULT: FAIL (see readiness runbook agents/runbooks/erp-nortiqa-lab-readiness.md)"
fi
exit "$fail"
