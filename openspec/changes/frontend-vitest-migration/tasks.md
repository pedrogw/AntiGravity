## 1. Migração da Infraestrutura de Testes

- [x] 1.1 Remover dependências do Jest (`jest`, `jest-environment-jsdom`) do `package.json` e apagar `jest.config.ts`, `jest.setup.ts`, `jest.polyfills.ts`.
- [x] 1.2 Instalar dependências do Vitest (`vitest`, `@testing-library/react`, `jsdom`).
- [x] 1.3 Criar `vitest.config.ts` com configuração para ambiente `jsdom` e setup file para RTL.
- [x] 1.4 Refatorar testes existentes em `__tests__/` para usar as importações globais ou manuais do `vitest` (trocar `jest.fn()` por `vi.fn()`, etc).
- [x] 1.5 Rodar `npm run test` garantindo que os testes básicos de componentes continuam passando.
