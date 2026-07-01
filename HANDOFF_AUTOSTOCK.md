# AutoStock — Handoff Técnico para Claude Code

> Documento de contexto de sessão. Leia por completo antes de qualquer ação.
> Auditoria de base realizada em 01/07/2026 — os estados marcados como
> "verificado" foram reproduzidos e confirmados executando o projeto.
> Sugestão de uso: colocar na raiz do repositório ou usar como base do `CLAUDE.md`.

---

## 1. O que é o projeto

Sistema **web** em Django para gestão de suprimentos de automação industrial,
usado pela equipe de analistas para controlar o estoque de peças de reposição
das linhas de produção. Acesso via navegador, sem instalação, base de dados
única compartilhada pela equipe.

Categorias de suprimentos previstas: IHMs, SSDs, scanners, fontes, cabos,
leitores e peças diversas. Fluxo do negócio: um item sai do estoque quando há
falha na linha e depois é reposto — hoje sem sistema dedicado, que é o que o
AutoStock resolve.

---

## 2. Stack (CONGELADA — não reestruturar)

- **Backend:** Python + Django `6.0.6`
- **Banco:** SQLite agora → PostgreSQL no futuro (migração NÃO é para agora)
- **Frontend:** Templates Django + Bootstrap + JavaScript + Charts.js
- **Dependências** (`requirements.txt`): `asgiref==3.11.1`, `Django==6.0.6`,
  `sqlparse==0.5.5`, `tzdata==2026.2`

Estrutura de pastas (definida e congelada):

```
AutoStock/
  config/        # settings, urls, wsgi, asgi
  inventory/     # app principal
  docs/
  media/
  static/
  templates/
  manage.py
  requirements.txt
  README.md  ROADMAP.md  CHANGELOG.md
  .gitignore  db.sqlite3
```

---

## 3. Princípios de trabalho (regras invioláveis)

1. **Desenvolver por funcionalidade, não por arquivo.** Uma feature é entregue
   inteira, ponta a ponta.
2. **A infraestrutura está congelada.** Não renomear apps, não mover pastas,
   não trocar settings estrutural, não reorganizar o projeto.
3. **Não antecipar arquitetura** "porque pode ser útil no futuro". Só se
   implementa o que a sprint atual exige.
4. **Cada funcionalidade completa termina com 1 commit.**
5. **Definition of Done de uma sprint:** `migrate` roda limpo **+** o recurso
   aparece/funciona no admin **+** há 1 commit descritivo.
6. **Stop gate:** ao chegar num ponto de decisão de arquitetura ou antes de
   iniciar a próxima milestone, **pare e peça aprovação** antes de prosseguir.

---

## 4. Estado atual verificado (auditoria 01/07/2026)

Base **íntegra**. Auditados e aprovados:

| Item | Estado |
|---|---|
| `config/settings.py` — `'inventory'` em `INSTALLED_APPS`, SQLite ok | OK |
| `inventory/apps.py` — `InventoryConfig`, `name = "inventory"` | OK |
| `inventory/models.py` — model `Category` bem definido | OK |
| `manage.py`, `config/urls.py`, `wsgi.py`, `asgi.py` | OK (padrão) |
| `python manage.py check` | `no issues` |

### Bug encontrado e sua causa raiz

`makemigrations` retornava **`No changes detected`** mesmo com o model correto.

**Causa:** a pasta `inventory/migrations/` existia **sem `__init__.py`**. Sem
esse arquivo, o Django trata a pasta como *namespace package* e considera o app
como "sem migrations", pulando-o silenciosamente. Não é erro no model.

Comprovação (reproduzido em ambiente limpo):

- `migrations/` sem `__init__.py` → `makemigrations` → `No changes detected`
- `migrations/__init__.py` presente → `makemigrations` → gera
  `0001_initial.py (Create model Category)` e `migrate` aplica com sucesso.

Observação: `makemigrations inventory` (nomeando o app) até funciona no Django 6,
mas `makemigrations` sem argumento ignora o app — foi o que deu a sensação de
comportamento intermitente.

---

## 5. AÇÃO IMEDIATA (primeira tarefa da sessão)

> Idempotente: verifique antes de aplicar. Se já estiver feito, apenas confirme.

**5.1 — Garantir o `__init__.py` das migrations**

```bash
# Windows (cmd)
type nul > inventory\migrations\__init__.py
```

Só criar se o arquivo não existir. Não sobrescrever nada.

**5.2 — Gerar e aplicar a migration da Category**

```bash
python manage.py makemigrations   # deve gerar inventory/0001_initial.py
python manage.py migrate          # deve aplicar inventory.0001_initial ... OK
```

**5.3 — Registrar `Category` no admin** (hoje `admin.py` só tem o import):

```python
from django.contrib import admin
from .models import Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at")
    search_fields = ("name",)
```

**5.4 — Validar e commitar**

```bash
python manage.py createsuperuser   # se ainda não houver
python manage.py runserver         # conferir /admin -> cadastrar 1 categoria
git add . && git commit -m "feat(inventory): cadastro de categorias (model, migration, admin)"
```

Isso fecha a **Milestone 1**. Após o commit, **pare e reporte** antes de iniciar Produtos.

---

## 6. Estado atual dos arquivos-chave

`inventory/models.py` (correto, não alterar sem motivo):

```python
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Nome")
    description = models.TextField(blank=True, verbose_name="Descrição")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
```

`inventory/apps.py`:

```python
from django.apps import AppConfig


class InventoryConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "inventory"
```

`inventory/admin.py` — **atual:** apenas `from django.contrib import admin`
(precisa do registro do passo 5.3).
`inventory/views.py`, `inventory/tests.py` — apenas boilerplate, ainda sem lógica.

---

## 7. Roadmap por funcionalidade (com Definition of Done)

Ordem fixa. Não iniciar uma milestone antes de fechar a anterior com commit.

**Milestone 1 — Categorias** *(desbloqueada; ver seção 5)*
DoD: model + migration aplicada + admin + cadastro/listagem funcionando + commit.

**Milestone 2 — Produtos**
Alvo (só implementar quando a sprint começar; não improvisar campos):
`Produto` com FK para `Category`, `quantidade` (int), `codigo_interno`
(unique), `descricao`. DoD igual ao da M1.

**Milestone 3 — Movimentações**
`Movimentacao` com tipo entrada/saída, FK para `Produto`, `usuario`
(FK `auth.User`), `data`, `observacao`. A quantidade disponível deriva daqui.
DoD igual.

**Milestone 4 — Dashboard**
Só após existir dado real de movimentação. Produtos críticos, mais utilizados,
quantidade por categoria, movimentações do mês, gráficos (Charts.js). DoD igual.

**Milestone 5 — Integração Obsidian**
Por último. Não desenhar antes da hora.

Itens explicitamente **fora de escopo por enquanto** (não implementar sem
aprovação): PostgreSQL, QR Code, SAP, GLPI, relatórios PDF/Excel/CSV,
fabricantes, localização física.

---

## 8. Comandos do ambiente

```bash
# ativar venv (Windows)
.venv\Scripts\activate

python manage.py runserver        # subir servidor de dev
python manage.py makemigrations   # gerar migrations
python manage.py migrate          # aplicar migrations
python manage.py check            # checagem do sistema
python manage.py test             # rodar testes
```

---

## 9. Resumo para o agente

A base está sã e congelada. A única pendência de infra é o `__init__.py` das
migrations (seção 5.1) — depois disso, **só desenvolvimento por funcionalidade**,
uma milestone de cada vez, cada uma terminando em commit, com stop gate entre elas.
