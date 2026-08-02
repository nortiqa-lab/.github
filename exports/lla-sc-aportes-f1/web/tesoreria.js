(async function () {
  const $ = (id) => document.getElementById(id);

  async function loadJSON(path) {
    const res = await fetch(path);
    if (!res.ok) throw new Error("No se pudo cargar " + path);
    return res.json();
  }

  const config = await loadJSON("../config/app.json");
  const apiBase = (config.api_base_url || "http://127.0.0.1:8787").replace(/\/$/, "");

  function money(cents) {
    return new Intl.NumberFormat("es-AR", {
      style: "currency",
      currency: config.currency || "ARS",
      maximumFractionDigits: 0,
    }).format((cents || 0) / 100);
  }

  async function api(path, opts) {
    const res = await fetch(apiBase + path, {
      headers: { "Content-Type": "application/json" },
      ...opts,
    });
    const ctype = res.headers.get("content-type") || "";
    const data = ctype.includes("application/json") ? await res.json() : await res.text();
    if (!res.ok) throw new Error((data && data.error) || res.statusText);
    return data;
  }

  async function refresh() {
    try {
      const health = await api("/health");
      $("apiStatus").textContent =
        `API ${health.service || "ok"} · v${health.version || "?"} · payments_enabled=${health.payments_enabled}`;
      $("exportLink").href = apiBase + "/v1/treasury/export.csv";

      const summary = await api("/v1/treasury/summary");
      $("sumEntries").textContent = String(summary.entries);
      $("sumGross").textContent = money(summary.gross_cents);
      $("sumPending").textContent = String(summary.pending_reconcile);
      $("sumOk").textContent = String(summary.reconciled);

      const ledger = await api("/v1/ledger?limit=50");
      const tbody = $("ledgerTable").querySelector("tbody");
      tbody.innerHTML = "";
      const rows = ledger.ledger || [];
      if (!rows.length) {
        tbody.innerHTML = "<tr><td colspan='6' class='muted'>Sin movimientos simulados. Creá un aporte en /web/.</td></tr>";
        return;
      }
      for (const row of rows) {
        const tr = document.createElement("tr");
        const reconciled = Boolean(row.reconciled_at);
        const receiptCell = row.receipt_id
          ? `<a href="${apiBase}/v1/receipts/${row.receipt_id}.html" target="_blank" rel="noopener">${row.receipt_number || row.receipt_id}</a>`
          : "—";
        tr.innerHTML = `
          <td>${(row.created_at || "").slice(0, 16)}</td>
          <td>${money(row.amount_gross_cents)}</td>
          <td>${row.destination_id || "—"}</td>
          <td>${receiptCell}</td>
          <td>${reconciled ? "conciliado" : "pendiente"} <span class="muted">${row.status || ""}</span></td>
          <td></td>
        `;
        const btn = document.createElement("button");
        btn.type = "button";
        btn.className = "btn secondary";
        btn.textContent = reconciled ? "Desmarcar" : "Conciliar";
        btn.addEventListener("click", async () => {
          btn.disabled = true;
          try {
            const action = reconciled ? "unreconcile" : "reconcile";
            await api(`/v1/ledger/${row.id}/${action}`, {
              method: "POST",
              body: JSON.stringify({
                actor: "tesoreria-ui",
                note: "acción desde web/tesoreria.html (simulación)",
              }),
            });
            await refresh();
          } catch (err) {
            alert(err.message || String(err));
            btn.disabled = false;
          }
        });
        tr.lastElementChild.appendChild(btn);
        tbody.appendChild(tr);
      }
    } catch (err) {
      $("apiStatus").textContent =
        "API no disponible en " + apiBase + ". Arrancá: python3 api/server.py — " + (err.message || err);
    }
  }

  await refresh();
})();
