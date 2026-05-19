## ADDED Requirements

### Requirement: Imutabilidade de Conceitos Estruturais
O sistema SHALL proteger a integridade de dados que representam conceitos atômicos através do encapsulamento em objetos imutáveis.

#### Scenario: Prevenção de alteração acidental de coordenadas
- **WHEN** um cálculo de ETA recebe coordenadas geográficas da Fábrica e da Loja
- **THEN** o objeto (ex: `Coordinates`) MUST garantir que os atributos `lat` e `lng` não possam ser reatribuídos independentemente após sua criação.
