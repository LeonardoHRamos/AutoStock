from django.contrib import admin
from .models import Category, Produto


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at")
    search_fields = ("name",)


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ("codigo_interno", "category", "quantidade")
    list_filter = ("category",)
    search_fields = ("codigo_interno", "descricao")
