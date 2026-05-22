## Why

O frontend atual apresenta uma arquitetura fortemente acoplada à infraestrutura (Next.js, Axios, LocalStorage), misturando as regras de negócio com componentes e hooks de UI. Essa configuração torna a testabilidade difícil, aumenta a fragilidade do código em cenários de mudança tecnológica e atrasa os testes unitários. A substituição do Jest pelo Vitest e a introdução da Clean Architecture isolarão o Domínio, tornando o código mais flexível, testável e previsível.

## What Changes

- Refatoração da estrutura do frontend em quatro camadas limpas (`domain`, `application`, `infrastructure`, `presentation`).
- Criação das abstrações do core (Entidades, Value Objects, Erros e Repositórios) na camada `domain`.
- Implementação de Casos de Uso (ex: `LoginUseCase`, `CreateDeliveryUseCase`) orquestrando a lógica da UI.
- Migração dos adaptadores de infraestrutura e clientes (Axios e LocalStorage) para a camada `infrastructure`.
- Refatoração dos Hooks para executarem Casos de Uso via Injeção de Dependência, sem acesso direto a APIs.
- Substituição total do framework de testes `Jest` por `Vitest`.
- Adaptação dos testes do `React Testing Library` (RTL) para a API do Vitest.

## Capabilities

### New Capabilities
- `frontend-clean-architecture`: Estruturação das regras de negócio puras através das camadas do Domain-Driven Design adaptado ao frontend.
- `frontend-vitest-testing`: Adoção do framework Vitest para testes unitários e de integração no ambiente React.

### Modified Capabilities
- Nenhuma capacidade ou regra de sistema existente foi modificada ao nível de requisito externo. A alteração é puramente arquitetural e metodológica.

## Impact

- **Testes Unitários:** Serão migrados em massa. Novos testes focarão intensamente na camada de Casos de Uso e Entidades sem carregar a árvore de componentes do React.
- **Hooks da Aplicação:** Terão suas chamadas de API substituídas por invocações de Casos de Uso instanciados por um contêiner de dependências.
- **Integração Continua (CI):** Os comandos de script `test` e as configurações do GitHub Actions deverão executar Vitest no lugar do Jest.
- **Dependências:** Remoção de pacotes relacionados ao Jest (`jest`, `jest-environment-jsdom`) e instalação de pacotes relacionados ao Vitest (`vitest`, `@testing-library/react` compatível, etc).
