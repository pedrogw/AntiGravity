## ADDED Requirements

### Requirement: Cache-Aside de Alta Velocidade
O sistema SHALL possuir uma camada de cache distribuída capaz de armazenar e recuperar respostas serializadas para reduzir consultas repetitivas ao banco de dados relacional.

#### Scenario: Leitura bem-sucedida do cache (Cache Hit)
- **WHEN** uma requisição de leitura (ex: listar lugares) solicita uma chave que está presente e não expirada no Redis
- **THEN** o sistema MUST retornar os dados serializados do cache em menos tempo que uma query SQL, sem invocar o Repositório do banco de dados.

#### Scenario: Inserção no cache (Cache Miss)
- **WHEN** a chave solicitada não existe no Redis
- **THEN** o sistema MUST buscar a informação no PostgreSQL, salvar o resultado no Redis com um TTL (Time To Live) configurado, e retornar os dados ao usuário.

### Requirement: Invalidação Determinística
O sistema SHALL assegurar que dados em cache não fiquem obsoletos permanentemente (stale), garantindo a invalidação quando mutações ocorrem.

#### Scenario: Invalidação via Eventos
- **WHEN** um evento de domínio indicando mutação (ex: `PlaceCreatedEvent`) é despachado pelo EventBus
- **THEN** o listener de cache MUST invalidar (deletar) as chaves de leitura correspondentes (ex: `places:all`), forçando um *Cache Miss* na próxima requisição.
