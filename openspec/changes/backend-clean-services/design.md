## Context

À medida que as regras de negócio de logística (como cálculo de rotas e predição de ETA) evoluem, colocá-las diretamente dentro dos Use Cases causa inchaço ("Fat Use Cases"). Além disso, quando ações secundárias devem ocorrer após o sucesso de uma entrega (ex: gravar log de auditoria), o Use Case fica acoplado a múltiplas dependências. Precisamos de serviços de domínio puros para encapsular lógica complexa e um barramento de eventos in-memory para reatividade, mantendo a integridade transacional.

## Goals / Non-Goals

**Goals:**
- Isolar a lógica pura (matemática/algorítmica) de cálculo de ETA em *Domain Services* (`app/domain/services/eta_service.py`), garantindo que o serviço receba apenas dados brutos (coordenadas) e não tenha acesso a repositórios.
- Implementar um mecanismo in-memory de Pub/Sub (`EventBus`) para disparar eventos de domínio *após* a persistência bem-sucedida.
- Suportar handlers assíncronos no EventBus, permitindo integração com `BackgroundTasks` do FastAPI para listeners pesados.
- Refatorar os Use Cases de entrega para orquestrar: buscar as coordenadas via repositórios de `Place`, calcular o ETA no serviço puro, persistir a entrega e só então disparar o evento.

**Non-Goals:**
- Integrar Message Brokers reais (Kafka, RabbitMQ, SQS) neste momento.
- Mudar a lógica fundamental do banco de dados; o foco é estruturação de memória e arquitetura.

## Decisions

### Decisão 1: Abordagem para Eventos In-Memory (Post-Persistence)
**Escolha**: Implementar um `EventBus` padrão *Observer* com suporte a handlers `async`. O disparo de eventos pelo Use Case será estritamente **após** o retorno de sucesso do repositório (`await repo.create()`).
**Por quê**: Disparar antes do commit pode gerar "ações fantasmas" se o banco falhar. Suportar `async` permite que listeners demorados usem `BackgroundTasks` sem travar a requisição principal.

### Decisão 2: Domain Services como Funções Puras (Pureza Arquitetural)
**Escolha**: O serviço de ETA (`calculate_eta`) receberá coordenadas (`lat`, `lng` da Factory e Store) em vez de receber IDs e buscá-las no banco. O `CreateDeliveryUseCase` fará a orquestração buscando as entidades através do `PlaceRepository`.
**Por quê**: O serviço de domínio permanece puramente funcional e 100% testável independentemente de I/O de banco de dados.

## Risks / Trade-offs

| Risco | Mitigação |
|---|---|
| Inchaço no Use Case com múltiplos Repositórios | O Use Case de criação de entrega precisará do `DeliveryRepository` e do `PlaceRepository`. Caso se torne muito complexo no futuro, poderemos introduzir o padrão *Unit of Work*. No momento, a injeção simples é suficiente. |
| Perda de eventos se a aplicação reiniciar logo após o commit | Para este bloco, como os eventos são para ações não-críticas imediatas (logs, notificações de interface), o risco é aceito. Ações críticas persistidas na transação do banco são seguras. |

## Migration Plan
1. Criar o barramento de eventos (`EventBus`) assíncrono e a classe base `DomainEvent`.
2. Criar o `eta_service` como uma função/classe de cálculo puro.
3. Modificar as rotas e injetores para prover o `PlaceRepository` e `BackgroundTasks` ao `CreateDeliveryUseCase`.
4. Refatorar o `CreateDeliveryUseCase`: buscar coordenadas -> calcular ETA -> salvar no BD -> disparar evento.
