"""Mercado Pago adapter — DEV stub with hard stops."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class PspResult:
    ok: bool
    mode: str
    message: str
    psp_ref: str | None = None
    checkout_url: str | None = None
    details: dict[str, Any] | None = None


class MercadoPagoAdapter:
    """Never charges unless payments_enabled and sandbox credentials exist."""

    def __init__(self, config: dict):
        self.config = config
        psp = config.get("psp") or {}
        self.payments_enabled = bool(config.get("payments_enabled"))
        self.mode = psp.get("mode", "disabled_until_gates")
        self.access_token = psp.get("access_token_env")  # name of env var, not value

    def create_checkout(self, intent: dict) -> PspResult:
        if not self.payments_enabled:
            return PspResult(
                ok=False,
                mode="blocked",
                message="payments_enabled=false — checkout blocked (F2 hard stop)",
                details={"intent_id": intent.get("id")},
            )
        if self.mode != "sandbox":
            return PspResult(
                ok=False,
                mode="blocked",
                message=f"psp.mode={self.mode!r} — only 'sandbox' allowed before G8",
            )
        # No real token handling in this repo package.
        return PspResult(
            ok=False,
            mode="sandbox_stub",
            message=(
                "Sandbox adapter stub: set MP credentials outside git and implement "
                "Preference API only after G1+G7. No charge executed."
            ),
            details={"would_create_preference_for": intent.get("id")},
        )

    def handle_webhook(self, payload: dict) -> PspResult:
        if not self.payments_enabled:
            return PspResult(
                ok=False,
                mode="blocked",
                message="webhook ignored — payments_enabled=false",
                details={"keys": list(payload.keys())[:10]},
            )
        return PspResult(
            ok=False,
            mode="sandbox_stub",
            message="Webhook stub — no ledger mutation without verified MP signature",
        )
