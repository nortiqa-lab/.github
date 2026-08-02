/**
 * CampaignRules engine (browser) — mirrors tools/campaign_rules.py
 * DEV / simulation only.
 */
(function (global) {
  const ALLOWED_LEGAL = new Set(["approved_for_staging", "approved_for_prod"]);

  function parseDay(value) {
    if (!value) return new Date().toISOString().slice(0, 10);
    return String(value).slice(0, 10);
  }

  function activeCampaigns(campaigns, now) {
    const day = parseDay(now);
    return (campaigns || [])
      .filter((c) => ALLOWED_LEGAL.has(c.legal_review_status))
      .filter((c) => c.window.start <= day && day <= c.window.end)
      .sort((a, b) => (b.priority || 0) - (a.priority || 0));
  }

  function evaluate(catalog, config, now, destinationId) {
    const day = parseDay(now);
    const base = [...(catalog.suggested_base_cents || [])];
    let display = [...base];
    const labels = [];
    const disclaimers = [config.disclaimer].filter(Boolean);
    const applied = [];
    const boosted = [];
    let floor = null;
    let cap = null;

    for (const camp of activeCampaigns(catalog.campaigns, day)) {
      const rule = camp.rule_type;
      const params = camp.params || {};
      const cid = camp.campaign_id;

      if (rule === "suggested_amount_override") {
        display = [...(params.suggested_base_cents || display)];
        applied.push(cid);
        labels.push(camp.title || cid);
      } else if (rule === "percent_reduction_on_suggested") {
        const pct = Number(params.percent || 0);
        display = display.map((v) => Math.max(0, Math.round(v * (1 - pct / 100))));
        applied.push(cid);
        labels.push(camp.title || cid);
      } else if (rule === "amount_floor") {
        floor = Number(params.floor_cents || 0);
        applied.push(cid);
      } else if (rule === "amount_cap") {
        cap = Number(params.cap_cents || 0);
        applied.push(cid);
      } else if (rule === "destination_boost") {
        if (params.destination_id) {
          boosted.push(params.destination_id);
          if (destinationId === params.destination_id) labels.push(camp.title || cid);
          applied.push(cid);
        }
      }
    }

    if (floor != null) display = display.map((v) => Math.max(floor, v));
    if (cap != null) display = display.map((v) => Math.min(cap, v));

    return {
      as_of: day,
      payments_enabled: !!config.payments_enabled,
      currency: config.currency || "ARS",
      suggested_base_cents: base,
      display_amounts_cents: display,
      labels,
      disclaimers,
      applied_campaign_ids: applied,
      boosted_destinations: boosted,
      floor_cents: floor,
      cap_cents: cap,
      simulation_only: !config.payments_enabled,
    };
  }

  function validateIntentAmount(amountCents, evaluation) {
    const errors = [];
    if (amountCents <= 0) errors.push("amount_must_be_positive");
    if (evaluation.floor_cents != null && amountCents < evaluation.floor_cents) {
      errors.push("below_floor");
    }
    if (evaluation.cap_cents != null && amountCents > evaluation.cap_cents) {
      errors.push("above_cap");
    }
    return {
      ok: errors.length === 0,
      errors,
      payments_enabled: evaluation.payments_enabled,
      checkout_allowed: evaluation.payments_enabled && errors.length === 0,
      mode: evaluation.payments_enabled ? "live" : "simulation",
    };
  }

  global.LlaCampaignEngine = { evaluate, validateIntentAmount, parseDay };
})(typeof window !== "undefined" ? window : globalThis);
