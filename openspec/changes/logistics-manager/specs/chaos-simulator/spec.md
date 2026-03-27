## ADDED Requirements

### Requirement: Catálogo de eventos de caos
O sistema SHALL suportar 4 tipos de eventos de caos pré-definidos: chuva (impact_factor=1.3), alagamento (delay=45min), engarrafamento (impact_factor=1.5, delay=15min), acidente (delay=60min). Cada evento MUST ter tipo, severidade, impact_factor e delay_minutes. Eventos NÃO alteram a rota — apenas o tempo estimado.

#### Scenario: Listar tipos de evento disponíveis no ambiente
- **GIVEN** que o catálogo de eventos de caos possui 4 eventos pré-cadastrados (chuva, alagamento, engarrafamento, acidente)
- **WHEN** o banco de testes bate em GET `/chaos/event-types`
- **THEN** o sistema retorna os 4 tipos exatos com seus parâmetros técnicos padrões (impact_factor e delay_minutes)

### Requirement: Injeção Autônoma/Scriptada de Caos
O sistema SHALL expor hooks restritos para acoplamento do clima num teste. Ao ser submetido, o ETA MUST ser recalculado na hora pela fórmula temporal.

#### Scenario: Carga climática afeta a viagem
- **GIVEN** uma entrega com o status "em_transito" cruzando uma rodovia
- **WHEN** a ferramenta de Banca Administrativa submete via POST em `/chaos/events` o id e type="chuva"
- **THEN** o sistema cria ativamente o evento, recalcula o ETA restante aplicando fator 1.3, registra em eta_history e retorna HTTP 201 com o novo ETA

#### Scenario: Hook rejeitado por entrega inativa
- **GIVEN** uma entrega que já foi finalizada com o status "entregue"
- **WHEN** a automação Admin clica em trigger de cenários passados
- **THEN** o sistema bloqueia a ação e retorna HTTP 422 "Só é possível injetar caos em entregas em trânsito"

### Requirement: Remoção e Limpeza Climática Temporal
O sistema SHALL suportar finalização limpa de intempéries atreladas a uma corrida atual via DevEndpoints.

#### Scenario: Ponto Cego de Chuva finalizado
- **GIVEN** que existe um evento de caos do tipo "chuva" atrelado e afetando o ETA de uma entrega
- **WHEN** a automação cessa e finaliza através de DELETE em `/chaos/events/{event_id}`
- **THEN** o sistema cessa a influência do evento, reverte o impacto de 1.3 no ETA restante, cria um marco em eta_history apontando a melhoria e retorna HTTP 200

### Requirement: Transparência Universal B2B do Caos
O sistema SHALL anexar visualizações explícitas de impedimentos temporais logados, permitindo Lojista entender porquê fura seu SLA.

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

#### Scenario: Evento remoto concluído crava stamp ML final
- **GIVEN** um registro prévio e pendente no `chaos_event_log`
- **WHEN** o ambiente encerra e destrói registro no core database da viagem ativa
- **THEN** o sistema injeta o `timestamp_end` no registro permanente de ML sem deletar a linha

#### Scenario: Analista de ML acessa raw pipeline
- **GIVEN** que a tabela de log de simulação de caos contém milhares de registros acumulados
- **WHEN** se extrai as métricas paginadas de GET `/chaos/log?limit=50&offset=0`
- **THEN** o sistema devolve apenas a página restrita com os 50 registros mais recentes para alimentar os engenheiros de dados
