## 1. Setup Compartilhado (Infra e Bootstrap)

- [ ] 1.1 Adicionar dependências `redis` e `arq` no `requirements.txt`
- [ ] 1.2 Atualizar `docker-compose.yml` para incluir `redis:alpine` e o serviço do `worker` rodando `arq`
- [ ] 1.3 Criar `app/core/bootstrap.py` extraindo a lógica de criação da Engine/SessionMaker do DB para ser reutilizável
- [ ] 1.4 Refatorar `app/main.py` para usar o `bootstrap.py` em seu evento de lifespan

## 2. Camada de Cache Segura (Serialização)

- [ ] 2.1 Criar módulo genérico de cache `app/infrastructure/cache/redis_client.py`
- [ ] 2.2 Implementar `CacheService` com suporte explícito aos Schemas do Pydantic (`model_dump_json()` / `model_validate_json()`) para serializar e desserializar respostas do banco
- [ ] 2.3 Garantir que o ambiente de testes unitários use `fakeredis` injetado via `conftest.py`

## 3. Worker Assíncrono (`arq`)

- [ ] 3.1 Criar `worker.py` importando `bootstrap.py` (para que o worker tenha seu próprio pool do PostgreSQL) e configurando a conexão Redis
- [ ] 3.2 Criar um job assíncrono real de teste (ex: simular notificação por email ou escrever log de auditoria longo)

## 4. Orquestração de Performance (Namespacing)

- [ ] 4.1 Modificar o Use Case `ListDeliveriesUseCase` para implementar o Cache-Aside utilizando um namespace padronizado como `deliveries:list:{limit}:{offset}`
- [ ] 4.2 Alterar o listener associado ao `DeliveryCreatedEvent` para despachar uma tarefa no Worker `arq` (em vez de rodar local)
- [ ] 4.3 Implementar função de **Invalidação Dinâmica**: Um listener local que execute comandos `SCAN` e `DEL` no Redis para limpar todas as chaves iniciadas em `deliveries:list:` quando uma nova entrega for criada

## 5. Validação Full Stack

- [ ] 5.1 Subir API, Postgres, Redis e Worker via `docker-compose up` e checar logs de health
- [ ] 5.2 Realizar uma bateria de requisições GET com paginações diferentes (`GET /deliveries`) e confirmar via logs que dados foram serializados pelo Pydantic para o Redis
- [ ] 5.3 Criar uma nova entrega (`POST`) e confirmar que o cache anterior foi explodido pelo listener de Invalidação Dinâmica e o Job assíncrono rodou silenciosamente no Worker
