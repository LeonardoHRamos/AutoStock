from django.contrib import admin

from .models import Category, Movimentacao, Produto


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at")
    search_fields = ("name",)


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ("nome", "category", "codigo_interno", "quantidade")
    list_filter = ("category",)
    search_fields = ("nome", "codigo_interno", "descricao")
    list_select_related = ("category",)
    readonly_fields = ("quantidade",)  # saldo é derivado das movimentações


@admin.register(Movimentacao)
class MovimentacaoAdmin(admin.ModelAdmin):
    list_display = ("produto", "tipo", "quantidade", "usuario", "data")
    list_filter = ("tipo", "produto__category")
    search_fields = ("produto__nome", "observacao")
    list_select_related = ("produto", "produto__category", "usuario")
    autocomplete_fields = ("produto",)
    date_hierarchy = "data"
    readonly_fields = ("data",)
