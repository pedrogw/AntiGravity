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
O sistema SHALL recalcular o ETA de uma entrega em andamento quando eventos de caos são injetados. O novo ETA MUST considerar o tempo já percorrido e os fatores de impacto dos eventos ativos.

#### Scenario: Recálculo por evento de caos
- **WHEN** um evento de chuva (impact_factor=1.3) é injetado em entrega com ETA restante de 2h
- **THEN** o novo ETA restante é 2h × 1.3 = 2h36min

#### Scenario: Múltiplos eventos acumulados
- **WHEN** chuva (factor=1.3) e engarrafamento (factor=1.5, delay=15min) estão ativos na mesma entrega
- **THEN** o ETA é recalculado como (ETA_restante × 1.3 × 1.5) + 15min
