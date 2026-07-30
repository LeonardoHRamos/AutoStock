# AutoStock

Sistema web para gestão de estoque desenvolvido com **Python** e **Django**, criado para controlar componentes utilizados em ambientes industriais.

O sistema centraliza o cadastro de produtos, registra movimentações de entrada e saída, calcula automaticamente o saldo de cada item e disponibiliza indicadores operacionais em um dashboard responsivo.

> Todo o repositório utiliza exclusivamente dados fictícios para fins de demonstração e portfólio.

---

# Funcionalidades

- Cadastro de produtos
- Cadastro de categorias
- Controle de entradas e saídas
- Atualização automática do estoque
- Dashboard com indicadores
- Produtos críticos
- Histórico completo de movimentações
- Autenticação integrada ao Django Admin
- Tema claro e escuro
- Carga idempotente de dados demonstrativos
- Documentação automática do modelo de dados

---

# Interface

> As imagens abaixo representam a interface atual da aplicação.

### Dashboard

![Dashboard](docs/images/dashboard.png)

### Catálogo de produtos

![Produtos](docs/images/catalogo.png)

### Auditoria de movimentações

![Movimentações](docs/images/movimentacoes.png)

---

# Arquitetura

O AutoStock foi desenvolvido utilizando uma arquitetura simples baseada no padrão MVC do Django.

Toda a regra de negócio permanece concentrada na aplicação `inventory`, enquanto o projeto `config` contém apenas configurações globais.

O princípio mais importante do sistema é:

> O estoque nunca é alterado manualmente.

O saldo dos produtos é calculado automaticamente a partir das movimentações registradas.

Cada entrada adiciona quantidade.

Cada saída reduz quantidade.

Isso mantém o histórico consistente e elimina divergências entre estoque e movimentações.

---

# Tecnologias

| Camada | Tecnologia |
|---------|------------|
| Backend | Python 3 |
| Framework | Django 6 |
| Banco de dados | SQLite |
| Frontend | Django Templates |
| Interface | Bootstrap 5 |
| Gráficos | Chart.js |
| Configuração | python-dotenv |

---

# Estrutura do projeto

```
AutoStock
│
├── config/
│
├── inventory/
│   ├── models.py
│   ├── views.py
│   ├── admin.py
│   ├── urls.py
│   ├── tests.py
│   └── management/
│
├── templates/
│
├── static/
│
├── docs/
│
├── manage.py
│
└── requirements.txt
```

---

# Modelo de Dados

O domínio principal é composto por três entidades.

```
Categoria
      │
      ▼
 Produto
      │
      ▼
Movimentação
```

Uma movimentação representa uma entrada ou saída de estoque.

O saldo do produto é atualizado automaticamente utilizando operações atômicas.

Categorias e produtos utilizados por movimentações não podem ser removidos, preservando a integridade do histórico.

A documentação completa do modelo é gerada automaticamente pelo comando:

```bash
python manage.py gerar_documentacao
```

---

# Instalação

Clone o projeto.

```bash
git clone https://github.com/LeonardoHRamos/AutoStock
```

Entre na pasta.

```bash
cd AutoStock
```

Crie um ambiente virtual.

Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Instale as dependências.

```bash
pip install -r requirements.txt
```

Crie o arquivo `.env`.

Windows

```powershell
Copy-Item .env.example .env
```

Linux

```bash
cp .env.example .env
```

Execute as migrações.

```bash
python manage.py migrate
```

Crie um administrador.

```bash
python manage.py createsuperuser
```

Execute o servidor.

```bash
python manage.py runserver
```

---

# Comandos úteis

Carregar dados demonstrativos.

```bash
python manage.py seed_inventario
```

Gerar documentação.

```bash
python manage.py gerar_documentacao
```

Executar testes.

```bash
python manage.py test
```

Verificar o projeto.

```bash
python manage.py check
```

---

# Testes

O projeto possui testes automatizados cobrindo principalmente:

- Atualização automática do estoque
- Entradas
- Saídas
- Integridade das movimentações
- Carga inicial de dados

---

# Segurança

- `.env` não é versionado.
- `db.sqlite3` permanece apenas localmente.
- O repositório utiliza somente dados fictícios.
- Configurações sensíveis são carregadas por variáveis de ambiente.

---

# Roadmap

- [ ] Impedir estoque negativo
- [ ] Movimentações imutáveis
- [ ] PostgreSQL
- [ ] Docker
- [ ] API REST
- [ ] Controle de permissões por perfil
- [ ] Histórico detalhado de auditoria
- [ ] Deploy em produção

---

# Autor

**Leonardo Henrique Ramos**

Software Engineer • Electrical Engineer

Python • Django • JavaScript • SQL • Industrial Automation

LinkedIn:

https://www.linkedin.com/in/leonardo-henrique-ramos-0821921a1/

GitHub:

https://github.com/LeonardoHRamos
