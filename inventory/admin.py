from django.contrib import admin
from .models import Category, Movimentacao, Produto


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at")
    search_fields = ("name",)


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ("codigo_interno", "category", "quantidade")
    list_filter = ("category",)
    search_fields = ("codigo_interno", "descricao")
    readonly_fields = ("quantidade",)


@admin.register(Movimentacao)
class MovimentacaoAdmin(admin.ModelAdmin):
    list_display = ("produto", "tipo", "quantidade", "usuario", "data")
    list_filter = ("tipo", "produto__category")
    search_fields = ("produto__codigo_interno", "observacao")
    autocomplete_fields = ("produto",)
