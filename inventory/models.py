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

    codigo_interno = models.CharField(
        max_length=50,
        unique=True,
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
        return f"{self.codigo_interno} - {self.category.name}"