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