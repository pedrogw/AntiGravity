## Contexto

O backend foi refatorado para Clean Architecture com camadas bem definidas. A mudança foi bem-sucedida estruturalmente, mas a análise do ambiente de testes revelou 3 falhas críticas e 1 vulnerabilidade de isolamento:
1. **Falha de Dialeto**: Todos os modelos ORM usam `postgresql.UUID`, o que impossibilita a criação do schema em SQLite, causando `OperationalError`.
2. **Poluição de Dados**: Testes rodando em SQLite in-memory compartilham a mesma conexão. Criar o schema por "sessão" sem isolar os dados faz os testes interferirem uns nos outros (ex: testar cadastro de um mesmo email duas vezes falharia a segunda).
3. **Fuga de Ambiente**: Background tasks ou scripts podem usar `settings.DATABASE_URL` ignorando o `dependency_override`, tentando bater no Postgres real (causando `socket.gaierror`).

## Objetivos / Não-Objetivos

**Objetivos:**
- Fazer a suíte completa passar em qualquer máquina, totalmente offline de serviços externos.
- Migrar os modelos ORM para serem agnósticos (SQLAlchemy UUID vs PostgreSQL UUID).
- Criar isolamento absoluto entre testes (Transaction Rollback).
- Garantir que NENHUMA conexão saia do ambiente simulado via Monkeypatching de variáveis de ambiente.

**Não-Objetivos:**
- Alterar regras de negócio ou contratos de resposta da API.
- Migrar o banco de produção.

## Decisões

### Decisão 1: `sqlalchemy.types.UUID` em vez de `postgresql.UUID`
**Escolha**: Remover todos os imports específicos do Postgres nos modelos ORM.
**Por quê**: Permite que o SQLAlchemy gere o DDL correto para o banco alvo (`CHAR(32)` no SQLite, `UUID` no Postgres), garantindo portabilidade entre ambientes de teste e produção.

### Decisão 2: Transaction Rollback para Isolamento de Estado
**Escolha**: O `conftest.py` criará o schema uma vez no setup da sessão, mas o fixture `get_db` (ou similar) abrirá uma transação e forçará um `rollback` ao final de cada teste.
**Por quê**: Garante que o banco comece limpo a cada teste sem o custo extremo de recriar as tabelas (DDL) 58 vezes.
**Alternativas consideradas**: *Recriar schema por teste* (Lento demais). *Usar UUIDs únicos nos testes* (Não previne vazamento de estado global).

### Decisão 3: Monkeypatch Global de Configurações
**Escolha**: O `conftest.py` deve modificar `os.environ["DATABASE_URL"]` *antes* de iniciar a aplicação.
**Por quê**: Mata qualquer "fuga" do ambiente de testes onde componentes que não usam o `Depends(get_db)` tentariam bater no banco real.

## Riscos / Trade-offs

| Risco | Mitigação |
|---|---|
| SQLAlchemy UUID mudar comportamento em queries cruas no Postgres | Focar no uso do ORM; `sqlalchemy.UUID(as_uuid=True)` é traduzido perfeitamente no psycopg2/asyncpg |
| Async SQLAlchemy Rollback causar Deadlocks | Usar `NestedTransaction` (savepoints) ou garantir que a sessão seja fechada rigorosamente no `finally` da fixture |
| Falhas de compilação em DateTime com Timezone | Manter a tipagem, SQLite abstrai strings no fundo. Evitar comparações complexas de Timezone nativas do Postgres |

## Plano de Migração

1. Alterar os 5 modelos ORM para usar UUID agnóstico.
2. Escrever o novo `conftest.py` (aiosqlite + transações per-test).
3. Ajustar variáveis de ambiente locais no conftest.
4. Validar os `ERROR` em `test_validation.py`.
5. Executar `pytest` e garantir 58/58 sem fuga de dados.
