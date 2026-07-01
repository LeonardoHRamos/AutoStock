from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render
from django.utils import timezone

from .models import Category, Movimentacao, Produto

# Limiar de estoque para considerar um produto "crítico".
# O handoff não previa campo de estoque mínimo por produto; usar constante
# ajustável até que essa regra de negócio seja definida.
ESTOQUE_CRITICO = 5


@login_required
def dashboard(request):
    produtos_criticos = (
        Produto.objects
        .select_related("category")
        .filter(quantidade__lte=ESTOQUE_CRITICO)
        .order_by("quantidade")
    )

    mais_utilizados = list(
        Produto.objects
        .filter(movimentacoes__tipo=Movimentacao.SAIDA)
        .annotate(total_saida=Sum("movimentacoes__quantidade"))
        .order_by("-total_saida")[:5]
    )

    por_categoria = (
        Category.objects
        .annotate(total=Sum("produtos__quantidade"))
        .order_by("-total")
    )

    agora = timezone.now()
    mov_mes = Movimentacao.objects.filter(
        data__year=agora.year,
        data__month=agora.month,
    )
    entradas_mes = mov_mes.filter(tipo=Movimentacao.ENTRADA).count()
    saidas_mes = mov_mes.filter(tipo=Movimentacao.SAIDA).count()

    context = {
        "estoque_critico": ESTOQUE_CRITICO,
        "produtos_criticos": produtos_criticos,
        "mais_utilizados": mais_utilizados,
        "entradas_mes": entradas_mes,
        "saidas_mes": saidas_mes,
        "total_produtos": Produto.objects.count(),
        # Séries para os gráficos (Chart.js), serializadas via json_script.
        "categoria_labels": [c.name for c in por_categoria],
        "categoria_values": [c.total or 0 for c in por_categoria],
        "mais_utilizados_labels": [p.codigo_interno for p in mais_utilizados],
        "mais_utilizados_values": [p.total_saida or 0 for p in mais_utilizados],
    }
    return render(request, "inventory/dashboard.html", context)
