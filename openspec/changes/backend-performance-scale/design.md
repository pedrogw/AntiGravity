## Context

Com a lógica de negócios isolada em eventos (Bloco 3), temos os gatilhos perfeitos para invalidação de cache e disparo de tarefas assíncronas. Leituras repetitivas geram I/O desnecessário no PostgreSQL. Ao mesmo tempo, "listeners" de eventos que fazem integrações pesadas não podem rodar na mesma thread do FastAPI. A introdução do Redis soluciona ambos: armazenamento chave-valor ultrarrápido para cache e broker para filas de background workers.

## Goals / Non-Goals

**Goals:**
- Implementar **Cache-Aside** para rotas de leitura utilizando `redis.asyncio`, com **serialização segura via Pydantic**.
- Configurar invalidação determinística de cache baseada em namespaces (ex: limpar todas as páginas de `deliveries:list:*` via SCAN) utilizando os Domain Events.
- Integrar a biblioteca `arq` para background workers e **compartilhar o contexto de banco de dados** entre a API e o Worker.

**Non-Goals:**
- Mover *toda* a leitura para o cache. Focaremos apenas nos Use Cases de listagem global ou dados que mudam raramente.
- Substituir o PostgreSQL por Redis para persistência real. O Redis será estritamente efêmero.

## Decisions

### Decisão 1: Abordagem de Cache e Serialização
**Escolha**: Implementar a lógica de cache via *Decorators* ou no Serviço. A conversão de Entidades para Redis será feita usando os Schemas Pydantic (`model_dump_json()` e `model_validate_json()`).
**Por quê**: Entidades puras ou modelos SQLAlchemy não são nativamente serializáveis para JSON. Pydantic garante *type safety* na ida e na volta do Redis.

### Decisão 2: Motor de Background Worker e Bootstrap Compartilhado
**Escolha**: Utilizar a biblioteca `arq`. Criaremos um `app/core/bootstrap.py` para instanciar a engine do SQLAlchemy e o pool do Redis de forma independente do ciclo de vida do FastAPI.
**Por quê**: O Worker roda em outro processo isolado. Se ele não inicializar seu próprio pool de banco, falhará ao tentar executar repositórios. Compartilhar a inicialização evita código duplicado.

### Decisão 3: Invalidação de Cache por Namespace
**Escolha**: Listagens (ex: `limit=50&offset=0`) usarão chaves padronizadas como `deliveries:list:50:0`. Quando uma entrega nova for criada, o listener executará um comando `SCAN` seguido de `DEL` para varrer e deletar todas as chaves que começam com `deliveries:list:`.
**Por quê**: Garante que nenhuma página fique obsoleta ("stale") após uma inserção.

## Risks / Trade-offs

| Risco | Mitigação |
|---|---|
| Inconsistência de Transação no Worker | Garantir que o Worker use blocos assíncronos de `Session` com commit/rollback explícitos, usando a mesma fábrica injetada no FastAPI. |
| Lentidão no `SCAN` do Redis | Para grandes datasets, o comando `SCAN` pode ser lento. Usar paginação no `SCAN` ou, futuramente, "Cache Versioning" (adicionar uma versão à chave global). Para a escala atual, `SCAN` iterativo é seguro. |

## Migration Plan
1. Atualizar o `docker-compose.yml` para incluir o serviço Redis e o serviço Worker.
2. Criar `bootstrap.py` e refatorar `main.py` para usá-lo no *lifespan*.
3. Implementar a conexão `redis.asyncio` e os serviços de serialização Pydantic.
4. Envolver endpoints de leitura (`ListDeliveriesUseCase`) no Cache-Aside e implementar a lógica `SCAN` para invalidação.
5. Configurar o Worker do `arq` consumindo o `bootstrap.py` e transferir logs de auditoria pesados para ele.
