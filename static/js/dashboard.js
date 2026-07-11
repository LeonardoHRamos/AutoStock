// Gráficos do dashboard (Chart.js). Os dados chegam via <script type="application/json">
// (json_script do Django) e as cores são lidas do tema ativo (CSS custom properties),
// de modo que os gráficos se redesenham ao alternar claro/escuro.
(function () {
    "use strict";

    const readJSON = (id) => JSON.parse(document.getElementById(id).textContent);

    Chart.defaults.font.family = "system-ui, -apple-system, 'Segoe UI', sans-serif";

    function themeColors() {
        const cs = getComputedStyle(document.documentElement);
        const g = (name) => cs.getPropertyValue(name).trim();
        return {
            inkMuted: g("--ink-muted"),
            inkSecondary: g("--ink-secondary"),
            inkPrimary: g("--ink-primary"),
            grid: g("--grid"),
            accent: g("--accent"),
            accentHover: g("--accent-hover"),
            surface2: g("--surface-2"),
            border: g("--bs-border-color"),
        };
    }

    let charts = [];

    function renderCharts() {
        charts.forEach((c) => c.destroy());
        charts = [];

        const t = themeColors();
        Chart.defaults.color = t.inkMuted;
        Chart.defaults.borderColor = t.grid;

        const tooltip = {
            backgroundColor: t.surface2,
            titleColor: t.inkPrimary,
            bodyColor: t.inkSecondary,
            borderColor: t.border,
            borderWidth: 1,
            padding: 10,
            cornerRadius: 8,
            displayColors: false,
        };

        // Barras horizontais, uma única série → um único tom (sem arco-íris de rank).
        const barDataset = (data) => ({
            data,
            backgroundColor: t.accent,
            hoverBackgroundColor: t.accentHover,
            borderRadius: 4,
            borderSkipped: false,
            maxBarThickness: 26,
        });

        const options = (valueLabel) => ({
            indexAxis: "y",
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                tooltip: { ...tooltip, callbacks: { label: (c) => ` ${valueLabel}: ${c.parsed.x}` } },
            },
            scales: {
                x: {
                    beginAtZero: true,
                    grid: { color: t.grid, drawTicks: false },
                    border: { display: false },
                    ticks: { color: t.inkMuted, precision: 0 },
                },
                y: {
                    grid: { display: false },
                    border: { display: false },
                    ticks: { color: t.inkSecondary },
                },
            },
        });

        const catEl = document.getElementById("chartCategoria");
        if (catEl) {
            charts.push(new Chart(catEl, {
                type: "bar",
                data: { labels: readJSON("categoria-labels"), datasets: [barDataset(readJSON("categoria-values"))] },
                options: options("Quantidade"),
            }));
        }

        const muEl = document.getElementById("chartMaisUtilizados");
        if (muEl) {
            charts.push(new Chart(muEl, {
                type: "bar",
                data: { labels: readJSON("mais-utilizados-labels"), datasets: [barDataset(readJSON("mais-utilizados-values"))] },
                options: options("Saídas"),
            }));
        }
    }

    renderCharts();
    // Redesenha com as novas cores quando o tema é alternado.
    window.addEventListener("themechange", renderCharts);
})();
