# AutoStock

Sistema web para **controle de estoque de peças de automação industrial** (SSDs,
cabos, scanners, sinaleiras, IHMs, baterias, carregadores, fontes). A equipe
registra entradas e saídas e o **saldo de cada item é calculado automaticamente** —
ninguém digita quantidade à mão. Um dashboard mostra os indicadores e alerta os
itens em nível crítico.

> Uso interno, acessado pelo navegador na rede local.

## Stack

- **Backend:** Python 3 · Django 6.0
- **Banco:** SQLite (desenvolvimento)
- **Frontend:** Templates Django · Bootstrap 5.3 · Chart.js 4 (via CDN)
- **Sem dependências além do Django** (ver `requirements.txt`).

## Estrutura do projeto

```
AutoStock/
├── config/              # projeto Django: settings, urls, wsgi/asgi
├── inventory/           # app principal (a regra de negócio vive aqui)
│   ├── models.py        # Category, Produto, Movimentacao (+ derivação do saldo)
│   ├── admin.py         # back-office (CRUD de tudo)
│   ├── views.py         # dashboard (indicadores e séries dos gráficos)
│   ├── urls.py          # rota do dashboard
│   ├── tests.py         # testes da regra de negócio
│   └── management/commands/
│       ├── seed_inventario.py      # carga inicial do inventário (idempotente)
│       └── gerar_documentacao.py   # gera docs/ a partir dos models
├── templates/           # base.html + inventory/dashboard.html
├── static/
│   ├── css/autostock.css           # tema claro/escuro
│   └── js/{theme.js,dashboard.js}  # toggle de tema + gráficos
├── docs/                # documentação gerada automaticamente
├── db.sqlite3
├── manage.py
└── iniciar_autostock.bat           # sobe o servidor para a equipe na rede
```

## Modelo de dados (resumo)

- **Category** → **Produto** → **Movimentacao** (entrada/saída).
- Relações com `on_delete=PROTECT`: não é possível apagar uma categoria/produto em uso.
- **O saldo é derivado:** `Movimentacao.save()` aplica `+qtd` (entrada) / `−qtd`
  (saída) na `quantidade` do produto, de forma atômica. Só a **criação** ajusta o
  saldo — edições não reajustam, mantendo o histórico consistente.

Detalhamento completo e sempre atualizado em [`docs/MODELO_DE_DADOS.md`](docs/MODELO_DE_DADOS.md)
(gerado a partir dos próprios models).

## Como rodar

```bash
# 1. Ativar o ambiente virtual (Windows)
.venv\Scripts\activate

# 2. Aplicar as migrations
python manage.py migrate

# 3. Subir o servidor de desenvolvimento
python manage.py runserver
```

Dashboard em `http://localhost:8000/` · Admin em `http://localhost:8000/admin/`.
O dashboard exige login (reaproveita o login do admin).

**Para a equipe (rede local):** dê duplo-clique em `iniciar_autostock.bat` e acesse
`http://IP_DO_PC:8000/`.

## Comandos de gestão

```bash
python manage.py seed_inventario       # carrega o inventário real (só uma vez; protege histórico)
python manage.py gerar_documentacao    # regenera docs/MODELO_DE_DADOS.md a partir dos models
```

## Testes

```bash
python manage.py test inventory.tests
```

Cobrem a derivação do saldo (entrada/saída/edição) e a trava anti-destruição da carga.

## Convenções

- **Uma funcionalidade por commit**, com mensagem descritiva (`feat(...)`, `fix(...)`).
- A `quantidade` do produto **nunca** é escrita à mão — sempre via movimentação.

## Roadmap / dívida técnica

- Validação de **estoque negativo** e movimentação imutável (sprint dedicada).
- Preparo para produção: PostgreSQL, `DEBUG=False`, `ALLOWED_HOSTS` restrito,
  servir por WSGI (gunicorn/IIS) e backups automáticos.
