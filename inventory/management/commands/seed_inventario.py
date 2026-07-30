from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Sum

from inventory.models import Category, Movimentacao, Produto

OBSERVACAO_CARGA = "Carga inicial de inventário"

# (categoria, produto, quantidade) — dados fictícios para demonstração.
INVENTARIO = [
    ("Sensores", "Sensor indutivo M12", 14),
    ("Sensores", "Sensor fotoelétrico compacto", 18),
    ("Sensores", "Sensor capacitivo industrial", 10),
    ("Cabos", "Cabo Ethernet industrial", 32),
    ("Cabos", "Cabo de alimentação industrial", 26),
    ("Cabos", "Cabo de sinal blindado", 20),
    ("Fontes", "Fonte 24V DC", 14),
    ("Fontes", "Fonte compacta para painel", 10),
    ("Controladores", "Controlador compacto", 8),
    ("Controladores", "Módulo de entrada digital", 12),
    ("Controladores", "Módulo de saída digital", 16),
    ("Interfaces", "Interface de operação", 10),
    ("Interfaces", "Painel indicador", 14),
    ("Interfaces", "Conversor de interface", 8),
    ("Atuadores", "Atuador linear compacto", 15),
    ("Atuadores", "Relé de interface", 20),
    ("Atuadores", "Válvula solenoide genérica", 11),
    ("Componentes de rede", "Switch Ethernet industrial", 14),
    ("Componentes de rede", "Módulo de comunicação Ethernet", 16),
    ("Componentes de rede", "Conector de rede industrial", 18),
    ("Armazenamento", "SSD industrial 240 GB", 19),
    ("Armazenamento", "Unidade de armazenamento industrial", 19),
]


class Command(BaseCommand):
    help = "Carrega dados demonstrativos, criando os saldos via entrada."

    @transaction.atomic
    def handle(self, *args, **options):
        # 1. Salvaguarda anti-destruição: se houver qualquer movimentação que
        # não seja da carga inicial, existe histórico e não podemos apagar.
        if Movimentacao.objects.exclude(observacao=OBSERVACAO_CARGA).exists():
            self.stderr.write(
                "Há movimentações adicionais no banco; seed abortado para não "
                "apagar histórico."
            )
            return

        # 2. Limpeza dos dados de teste (ordem por causa do PROTECT).
        Movimentacao.objects.all().delete()
        Produto.objects.all().delete()
        Category.objects.all().delete()

        # 3. Usuário das entradas: superusuário, ou um usuário de sistema.
        User = get_user_model()
        usuario = User.objects.filter(is_superuser=True).first()
        if usuario is None:
            usuario, _ = User.objects.get_or_create(username="inventario")

        # 4. Categorias.
        categorias = {}
        for nome_categoria in dict.fromkeys(cat for cat, _, _ in INVENTARIO):
            categoria, _ = Category.objects.get_or_create(name=nome_categoria)
            categorias[nome_categoria] = categoria

        # 5. e 6. Produtos + entrada inicial de saldo.
        for nome_categoria, nome_produto, quantidade in INVENTARIO:
            produto, created = Produto.objects.get_or_create(
                nome=nome_produto,
                defaults={"category": categorias[nome_categoria]},
            )
            if created:
                Movimentacao.objects.create(
                    produto=produto,
                    tipo=Movimentacao.ENTRADA,
                    quantidade=quantidade,
                    usuario=usuario,
                    observacao=OBSERVACAO_CARGA,
                )

        # 7. Resumo.
        total_quantidade = (
            Produto.objects.aggregate(total=Sum("quantidade"))["total"] or 0
        )
        self.stdout.write(self.style.SUCCESS(
            "Carga concluída: "
            f"{Category.objects.count()} categorias, "
            f"{Produto.objects.count()} produtos, "
            f"quantidade total = {total_quantidade}."
        ))
