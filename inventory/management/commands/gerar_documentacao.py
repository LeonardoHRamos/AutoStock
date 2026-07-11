"""Gera a documentação do modelo de dados a partir dos próprios models.

Fonte única da verdade: os models. Rode após qualquer mudança de schema:

    python manage.py gerar_documentacao

Saída: docs/MODELO_DE_DADOS.md (não editar à mão — é sobrescrito).
"""

from pathlib import Path

from django.apps import apps
from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone

APP_LABEL = "inventory"
SAIDA = Path(settings.BASE_DIR) / "docs" / "MODELO_DE_DADOS.md"


def _atributos(field):
    """Lista curta de restrições relevantes de um campo."""
    partes = []
    if field.primary_key:
        partes.append("PK")
    if field.unique and not field.primary_key:
        partes.append("único")
    if field.null:
        partes.append("aceita nulo")
    if getattr(field, "blank", False):
        partes.append("opcional no formulário")
    if field.has_default() and field.get_default() not in (None, ""):
        partes.append(f"padrão={field.get_default()!r}")
    if field.choices:
        opcoes = ", ".join(str(rotulo) for _, rotulo in field.choices)
        partes.append(f"opções: {opcoes}")
    return "; ".join(partes) or "—"


def _tipo(field):
    tipo = field.get_internal_type()
    if field.is_relation and field.related_model is not None:
        alvo = field.related_model._meta.verbose_name
        on_delete = getattr(field.remote_field, "on_delete", None)
        regra = f", on_delete={on_delete.__name__}" if on_delete else ""
        return f"{tipo} → {alvo}{regra}"
    return tipo


class Command(BaseCommand):
    help = "Gera docs/MODELO_DE_DADOS.md a partir dos models do app inventory."

    def handle(self, *args, **options):
        config = apps.get_app_config(APP_LABEL)

        linhas = [
            "# Modelo de dados — AutoStock",
            "",
            "> **Documento gerado automaticamente** por "
            "`python manage.py gerar_documentacao`. Não editar à mão.",
            f"> Gerado em {timezone.localtime():%d/%m/%Y %H:%M}.",
            "",
        ]

        for model in sorted(config.get_models(), key=lambda m: m._meta.verbose_name):
            meta = model._meta
            linhas.append(f"## {meta.verbose_name_plural.title()} (`{model.__name__}`)")
            linhas.append("")
            doc = (model.__doc__ or "").strip()
            if doc:
                linhas.append(doc)
                linhas.append("")
            linhas.append("| Campo | Rótulo | Tipo | Restrições |")
            linhas.append("|-------|--------|------|------------|")
            for field in meta.get_fields():
                if field.auto_created and not field.concrete:
                    continue  # ignora relações reversas
                rotulo = getattr(field, "verbose_name", field.name)
                linhas.append(
                    f"| `{field.name}` | {rotulo} | {_tipo(field)} | {_atributos(field)} |"
                )
            linhas.append("")

        SAIDA.parent.mkdir(parents=True, exist_ok=True)
        SAIDA.write_text("\n".join(linhas), encoding="utf-8")

        self.stdout.write(self.style.SUCCESS(
            f"Documentação gerada em {SAIDA.relative_to(settings.BASE_DIR)}."
        ))
