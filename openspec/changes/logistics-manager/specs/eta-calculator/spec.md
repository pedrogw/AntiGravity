## ADDED Requirements

### Requirement: Cálculo de ETA por Haversine
O sistema SHALL calcular a distância entre dois pontos (fábrica e loja) usando a fórmula de Haversine com coordenadas lat/lng. O ETA MUST ser calculado como `distância_km / velocidade_media_kmh`.

#### Scenario: Cálculo de ETA entre dois pontos
- **GIVEN** que existe uma fábrica em SP e uma loja no RJ cadastradas com coordenadas lat/lng válidas
- **WHEN** uma entrega é criada ligando estes dois pontos
- **THEN** o sistema calcula distância ~360 km e ETA ~4.5h assumindo velocidade padrão de 80 km/h

#### Scenario: Velocidade média configurável
- **GIVEN** que o sistema possui configuração de velocidades médias por tipo de rota
- **WHEN** uma rota é cadastrada explicitamente com o tipo "urbana"
- **THEN** o sistema usa velocidade média de 40 km/h ao invés de 80 km/h no cálculo do ETA

### Requirement: Recálculo dinâmico de ETA
O sistema SHALL recalcular o ETA de uma entrega em andamento quando eventos de caos são injetados. A rota é fixa — apenas o tempo é recalculado. O novo ETA MUST considerar o tempo já percorrido e os fatores de impacto dos eventos ativos.

#### Scenario: Recálculo por evento de caos
- **GIVEN** uma entrega em andamento cujo ETA restante calculado no instante atual é de 2h
- **WHEN** um evento de chuva (impact_factor=1.3) é injetado nesta entrega
- **THEN** o novo ETA restante é atualizado para 2h × 1.3 = 2h36min

#### Scenario: Múltiplos eventos acumulados
- **GIVEN** uma entrega em andamento
- **WHEN** chuva (factor=1.3) e engarrafamento (factor=1.5, delay=15min) são ativados simultaneamente
- **THEN** o ETA é recalculado agregando os fatores: (ETA_restante × 1.3 × 1.5) + 15min

### Requirement: Histórico de ETA
O sistema SHALL registrar cada mudança de ETA em uma tabela `eta_history`. Cada registro MUST conter: delivery_id, eta_before, eta_after, reason (tipo do evento que causou a mudança) e timestamp em UTC.

#### Scenario: ETA recalculado por evento de caos é registrado no histórico
- **GIVEN** uma entrega com ETA atual de 4h
- **WHEN** um evento de chuva recalcula o ETA para 5h12min
- **THEN** o sistema cria um registro em eta_history contendo eta_before=4h, eta_after=5h12min, reason="chaos:chuva"

#### Scenario: ETA recalculado por reroute é registrado no histórico
- **GIVEN** uma entrega em andamento com ETA atual de 3h
- **WHEN** o motorista efetua um reroute que altera o ETA restante para 2h
- **THEN** o sistema cria um registro em eta_history contendo eta_before=3h, eta_after=2h, reason="reroute_motorista"

#### Scenario: Consultar histórico de ETA de uma entrega
- **GIVEN** que uma entrega possui múltiplos registros na tabela de histórico de ETA
- **WHEN** um request GET é feito em `/deliveries/{id}/eta-history`
- **THEN** o sistema retorna uma lista ordenada cronologicamente por timestamp detalhando a evolução do ETA

### Requirement: Reroute pelo motorista
O sistema SHALL permitir ao motorista informar que mudou de rota via POST com sua posição atual (lat/lng). O sistema MUST recalcular a distância restante (posição atual → loja) usando Haversine, aplicar eventos de caos ativos e registrar a mudança no histórico de ETA.

#### Scenario: Motorista faz reroute com sucesso
- **GIVEN** que uma entrega está com o status "em_transito"
- **WHEN** o motorista faz POST em `/deliveries/{id}/reroute` enviando as novas coordenadas atuais
- **THEN** o sistema calcula a nova distância até a loja via Haversine, aplica os eventos de caos vigentes, salva em eta_history e devolve o novo ETA

#### Scenario: Reroute em entrega não em trânsito
- **GIVEN** uma entrega que ainda está com o status "pendente" (não iniciada)
- **WHEN** o motorista tenta efetuar um reroute
- **THEN** o sistema rejeita a operação retornando HTTP 422 "Reroute só é possível em entregas em trânsito"
