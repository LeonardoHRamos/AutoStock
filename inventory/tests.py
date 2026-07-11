import io

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.db.models import Sum
from django.test import TestCase

from .models import Category, Movimentacao, Produto


class DerivacaoSaldoTests(TestCase):
    """A quantidade do produto deve derivar das movimentações."""

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user("operador", password="x")
        cls.categoria = Category.objects.create(name="SSDs")
        cls.produto = Produto.objects.create(nome="SSD X", category=cls.categoria)

    def _mov(self, tipo, quantidade):
        return Movimentacao.objects.create(
            produto=self.produto,
            tipo=tipo,
            quantidade=quantidade,
            usuario=self.user,
        )

    def test_entrada_incrementa_saldo(self):
        self._mov(Movimentacao.ENTRADA, 10)
        self.produto.refresh_from_db()
        self.assertEqual(self.produto.quantidade, 10)

    def test_saida_decrementa_saldo(self):
        self._mov(Movimentacao.ENTRADA, 10)
        self._mov(Movimentacao.SAIDA, 4)
        self.produto.refresh_from_db()
        self.assertEqual(self.produto.quantidade, 6)

    def test_editar_movimentacao_nao_reajusta_saldo(self):
        # Só a criação ajusta o saldo; edições não reajustam (histórico imutável).
        mov = self._mov(Movimentacao.ENTRADA, 10)
        mov.quantidade = 999
        mov.save()
        self.produto.refresh_from_db()
        self.assertEqual(self.produto.quantidade, 10)

    def test_str_usa_nome_do_produto(self):
        mov = self._mov(Movimentacao.SAIDA, 1)
        self.assertEqual(str(mov), "Saída - SSD X (1)")


class SeedInventarioTests(TestCase):
    """O comando de carga deve montar o inventário e proteger o histórico real."""

    def test_seed_gera_inventario_completo(self):
        call_command("seed_inventario", stdout=io.StringIO())
        self.assertEqual(Category.objects.count(), 8)
        self.assertEqual(Produto.objects.count(), 22)
        self.assertEqual(Produto.objects.aggregate(t=Sum("quantidade"))["t"], 344)
        # O saldo nasceu de entradas, não foi chumbado no campo.
        self.assertEqual(Movimentacao.objects.filter(tipo=Movimentacao.ENTRADA).count(), 22)

    def test_seed_aborta_quando_ha_movimentacao_real(self):
        user = get_user_model().objects.create_user("operador", password="x")
        categoria = Category.objects.create(name="SSDs")
        produto = Produto.objects.create(nome="SSD X", category=categoria)
        Movimentacao.objects.create(
            produto=produto,
            tipo=Movimentacao.ENTRADA,
            quantidade=5,
            usuario=user,
            observacao="uso real",
        )

        call_command("seed_inventario", stderr=io.StringIO())

        # A trava anti-destruição impediu a limpeza e a recarga.
        self.assertEqual(Produto.objects.count(), 1)
        self.assertEqual(Category.objects.count(), 1)
