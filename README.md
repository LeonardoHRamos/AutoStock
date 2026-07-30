# AutoStock

O AutoStock é um projeto demonstrativo de gestão de estoque de peças de automação industrial. A aplicação registra entradas e saídas, calcula automaticamente o saldo de cada item e apresenta indicadores e alertas de nível crítico em um dashboard.

O repositório deve ser utilizado com dados demonstrativos. Antes de publicar ou compartilhar uma instalação, confira se bancos locais, arquivos de ambiente e cargas de dados não contêm informações sensíveis.

## Stack

- **Backend:** Python 3 · Django 6.0
- **Banco:** SQLite (desenvolvimento)
- **Frontend:** Templates Django · Bootstrap 5.3 · Chart.js 4 (via CDN)
- **Configuração de ambiente:** python-dotenv

## Estrutura do projeto

```text
AutoStock/
├── config/              # projeto Django: settings, urls, wsgi/asgi
├── inventory/           # app principal (a regra de negócio vive aqui)
│   ├── models.py        # Category, Produto, Movimentacao e derivação do saldo
│   ├── admin.py         # back-office (CRUD)
│   ├── views.py         # dashboard (indicadores e séries dos gráficos)
│   ├── urls.py          # rota do dashboard
│   ├── tests.py         # testes da regra de negócio
│   └── management/commands/
│       ├── seed_inventario.py      # carga inicial de dados
│       └── gerar_documentacao.py   # gera docs/ a partir dos models
├── templates/           # base.html e inventory/dashboard.html
├── static/
│   ├── css/autostock.css           # tema claro/escuro
│   └── js/                         # tema e gráficos
├── docs/                # documentação gerada automaticamente
├── .env.example         # exemplo de configuração local
├── manage.py
└── requirements.txt
```

O arquivo `db.sqlite3` é local e não faz parte da árvore versionada.

## Modelo de dados (resumo)

- **Category** → **Produto** → **Movimentacao** (entrada/saída).
- Relações com `on_delete=PROTECT` impedem a exclusão de categorias e produtos em uso.
- O saldo é derivado: `Movimentacao.save()` aplica a quantidade como entrada ou saída no produto de forma atômica. Somente a criação da movimentação ajusta o saldo; edições não fazem um novo ajuste.

O detalhamento está em [`docs/MODELO_DE_DADOS.md`](docs/MODELO_DE_DADOS.md), gerado a partir dos models.

## Como executar

Crie e ative um ambiente virtual:

```bash
# Windows (PowerShell)
python -m venv .venv
.venv\Scripts\Activate.ps1

# Linux/macOS
python3 -m venv .venv
source .venv/bin/activate
```

Instale as dependências:

```bash
python -m pip install -r requirements.txt
```

Crie o arquivo local de configuração a partir do exemplo:

```bash
# Windows (PowerShell)
Copy-Item .env.example .env

# Linux/macOS
cp .env.example .env
```

Substitua `DJANGO_SECRET_KEY` no `.env` por uma chave aleatória segura. Para uma implantação pública, use também `DJANGO_DEBUG=False` e informe os hosts permitidos em `DJANGO_ALLOWED_HOSTS`, separados por vírgulas.

Prepare e execute a aplicação:

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

O dashboard fica em `http://localhost:8000/` e o admin em `http://localhost:8000/admin/`. O dashboard exige autenticação.

## Comandos de gestão

```bash
python manage.py seed_inventario       # carrega dados iniciais
python manage.py gerar_documentacao    # regenera a documentação dos models
```

Use apenas dados demonstrativos. O comando `seed_inventario` ainda precisa ser anonimizado antes da publicação pública.

## Testes

```bash
python manage.py check
python manage.py test inventory.tests
python manage.py makemigrations --check --dry-run
```

Os testes existentes cobrem a derivação do saldo em entradas, saídas e edições, além do comportamento da carga inicial.

## Convenções

- Uma funcionalidade por commit, com mensagem descritiva (`feat(...)`, `fix(...)`).
- A quantidade do produto é atualizada por movimentações.
- Segredos e configurações locais devem permanecer no `.env`, que não é versionado.

## Roadmap / dívida técnica

- Implementar validação para impedir estoque negativo.
- Tornar movimentações imutáveis.
- Preparar a implantação em produção com PostgreSQL, `DEBUG=False`, hosts restritos, servidor WSGI e backups automatizados.
