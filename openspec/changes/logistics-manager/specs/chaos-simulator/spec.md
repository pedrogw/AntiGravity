## ADDED Requirements

### Requirement: Catálogo de eventos de caos
O sistema SHALL suportar 4 tipos de eventos de caos pré-definidos: chuva (impact_factor=1.3), alagamento (delay=45min), engarrafamento (impact_factor=1.5, delay=15min), acidente (delay=60min). Cada evento MUST ter tipo, severidade, impact_factor e delay_minutes. Eventos NÃO alteram a rota — apenas o tempo estimado.

#### Scenario: Listar tipos de evento disponíveis
- **WHEN** operador faz GET em `/chaos/event-types`
- **THEN** o sistema retorna os 4 tipos com seus parâmetros padrão

### Requirement: Injeção de evento de caos
O sistema SHALL permitir ao operador injetar um evento de caos em uma entrega ativa. Ao injetar, o ETA MUST ser recalculado imediatamente e a mudança registrada em eta_history.

#### Scenario: Injetar evento de chuva
- **WHEN** operador faz POST em `/chaos/events` com delivery_id e type="chuva"
- **THEN** o sistema cria o evento, recalcula ETA, registra em eta_history e retorna HTTP 201 com novo ETA

#### Scenario: Injetar evento em entrega não ativa
- **WHEN** operador tenta injetar caos em entrega com status "entregue"
- **THEN** o sistema retorna HTTP 422 "Só é possível injetar caos em entregas em trânsito"

### Requirement: Remoção de evento de caos
O sistema SHALL permitir ao operador remover um evento de caos ativo. Ao remover, o ETA MUST ser recalculado sem aquele evento e a mudança registrada em eta_history.

#### Scenario: Remover evento de chuva
- **WHEN** operador faz DELETE em `/chaos/events/{event_id}`
- **THEN** o sistema remove o evento, recalcula ETA, registra em eta_history e retorna HTTP 200 com ETA atualizado

### Requirement: Visibilidade dos eventos para todos os roles
O sistema SHALL expor os eventos de caos ativos para lojistas e motoristas em suas entregas. Todos os roles MUST visualizar quais eventos estão impactando o ETA.

#### Scenario: Lojista visualiza eventos de caos em sua entrega
- **WHEN** lojista faz GET em `/deliveries/{id}`
- **THEN** a resposta inclui lista de eventos de caos ativos com tipo, impacto e hora de criação (UTC)

### Requirement: Log permanente de eventos de caos para ML
O sistema SHALL manter um log permanente (chaos_event_log) de todos os eventos de caos com contexto geográfico. Registros MUST nunca ser deletados. Cada registro MUST conter: delivery_id, event_type, impact_factor, delay_minutes, coordenadas do trecho afetado (lat/lng início e fim), timestamp_start e timestamp_end.

#### Scenario: Evento injetado é registrado no log de ML
- **WHEN** um evento de chuva é injetado em uma entrega
- **THEN** o sistema cria registro em chaos_event_log com todos os campos preenchidos, independente do chaos_events principal

#### Scenario: Evento removido atualiza timestamp_end no log
- **WHEN** operador remove um evento de caos
- **THEN** o sistema atualiza timestamp_end no chaos_event_log (mas NÃO deleta o registro)

#### Scenario: Consultar log de caos para análise
- **WHEN** operador faz GET em `/chaos/log?limit=50&offset=0`
- **THEN** o sistema retorna registros paginados do log permanente, com filtros opcionais por tipo e período
