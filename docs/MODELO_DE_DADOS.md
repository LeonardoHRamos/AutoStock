# Modelo de dados — AutoStock

> **Documento gerado automaticamente** por `python manage.py gerar_documentacao`. Não editar à mão.
> Gerado em 11/07/2026 09:20.

## Categorias (`Category`)

Agrupa os produtos por tipo (SSDs, Cabos, Scanners, ...).

| Campo | Rótulo | Tipo | Restrições |
|-------|--------|------|------------|
| `id` | ID | BigAutoField | PK; opcional no formulário |
| `name` | Nome | CharField | único |
| `description` | Descrição | TextField | opcional no formulário |
| `created_at` | created at | DateTimeField | opcional no formulário |

## Movimentações (`Movimentacao`)

Entrada ou saída de um produto no estoque.

É a fonte da verdade do saldo: ao ser criada, ajusta a ``quantidade`` do
produto correspondente. Edições posteriores NÃO reajustam o saldo (só a
criação conta), mantendo o histórico imutável na prática.

| Campo | Rótulo | Tipo | Restrições |
|-------|--------|------|------------|
| `id` | ID | BigAutoField | PK; opcional no formulário |
| `produto` | Produto | ForeignKey → Produto, on_delete=PROTECT | — |
| `tipo` | Tipo | CharField | opções: Entrada, Saída |
| `quantidade` | Quantidade | PositiveIntegerField | — |
| `usuario` | Usuário | ForeignKey → usuário, on_delete=PROTECT | — |
| `data` | Data | DateTimeField | opcional no formulário |
| `observacao` | Observação | TextField | opcional no formulário |

## Produtos (`Produto`)

Item de estoque.

A ``quantidade`` é um valor DERIVADO: nunca é editada à mão, e sim
recalculada a cada ``Movimentacao`` (ver ``Movimentacao.save``). Por isso
ela é somente-leitura no admin.

| Campo | Rótulo | Tipo | Restrições |
|-------|--------|------|------------|
| `id` | ID | BigAutoField | PK; opcional no formulário |
| `category` | Categoria | ForeignKey → Categoria, on_delete=PROTECT | — |
| `nome` | Nome | CharField | — |
| `codigo_interno` | Código interno | CharField | único; aceita nulo; opcional no formulário |
| `descricao` | Descrição | TextField | opcional no formulário |
| `quantidade` | Quantidade | IntegerField | padrão=0 |
