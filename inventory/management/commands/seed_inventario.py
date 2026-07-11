from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Sum

from inventory.models import Category, Movimentacao, Produto

OBSERVACAO_CARGA = "Carga inicial de inventário"

# (categoria, produto, quantidade) — inventário real.
INVENTARIO = [
    ("SSDs", "SSD SATA WDGreen 120Gb", 20),
    ("SSDs", "SSD SATA Kingston 120Gb", 10),
    ("SSDs", "SSD SATA Macrovip 120Gb", 15),
    ("Cabos", "Cabo de comunicação SATA", 40),
    ("Cabos", "Cabo Scanner Datalogic", 13),
    ("Scanners", "Scanner DataLogic com cabo", 7),
    ("Scanners", "Scanner DataLogic sem cabo", 3),
    ("Scanners", "Scanner Keyence (Base e cabos de comunicação)", 40),
    ("Scanners", "Base Datalogic para Scanner sem fio", 3),
    ("Sinaleiras", "Sinaleiras Stacklight Verde", 20),
    ("Sinaleiras", "Sinaleiras Stacklight Amarela", 17),
    ("Sinaleiras", "Sinaleiras Stacklight Vermelha", 23),
    ("Sinaleiras", "Sinaleiras Stacklight Buzzer", 6),
    ("IHMs", "IHM HLT15 Synatec", 6),
    ("IHMs", "IHM Synatec old", 3),
    ("IHMs", "IHM ACNode AtlasCopco", 7),
    ("Baterias", "Baterias Datalogic Scanner sem Fio", 10),
    ("Baterias", "Baterias Keyence Scanner sem Fio", 40),
    ("Carregadores", "Carregador de baterias Datalogic", 6),
    ("Carregadores", "Carregador de baterias Keyence", 40),
    ("Fontes", "Fonte de IHM HLT15", 11),
    ("Fontes", "Fonte IHM old", 4),
]


class Command(BaseCommand):
    help = "Carrega o inventário real, criando os saldos via movimentação de entrada."

    @transaction.atomic
    def handle(self, *args, **options):
        # 1. Salvaguarda anti-destruição: se houver qualquer movimentação que
        # não seja da carga inicial, existe histórico real e não podemos apagar.
        if Movimentacao.objects.exclude(observacao=OBSERVACAO_CARGA).exists():
            self.stderr.write(
                "Há movimentações reais no banco; seed abortado para não "
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
