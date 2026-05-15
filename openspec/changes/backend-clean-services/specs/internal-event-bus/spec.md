## ADDED Requirements

### Requirement: Desacoplamento via Eventos In-Memory (Assíncronos)
O sistema SHALL implementar um padrão de Pub/Sub interno para permitir que múltiplas partes do sistema reajam a mudanças de estado sem exigir chamadas de função diretas e acoplamento duro nos Casos de Uso. O barramento MUST suportar listeners assíncronos.

#### Scenario: Disparo de evento de negócio após persistência
- **WHEN** uma entidade principal é persistida com sucesso no banco de dados (ex: `await repo.create()` não levanta exceções)
- **THEN** o Caso de Uso responsável MUST publicar o evento correspondente (ex: `DeliveryCreatedEvent`) no barramento interno, garantindo que o evento só existe se a mutação for consolidada.

#### Scenario: Reação a eventos sem bloqueio de I/O
- **WHEN** um evento é publicado no barramento interno
- **THEN** o barramento MUST notificar os listeners de forma assíncrona, permitindo que processos lentos (ex: logs via API) sejam despachados para background tasks sem degradar o tempo de resposta da requisição original.
