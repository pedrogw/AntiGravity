## Por quê

A suíte de testes do backend (`pytest`) está falhando em 11 dos 58 testes com erros de `socket.gaierror` — o que indica que os testes de integração tentam estabelecer uma conexão real com um banco de dados PostgreSQL externo. Em ambiente de CI/CD ou na máquina local sem Docker ativo, isso causa falha total, impossibilitando validar qualquer mudança no código com segurança.
Além disso, foi identificada uma falha crítica na compatibilidade do ORM (uso de `postgresql.UUID`) que quebra qualquer banco que não seja Postgres, e uma vulnerabilidade de vazamento de estado (test pollution) se os testes rodarem de forma paralela ou concorrente na mesma sessão SQLite.

## O que Muda

- **Ambiente de testes migrado para SQLite in-memory**: O `conftest.py` será reescrito para usar um banco leve e local, eliminando a dependência de PostgreSQL em testes.
- **Isolamento via Transaction Rollback**: O banco será criado uma única vez por sessão, mas cada teste rodará dentro de uma transação que sofrerá `rollback` garantido ao final. Isso elimina qualquer "test pollution".
- **Monkeypatch de Variáveis de Ambiente**: A variável `DATABASE_URL` será sobrescrita antes do start do app para evitar "fugas" de conexões em scripts ou background tasks.
- **Refatoração de Modelos ORM (BREAKING INTERNAL)**: Todos os modelos ORM deixarão de usar `sqlalchemy.dialects.postgresql.UUID` e passarão a usar o agnóstico `sqlalchemy.types.UUID`.
- **Fixtures de repositório mocadas (testes unitários)**: Os testes unitários de Use Cases passarão a usar repositórios falsos injetáveis, sem nenhuma camada de banco.

## Capacidades

### Novas Capacidades
- `test-isolation`: Ambiente de testes completamente isolado, determinístico e livre de vazamento de estado, sem dependência de serviços externos.

### Capacidades Modificadas
*(Nenhuma mudança de requisito de negócio — apenas infraestrutura interna de testes e sintaxe ORM)*

## Impacto

| Área | Detalhe |
|---|---|
| `backend/app/infrastructure/orm/*.py` | Remoção de `postgresql.UUID` e substituição por `sqlalchemy.UUID` em todos os modelos |
| `backend/tests/conftest.py` | Reescrita completa do motor de banco (SQLite assíncrono), monkeypatch de ENV, e implementação de rollback por teste |
| `backend/tests/api/*.py` | Ajuste nos testes que usam fixtures com banco real |
| Banco de dados PostgreSQL | **NÃO impactado** — banco de produção intocado |
| Contratos de API (rotas, schemas) | **NÃO impactados** |
| Frontend | **NÃO impactado** |
