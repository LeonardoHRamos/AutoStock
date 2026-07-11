// Alternância de tema claro/escuro: alterna, persiste e avisa os gráficos.
// A aplicação inicial do tema salvo é feita inline no <head> (evita "flash").
(function () {
    "use strict";
    var btn = document.getElementById("themeToggle");
    if (!btn) return;
    btn.addEventListener("click", function () {
        var atual = document.documentElement.getAttribute("data-bs-theme") === "light" ? "light" : "dark";
        var proximo = atual === "light" ? "dark" : "light";
        document.documentElement.setAttribute("data-bs-theme", proximo);
        try { localStorage.setItem("autostock-theme", proximo); } catch (e) {}
        window.dispatchEvent(new CustomEvent("themechange", { detail: proximo }));
    });
})();
