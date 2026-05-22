## ADDED Requirements

### Requirement: Injeção de Dependências Manual (Factories)
Todos os Casos de Uso MUST ter suas dependências injetadas de fora para dentro. Nenhuma classe de caso de uso deve importar e dar `new` numa classe de infraestrutura ou repositório concreto.

#### Scenario: Instanciação Pura
- **WHEN** precisamos utilizar o `CreateDeliveryUseCase` na interface do usuário
- **THEN** importamos uma factory pronta `makeCreateDeliveryUseCase()` que se encarregou de inicializar os repositórios Axios correspondentes e instanciar o UseCase.
