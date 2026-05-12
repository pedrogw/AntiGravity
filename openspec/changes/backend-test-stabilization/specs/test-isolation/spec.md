## ADDED Requirements

### Requirement: Ambiente de Testes Independente de Serviços Externos
A suíte de testes do backend SHALL executar completamente sem conexão com PostgreSQL, Redis, ou qualquer serviço de infraestrutura externo. O ambiente de testes DEVE usar SQLite in-memory como banco de dados.

#### Scenario: Execução dos testes sem banco externo ativo
- **WHEN** o comando `pytest` é executado em uma máquina sem PostgreSQL em execução
- **THEN** todos os testes devem executar e completar (passando ou falhando por lógica, nunca por erro de conexão `socket.gaierror`)

#### Scenario: Proteção Global via Variáveis de Ambiente
- **WHEN** a sessão pytest é iniciada
- **THEN** a variável `DATABASE_URL` DEVE ser sobrescrita pelo conftest antes de qualquer módulo ser importado, prevenindo fugas de conexão

### Requirement: Schema e Isolamento Perfeito via Transaction Rollback
O ambiente de testes SHALL garantir isolamento absoluto de estado. As tabelas são criadas uma vez por sessão, mas cada teste recebe um ambiente limpo.

#### Scenario: Teardown Automático por Transação
- **WHEN** um teste específico insere ou modifica dados no banco
- **THEN** ao final do teste, essas modificações sofrem ROLLBACK, não impactando testes subsequentes

#### Scenario: Desempenho no Setup
- **WHEN** uma sessão com dezenas de testes é iniciada
- **THEN** o DDL (`Base.metadata.create_all`) é executado apenas uma vez, otimizando o tempo total de execução

### Requirement: Compatibilidade Universal dos Modelos ORM
Os modelos ORM SQLAlchemy MUST ser agnósticos de banco de dados, abandonando tipos exclusivos para garantir compilação em múltiplos dialetos.

#### Scenario: Remoção do Dialeto Exclusivo
- **WHEN** os modelos ORM (ex: `user.py`, `place.py`) definem UUIDs
- **THEN** eles DEVEM usar `sqlalchemy.types.UUID` em vez de `sqlalchemy.dialects.postgresql.UUID`

#### Scenario: Criação bem-sucedida das tabelas em SQLite
- **WHEN** `Base.metadata.create_all(sqlite_engine)` é chamado
- **THEN** todas as tabelas são criadas sem `OperationalError` ou `CompileError`
