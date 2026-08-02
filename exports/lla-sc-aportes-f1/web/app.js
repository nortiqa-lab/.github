(async function () {
  const $ = (id) => document.getElementById(id);

  async function loadJSON(path) {
    const res = await fetch(path);
    if (!res.ok) throw new Error("No se pudo cargar " + path);
    return res.json();
  }

  // Prefer sibling data/ from package root when served from /web/
  const config = await loadJSON("../config/app.json");
  const campaigns = await loadJSON("../data/campaigns.json");
  const destinationsDoc = await loadJSON("../data/destinations.json");

  let mode = "one_time";
  let selectedCents = null;
  const storageKey = "lla_sc_aportes_f1_intents";

  function money(cents) {
    return new Intl.NumberFormat("es-AR", {
      style: "currency",
      currency: config.currency || "ARS",
      maximumFractionDigits: 0,
    }).format(cents / 100);
  }

  function visibleDestinations() {
    return (destinationsDoc.destinations || []).filter((d) => d.ui_visible !== false && !d.electoral_circuit);
  }

  function evaluation() {
    return LlaCampaignEngine.evaluate(
      campaigns,
      config,
      new Date().toISOString().slice(0, 10),
      $("destination").value
    );
  }

  function renderDestinations(ev) {
    const select = $("destination");
    const current = select.value;
    select.innerHTML = "";
    for (const d of visibleDestinations()) {
      const opt = document.createElement("option");
      opt.value = d.id;
      opt.textContent = d.label + (ev.boosted_destinations.includes(d.id) ? " · destacado" : "");
      if (ev.boosted_destinations.includes(d.id)) opt.classList.add("boosted");
      select.appendChild(opt);
    }
    if ([...select.options].some((o) => o.value === current)) select.value = current;
  }

  function renderAmounts(ev) {
    const box = $("amountButtons");
    box.innerHTML = "";
    ev.display_amounts_cents.forEach((cents, idx) => {
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "amount-btn" + (selectedCents === cents ? " is-active" : "");
      const base = ev.suggested_base_cents[idx];
      btn.innerHTML =
        money(cents) +
        (base && base !== cents
          ? `<div class="muted" style="font-weight:400;font-size:0.8rem;text-decoration:line-through">${money(base)}</div>`
          : "");
      btn.addEventListener("click", () => {
        selectedCents = cents;
        $("amountInput").value = String(Math.round(cents / 100));
        render(ev);
      });
      box.appendChild(btn);
    });
  }

  function renderHistory() {
    const items = JSON.parse(localStorage.getItem(storageKey) || "[]");
    const list = $("historyList");
    list.innerHTML = "";
    if (!items.length) {
      list.innerHTML = "<li class='muted'>Sin simulaciones aún.</li>";
      return;
    }
    items.slice(0, 6).forEach((it) => {
      const li = document.createElement("li");
      li.textContent = `${it.created_at.slice(0, 16)} · ${it.mode} · ${money(it.amount_cents)} · ${it.status}`;
      list.appendChild(li);
    });
  }

  function render(ev) {
    $("payFlag").textContent = String(ev.payments_enabled);
    $("activeCamps").textContent = ev.applied_campaign_ids.join(", ") || "ninguna";
    $("floorCap").textContent = `${ev.floor_cents != null ? money(ev.floor_cents) : "—"} / ${
      ev.cap_cents != null ? money(ev.cap_cents) : "—"
    }`;
    $("disclaimerText").textContent = ev.disclaimers.join(" ");

    const banner = $("campaignBanner");
    if (ev.labels.length) {
      banner.hidden = false;
      banner.textContent = ev.labels.join(" · ");
    } else {
      banner.hidden = true;
    }

    renderDestinations(ev);
    renderAmounts(ev);

    $("submitBtn").textContent = ev.payments_enabled
      ? "Continuar al pago"
      : "Confirmar en simulación";
    $("simBadge").textContent = ev.payments_enabled ? "Cobros habilitados" : "Simulación · sin cobros";
    $("statusNote").textContent = ev.simulation_only
      ? "Checkout PSP bloqueado: payments_enabled=false. Se guarda un intent simulado localmente."
      : "Modo live (no debería ocurrir en F1).";
    renderHistory();
  }

  function saveIntent(intent) {
    const items = JSON.parse(localStorage.getItem(storageKey) || "[]");
    items.unshift(intent);
    localStorage.setItem(storageKey, JSON.stringify(items.slice(0, 50)));
  }

  $("tabOnce").addEventListener("click", () => {
    mode = "one_time";
    $("tabOnce").classList.add("is-active");
    $("tabMonth").classList.remove("is-active");
  });
  $("tabMonth").addEventListener("click", () => {
    mode = "recurring";
    $("tabMonth").classList.add("is-active");
    $("tabOnce").classList.remove("is-active");
  });
  $("destination").addEventListener("change", () => render(evaluation()));
  $("amountInput").addEventListener("input", () => {
    selectedCents = Math.round(Number($("amountInput").value || 0) * 100);
    render(evaluation());
  });

  $("submitBtn").addEventListener("click", () => {
    $("errorBox").hidden = true;
    $("receiptBox").hidden = true;
    const ev = evaluation();
    const amountCents = Math.round(Number($("amountInput").value || 0) * 100);
    const validation = LlaCampaignEngine.validateIntentAmount(amountCents, ev);
    const name = $("name").value.trim();
    const email = $("email").value.trim();
    const consent = $("consent").checked;

    if (!name || !email) {
      $("errorBox").hidden = false;
      $("errorBox").textContent = "Completá nombre y email.";
      return;
    }
    if (!consent) {
      $("errorBox").hidden = false;
      $("errorBox").textContent = "Se requiere consentimiento para datos sensibles.";
      return;
    }
    if (!validation.ok) {
      $("errorBox").hidden = false;
      $("errorBox").textContent = "Monto inválido: " + validation.errors.join(", ");
      return;
    }

    if (validation.checkout_allowed) {
      $("errorBox").hidden = false;
      $("errorBox").textContent = "Cobro live no implementado en F1.";
      return;
    }

    const intent = {
      id: "sim_" + Date.now(),
      mode,
      amount_cents: amountCents,
      amount_before_campaign_cents: ev.suggested_base_cents[0] || null,
      destination_id: $("destination").value,
      campaign_ids: ev.applied_campaign_ids,
      person: { name, email },
      status: "simulated_authorized",
      payments_enabled: false,
      created_at: new Date().toISOString(),
    };
    saveIntent(intent);
    $("receiptBox").hidden = false;
    $("receiptBox").innerHTML =
      `<strong>Comprobante simulado</strong><br>` +
      `${intent.id}<br>${money(amountCents)} · ${mode}<br>` +
      `Destino: ${intent.destination_id}<br>` +
      `No se debitó dinero.`;
    render(evaluation());
  });

  function money(cents) {
    return new Intl.NumberFormat("es-AR", {
      style: "currency",
      currency: config.currency || "ARS",
      maximumFractionDigits: 0,
    }).format(cents / 100);
  }

  // Initial suggested amount
  const firstEv = evaluation();
  selectedCents = firstEv.display_amounts_cents[0] || 0;
  $("amountInput").value = String(Math.round(selectedCents / 100));
  render(firstEv);
})().catch((err) => {
  console.error(err);
  document.body.insertAdjacentHTML(
    "afterbegin",
    `<p style="padding:1rem;color:#8b1e1e;font-weight:700">Error cargando F1: ${err.message}. Serví el paquete desde exports/lla-sc-aportes-f1 (no abras solo el HTML).</p>`
  );
});
