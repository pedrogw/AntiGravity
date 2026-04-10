## ADDED Requirements

### Requirement: validation-hardening
Todos os inputs do modelo geográfico DEVEM validar limites físicos reais.

#### Scenario: Latitude Fora de Faixa
- **WHEN** O cliente envia Lat: 154.0
- **THEN** A API retorna 422 Unprocessable Entity

#### Scenario: Longitude Fora de Faixa
- **WHEN** O cliente envia Lng: -200.0
- **THEN** A API retorna 422 Unprocessable Entity

#### Scenario: Nome de Localidade Vazio
- **WHEN** O cliente envia "name": ""
- **THEN** A API retorna 422 Unprocessable Entity
