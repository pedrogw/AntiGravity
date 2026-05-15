## Por quê

O backend do Antigravity possui uma arquitetura sólida (Clean Architecture) e observabilidade garantida. No entanto, à medida que o volume de entregas e consultas cresce, rotas de leitura pesadas (como listagem de entregas ou SLA) e tarefas secundárias começam a competir por recursos do banco de dados relacional e da thread do FastAPI. Precisamos elevar a infraestrutura para o próximo nível introduzindo Caching (Redis) para reduzir a latência de consultas frequentes e consolidar tarefas pesadas em Background Workers reais, garantindo a escalabilidade horizontal e performance (The "Next Level").

## O que Muda

- **Integração com Redis**: Adição do Redis como camada de cache na infraestrutura (`app/infrastructure/cache/`).
- **Caching de Leitura**: Implementação de cache para endpoints de alta leitura (ex: `GET /places`, `GET /deliveries` com paginação padrão), invalidando o cache via eventos de domínio recém-criados no Bloco 3.
- **Background Tasks Avançadas**: Estruturação de processamento em background (utilizando Celery/Arq ou aprimorando substancialmente o `BackgroundTasks` nativo do FastAPI com Redis) para processar os listeners de eventos (ex: logs de auditoria e webhook notifications) de forma totalmente não-bloqueante e escalável.

## Capacidades

### Novas Capacidades
- `distributed-caching-layer`: Sistema de cache distribuído via Redis para reduzir latência e carga no PostgreSQL.
- `async-worker-queue`: Fila de processamento de tarefas em background para garantir que ações pesadas disparadas por eventos não impactem o event loop da API.

### Capacidades Modificadas
- `internal-event-bus`: Modificado para despachar eventos não apenas para listeners in-memory, mas para a nova fila de background workers quando necessário.

## Impacto

| Área | Detalhe |
|---|---|
| Infraestrutura (`app/infrastructure`) | Novo pacote `cache` com client Redis (ex: `redis.asyncio`). |
| Repositórios e Use Cases de Leitura | Serão "envelopados" ou decorados com lógica de cache (`Cache-Aside pattern`). |
| Event Bus (`app/core/events/bus.py`) | Integração com o dispatcher do background worker (Arq/Celery). |
| Docker & CI | O ambiente precisará de um container Redis e potencialmente um novo serviço de Worker. |
