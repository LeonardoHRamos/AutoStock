from django.conf import settings
from django.db import models


class Category(models.Model):
    """Agrupa os produtos por tipo (SSDs, Cabos, Scanners, ...)."""

    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Nome"
    )

    description = models.TextField(
        blank=True,
        verbose_name="Descrição"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Produto(models.Model):
    """Item de estoque.

    A ``quantidade`` é um valor DERIVADO: nunca é editada à mão, e sim
    recalculada a cada ``Movimentacao`` (ver ``Movimentacao.save``). Por isso
    ela é somente-leitura no admin.
    """

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="produtos",
        verbose_name="Categoria"
    )

    nome = models.CharField(
        max_length=200,
        verbose_name="Nome"
    )

    codigo_interno = models.CharField(
        max_length=50,
        unique=True,
        null=True,
        blank=True,
        verbose_name="Código interno"
    )

    descricao = models.TextField(
        blank=True,
        verbose_name="Descrição"
    )

    quantidade = models.IntegerField(
        default=0,
        verbose_name="Quantidade"
    )

    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"
        ordering = ["nome"]

    def __str__(self):
        return self.nome


class Movimentacao(models.Model):
    """Entrada ou saída de um produto no estoque.

    É a fonte da verdade do saldo: ao ser criada, ajusta a ``quantidade`` do
    produto correspondente. Edições posteriores NÃO reajustam o saldo (só a
    criação conta), mantendo o histórico imutável na prática.
    """

    ENTRADA = "entrada"
    SAIDA = "saida"
    TIPO_CHOICES = [
        (ENTRADA, "Entrada"),
        (SAIDA, "Saída"),
    ]

    produto = models.ForeignKey(
        Produto,
        on_delete=models.PROTECT,
        related_name="movimentacoes",
        verbose_name="Produto"
    )

    tipo = models.CharField(
        max_length=10,
        choices=TIPO_CHOICES,
        verbose_name="Tipo"
    )

    quantidade = models.PositiveIntegerField(
        verbose_name="Quantidade"
    )

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        verbose_name="Usuário"
    )

    data = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data"
    )

    observacao = models.TextField(
        blank=True,
        verbose_name="Observação"
    )

    class Meta:
        verbose_name = "Movimentação"
        verbose_name_plural = "Movimentações"
        ordering = ["-data"]

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.produto.nome} ({self.quantidade})"

    def save(self, *args, **kwargs):
        # O saldo do produto só é ajustado na criação da movimentação.
        is_new = self._state.adding
        super().save(*args, **kwargs)
        if is_new:
            delta = self.quantidade if self.tipo == self.ENTRADA else -self.quantidade
            Produto.objects.filter(pk=self.produto_id).update(
                quantidade=models.F("quantidade") + delta
            )
