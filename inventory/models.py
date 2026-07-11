from django.conf import settings
from django.db import models


class Category(models.Model):
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

    def __str__(self):
        return self.name


class Produto(models.Model):
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

    def __str__(self):
        return self.nome


class Movimentacao(models.Model):
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

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.produto.codigo_interno} ({self.quantidade})"

    def save(self, *args, **kwargs):
        is_new = self._state.adding
        super().save(*args, **kwargs)
        if is_new:
            delta = self.quantidade if self.tipo == self.ENTRADA else -self.quantidade
            Produto.objects.filter(pk=self.produto_id).update(
                quantidade=models.F("quantidade") + delta
            )