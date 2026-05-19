## Why

O frontend atual concentra responsabilidades de requisição de API, gerenciamento de estado e estrutura visual diretamente dentro dos arquivos de página (como `src/app/page.tsx`). Isso viola a separação de conceitos (Separation of Concerns) e dificulta a testabilidade e reuso. Precisamos elevar a qualidade do código frontend abstraindo a lógica de estado/API em Custom Hooks e extraindo blocos visuais repetitivos ou densos para Componentes reutilizáveis.

## What Changes

- Criação do diretório `src/hooks/` para abrigar a lógica da aplicação (ex: `useAuth`, `useDeliveries`).
- Extração de formulários complexos (ex: `<LoginForm>`) do arquivo de rotas para a pasta `src/components/`.
- Limpeza dos arquivos `page.tsx` para se tornarem meros orquestradores de layout, conectando os Hooks aos Componentes Visuais.
- **BREAKING**: Nenhuma mudança de requisito, mas refatoração estrutural no Next.js App Router.

## Capabilities

### New Capabilities
- `custom-hooks`: Camada de aplicação no frontend que centraliza chamadas à infraestrutura (APIs) e o estado atrelado a elas.
- `ui-components`: Estrutura hierárquica de componentes visuais puramente focados em apresentação, separando o "dumb" (visual) do "smart" (página/hook).

### Modified Capabilities
- Nenhuma modificação de requisito de negócio.

## Impact

- `src/app/page.tsx` se tornará substancialmente menor e mais legível.
- `src/components/` passará a abrigar peças reutilizáveis.
- `__tests__/` serão mais direcionados: poderemos testar os hooks independentemente usando o `@testing-library/react` e componentes visuais de forma isolada.
