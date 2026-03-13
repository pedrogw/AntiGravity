## ADDED Requirements

### Requirement: Cálculo de ETA por Haversine
O sistema SHALL calcular a distância entre dois pontos (fábrica e loja) usando a fórmula de Haversine com coordenadas lat/lng. O ETA MUST ser calculado como `distância_km / velocidade_media_kmh`.

#### Scenario: Cálculo de ETA entre dois pontos
- **WHEN** uma entrega é criada com fábrica (lat:-23.55, lng:-46.63) e loja (lat:-22.90, lng:-43.17)
- **THEN** o sistema calcula distância ~360 km e ETA ~4.5h com velocidade padrão de 80 km/h

#### Scenario: Velocidade média configurável
- **WHEN** uma rota é cadastrada com tipo "urbana"
- **THEN** o sistema usa velocidade média de 40 km/h ao invés de 80 km/h

### Requirement: Recálculo dinâmico de ETA
O sistema SHALL recalcular o ETA de uma entrega em andamento quando eventos de caos são injetados. A rota é fixa — apenas o tempo é recalculado. O novo ETA MUST considerar o tempo já percorrido e os fatores de impacto dos eventos ativos.

#### Scenario: Recálculo por evento de caos
- **WHEN** um evento de chuva (impact_factor=1.3) é injetado em entrega com ETA restante de 2h
- **THEN** o novo ETA restante é 2h × 1.3 = 2h36min

#### Scenario: Múltiplos eventos acumulados
- **WHEN** chuva (factor=1.3) e engarrafamento (factor=1.5, delay=15min) estão ativos na mesma entrega
- **THEN** o ETA é recalculado como (ETA_restante × 1.3 × 1.5) + 15min

### Requirement: Histórico de ETA
O sistema SHALL registrar cada mudança de ETA em uma tabela `eta_history`. Cada registro MUST conter: delivery_id, eta_before, eta_after, reason (tipo do evento que causou a mudança) e timestamp em UTC.

#### Scenario: ETA recalculado por evento de caos é registrado no histórico
- **WHEN** evento de chuva recalcula ETA de 4h para 5h12min
- **THEN** o sistema cria registro em eta_history com eta_before=4h, eta_after=5h12min, reason="chaos:chuva"

#### Scenario: ETA recalculado por reroute é registrado no histórico
- **WHEN** motorista faz reroute e ETA muda de 3h para 2h
- **THEN** o sistema cria registro em eta_history com eta_before=3h, eta_after=2h, reason="reroute_motorista"

#### Scenario: Consultar histórico de ETA de uma entrega
- **WHEN** GET em `/deliveries/{id}/eta-history`
- **THEN** o sistema retorna lista ordenada por timestamp com todas as mudanças de ETA

### Requirement: Reroute pelo motorista
O sistema SHALL permitir ao motorista informar que mudou de rota via POST com sua posição atual (lat/lng). O sistema MUST recalcular a distância restante (posição atual → loja) usando Haversine, aplicar eventos de caos ativos e registrar a mudança no histórico de ETA.

#### Scenario: Motorista faz reroute com sucesso
- **WHEN** motorista faz POST em `/deliveries/{id}/reroute` com lat=-23.20 e lng=-45.90
- **THEN** o sistema calcula nova distância até a loja, recalcula ETA com eventos ativos, registra em eta_history e retorna novo ETA

#### Scenario: Reroute em entrega não em trânsito
- **WHEN** motorista tenta reroute em entrega com status "pendente"
- **THEN** o sistema retorna HTTP 422 "Reroute só é possível em entregas em trânsito"
