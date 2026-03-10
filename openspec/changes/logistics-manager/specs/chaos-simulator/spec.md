## ADDED Requirements

### Requirement: Catálogo de eventos de caos
O sistema SHALL suportar 4 tipos de eventos de caos pré-definidos: chuva (impact_factor=1.3), alagamento (delay=45min), engarrafamento (impact_factor=1.5, delay=15min), acidente (delay=60min). Cada evento MUST ter tipo, severidade, impact_factor e delay_minutes.

#### Scenario: Listar tipos de evento disponíveis
- **WHEN** operador faz GET em `/chaos/event-types`
- **THEN** o sistema retorna os 4 tipos com seus parâmetros padrão

### Requirement: Injeção de evento de caos
O sistema SHALL permitir ao operador injetar um evento de caos em uma entrega ativa. Ao injetar, o ETA MUST ser recalculado imediatamente.

#### Scenario: Injetar evento de chuva
- **WHEN** operador faz POST em `/chaos/events` com delivery_id e type="chuva"
- **THEN** o sistema cria o evento, recalcula ETA da entrega e retorna HTTP 201 com novo ETA

#### Scenario: Injetar evento em entrega não ativa
- **WHEN** operador tenta injetar caos em entrega com status "entregue"
- **THEN** o sistema retorna HTTP 422 "Só é possível injetar caos em entregas em trânsito"

### Requirement: Remoção de evento de caos
O sistema SHALL permitir ao operador remover um evento de caos ativo. Ao remover, o ETA MUST ser recalculado sem aquele evento.

#### Scenario: Remover evento de chuva
- **WHEN** operador faz DELETE em `/chaos/events/{event_id}`
- **THEN** o sistema remove o evento, recalcula ETA e retorna HTTP 200 com ETA atualizado

### Requirement: Visibilidade dos eventos para todos os roles
O sistema SHALL expor os eventos de caos ativos para lojistas e motoristas em suas entregas. Todos os roles MUST visualizar quais eventos estão impactando o ETA.

#### Scenario: Lojista visualiza eventos de caos em sua entrega
- **WHEN** lojista faz GET em `/deliveries/{id}`
- **THEN** a resposta inclui lista de eventos de caos ativos com tipo, impacto e hora de criação
