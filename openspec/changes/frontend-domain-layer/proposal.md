## Why

Com a infraestrutura de testes migrada para o Vitest (Fase 1), o frontend está pronto para receber sua camada mais importante: o **Domínio**. Atualmente, a ausência de uma modelagem forte no frontend resulta em componentes React que processam dados brutos de APIs sem tipagem robusta ou métodos utilitários, gerando duplicação de regras de negócio. Implementar o Domínio isolado resolve isso e prepara o terreno para os Casos de Uso.

## What Changes

- Criação dos contratos puros de Entidades (`User`, `Place`, `Delivery`).
- Criação dos Value Objects essenciais (ex: `Coordinates`, manipuladores de tokens JWT puros).
- Criação de Classes de Erro personalizadas (ex: `InvalidCredentialsError`, `NetworkError`) para unificar o tratamento de exceções.
- Definição dos protocolos de Repositório (`AuthRepositoryProtocol`, `DeliveryRepositoryProtocol`).
- Implementação inicial da Infraestrutura que assina esses contratos (ex: `ApiAuthRepository` encapsulando as chamadas HTTP e os adaptadores de LocalStorage).

## Capabilities

### New Capabilities
- `frontend-core-domain`: Criação das Entidades, Erros e Protocolos puramente em TypeScript, independentes de React ou Axios.
- `frontend-infrastructure-adapters`: Criação das implementações concretas dos Repositórios e do Storage Adapter.

### Modified Capabilities
- Nenhuma modificação em requisitos de produto. A mudança foca em estruturação interna de código (refactoring arquitetural).

## Impact

- **Segurança de Tipos:** O frontend passará a lidar com objetos instanciados do Domínio (com métodos próprios) em vez de tipos anêmicos ou dictionaries.
- **Isolamento de Falhas:** Erros da API (HTTP 401, 404, 500) serão interceptados na Infraestrutura e convertidos em Erros de Domínio previsíveis antes de chegarem aos componentes.
- **Testabilidade:** Esses repositórios e entidades poderão ser testados isoladamente no Vitest de forma imediata.
