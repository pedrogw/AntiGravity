## Why

Com as Fundações do Domínio e da Infraestrutura mapeadas na Fase 2, o Frontend agora tem os blocos de montar, mas falta a "cola" que os une: os Casos de Uso (Application Layer). Atualmente, componentes e hooks injetam regras de negócio diretamente neles (ex: validação dupla, formatação de dados antes do request). Centralizar isso em Casos de Uso puramente agnósticos aumenta exponencialmente a coesão, permitindo que a mesma lógica seja consumida por telas diferentes ou até interfaces de CLI, e facilita imensamente o TDD.

## What Changes

- Criação dos Casos de Uso (`UseCases`) que operam as Entidades e chamam os Repositórios do domínio.
- Injeção de Dependências manual via Factory que instanciará Repositórios e os passará para os UseCases.
- Os Casos de Uso serão completamente isolados de bibliotecas do React (sem importar `useState`, `useEffect` ou qualquer coisa do ecossistema do navegador/React).
- Os Casos de Uso retornarão sempre instâncias de Entidades puras ou jogarão Erros de Domínio previsíveis.

## Capabilities

### New Capabilities
- `frontend-application-use-cases`: Introdução do padrão de Casos de Uso (Use Cases) no frontend, atuando como orquestradores de regras de negócio estritas.
- `frontend-dependency-injection`: Sistema manual de Injeção de Dependências (DI Container / Factories) para acoplar a infraestrutura (Axios) aos Casos de Uso.

### Modified Capabilities
- Nenhuma. O produto final continuará operando exatamente do mesmo modo; apenas o fluxo de dados interno está sendo re-arquitetado.

## Impact

- **Testes Unitários:** Serão o foco principal desta fase. Testar a camada de `application` no Vitest é extremamente rápido e garantirá a segurança lógica de todas as features sem precisar instanciar a UI.
- **Isolamento da Apresentação:** Esta fase prepara o terreno definitivo para a Fase 4, onde o React se tornará puramente burro ("dumb view"), apenas exibindo dados e disparando os UseCases.
