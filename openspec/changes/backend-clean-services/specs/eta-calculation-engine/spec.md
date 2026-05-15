## ADDED Requirements

### Requirement: Cálculo Isolado de ETA
O sistema SHALL delegar qualquer estimativa matemática de tempo de chegada (ETA - Estimated Time of Arrival) para um serviço de domínio dedicado e stateless, livre de acoplamento com banco de dados ou frameworks.

#### Scenario: Predição baseada em coordenadas simples
- **WHEN** o serviço de ETA recebe um conjunto válido de coordenadas de origem e destino
- **THEN** o serviço MUST retornar uma estimativa de tempo (ex: em minutos) baseada em um algoritmo puro (ex: distância Haversine ajustada por fator de velocidade)

#### Scenario: Independência Arquitetural
- **WHEN** o serviço de ETA é instanciado para ser testado unitariamente
- **THEN** ele MUST funcionar perfeitamente sem necessidade de inicialização de conexões de banco de dados, mocks HTTP ou contextos do FastAPI
