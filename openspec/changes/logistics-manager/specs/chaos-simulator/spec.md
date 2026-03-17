## ADDED Requirements

### Requirement: Catálogo de eventos de caos
O sistema SHALL suportar 4 tipos de eventos de caos pré-definidos: chuva (impact_factor=1.3), alagamento (delay=45min), engarrafamento (impact_factor=1.5, delay=15min), acidente (delay=60min). Cada evento MUST ter tipo, severidade, impact_factor e delay_minutes. Eventos NÃO alteram a rota — apenas o tempo estimado.

#### Scenario: Listar tipos de evento disponíveis
- **GIVEN** que o catálogo de eventos de caos possui 4 eventos pré-cadastrados (chuva, alagamento, engarrafamento, acidente)
- **WHEN** o operador faz GET em `/chaos/event-types`
- **THEN** o sistema retorna os 4 tipos exatos com seus parâmetros técnicos padrões (impact_factor e delay_minutes)

### Requirement: Injeção de evento de caos
O sistema SHALL permitir ao operador injetar um evento de caos em uma entrega ativa. Ao injetar, o ETA MUST ser recalculado imediatamente e a mudança registrada em eta_history.

#### Scenario: Injetar evento de chuva
- **GIVEN** uma entrega com o status "em_transito"
- **WHEN** o operador faz POST em `/chaos/events` fornecendo o `delivery_id` e type="chuva"
- **THEN** o sistema cria ativamente o evento, recalcula o ETA restante aplicando fator 1.3, registra em eta_history e retorna HTTP 201 com o novo ETA

#### Scenario: Injetar evento em entrega não ativa
- **GIVEN** uma entrega que já foi finalizada com o status "entregue"
- **WHEN** o operador tenta injetar qualquer cenário de caos nesta entrega
- **THEN** o sistema bloqueia a ação e retorna HTTP 422 "Só é possível injetar caos em entregas em trânsito"

### Requirement: Remoção de evento de caos
O sistema SHALL permitir ao operador remover um evento de caos ativo. Ao remover, o ETA MUST ser recalculado sem aquele evento e a mudança registrada em eta_history.

#### Scenario: Remover evento de chuva
- **GIVEN** que existe um evento de caos do tipo "chuva" atrelado e afetando o ETA de uma entrega
- **WHEN** o operador faz DELETE em `/chaos/events/{event_id}`
- **THEN** o sistema cessa a influência do evento, reverte o impacto de 1.3 no ETA restante, cria um marco em eta_history apontando a melhoria e retorna HTTP 200

### Requirement: Visibilidade dos eventos para todos os roles
O sistema SHALL expor os eventos de caos ativos para lojistas e motoristas em suas entregas. Todos os roles MUST visualizar quais eventos estão impactando o ETA.

#### Scenario: Lojista visualiza eventos de caos em sua entrega
- **GIVEN** que um ou mais eventos de caos foram injetados na carga destinada ao lojista
- **WHEN** o lojista autenticado faz GET em `/deliveries/{id}`
- **THEN** o objeto de resposta inclui obrigatoriamente um array com os detalhes públicos do caos (tipo, impacto temporário e hora de criação UTC)

### Requirement: Log permanente de eventos de caos para ML
O sistema SHALL manter um log permanente (chaos_event_log) de todos os eventos de caos com contexto geográfico. Registros MUST nunca ser deletados. Cada registro MUST conter: delivery_id, event_type, impact_factor, delay_minutes, coordenadas do trecho afetado (lat/lng início e fim), timestamp_start e timestamp_end.

#### Scenario: Evento injetado é registrado no log de ML
- **GIVEN** a injeção bem-sucedida de um evento de "chuva"
- **WHEN** a transação de banco de dados do evento de caos for finalizada
- **THEN** o sistema espelha (append-only) a criação no `chaos_event_log` gravando contexto, `timestamp_start` e impacto

#### Scenario: Evento removido atualiza timestamp_end no log
- **GIVEN** um registro prévio e pendente no `chaos_event_log`
- **WHEN** o operador remove e finaliza o evento ativo da tabela principal de caos
- **THEN** o sistema injeta o `timestamp_end` no registro permanente de ML sem deletar a linha

#### Scenario: Consultar log de caos para análise
- **GIVEN** que a tabela de log de simulação de caos contém milhares de registros acumulados
- **WHEN** o operador faz GET em `/chaos/log?limit=50&offset=0`
- **THEN** o sistema devolve apenas a página restrita com os 50 registros mais recentes para alimentar os engenheiros de dados
