## 1. Preparação e Sanitização de Modelos

- [x] 1.1 Adicionar `aiosqlite>=0.19.0` ao `backend/requirements.txt`
- [x] 1.2 Auditar os 5 modelos ORM em `app/infrastructure/orm/` removendo a importação de `postgresql.UUID`
- [x] 1.3 Substituir todas as instâncias nos modelos para `sqlalchemy.types.UUID(as_uuid=True)`

## 2. Bloqueio de Fugas de Ambiente

- [x] 2.1 Adicionar monkeypatch logo no início do `tests/conftest.py` para forçar `os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///:memory:"` *antes* do import da aplicação
- [x] 2.2 Confirmar que o `core.config.settings` lê o valor correto mockado em tempo de inicialização

## 3. Isolamento Perfeito (Transaction Rollback)

- [x] 3.1 Reescrever o motor no `conftest.py` usando `create_async_engine("sqlite+aiosqlite:///:memory:")`
- [x] 3.2 Criar um fixture `setup_db_schema` (scope="session") que roda `Base.metadata.create_all`
- [x] 3.3 Modificar o `override_get_db` para criar uma transação (`async with engine.begin() as conn`), bindar a sessão na conexão, e disparar `await session.rollback()` no bloco `finally`
- [x] 3.4 Injetar a dependência com `app.dependency_overrides[get_db] = override_get_db`

## 4. Correção de Fixtures com Erros

- [x] 4.1 Investigar os 3 `ERROR` em `test_validation.py` (problema no payload ou dependências da rota testada)
- [x] 4.2 Corrigir os testes no arquivo para evitar falsos negativos relacionados ao banco in-memory

## 5. Alinhamento de Contratos ORM → Entidade

- [x] 5.1 Auditar os Use Cases em `app/use_cases/` para garantir que métodos retornam Entidades puras e não modelos ORM 
- [x] 5.2 Se necessário, mapear explicitamente a saída dos Use Cases antes de retornar

## 6. Validação Final

- [x] 6.1 Rodar `pytest -v` repetidas vezes (e em paralelo se aplicável) para confirmar que nenhum teste interfere no outro
- [x] 6.2 Validar se a suíte crava em 58/58 passing, sem avisos de vazamento de resource assíncrono (ResourceWarnings)
