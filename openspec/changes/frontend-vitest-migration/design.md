## Context

O projeto front-end React está fortemente acoplado à infraestrutura HTTP e ao local storage. Testes unitários do front são lentos com o Jest, pois o JS DOM acaba levantando o ambiente inteiro do React mesmo quando queremos testar funções de negócio (que no momento estão embutidas nos Hooks). Precisamos desacoplar o sistema (DDD) em camadas `domain`, `application`, `infrastructure` e `presentation`, substituindo também o Jest pelo Vitest.

## Goals / Non-Goals

**Goals:**
- Desacoplar a lógica de negócio dos componentes React, utilizando as camadas Clean Architecture.
- Instalar e configurar Vitest + React Testing Library (RTL).
- Atualizar a CI/CD e as configurações `package.json` para Vitest.
- Substituir o uso direto do Axios nos Hooks por injeção de `UseCases`.

**Non-Goals:**
- Refatoração total visual das telas (O UI não deve mudar nada).
- Integrações de novas bibliotecas de estado (ex: não queremos instalar Redux ou Zustand se o Context API e hooks customizados atuais atenderem).
- Não adicionaremos E2E Testing (Cypress/Playwright) nesta fase.

## Decisions

1. **Vitest no lugar do Jest:**
   - *Por quê?* O ecossistema em torno do Vite (mesmo não usando Vite no build do App Router do Next) torna os testes muito mais rápidos. O setup do Vitest no Next.js é simples e drop-in replacement na sintaxe de testes.
   - *Alternativas:* Manter Jest com ts-jest, o que mantém a compilação de testes muito lenta, prejudicando o TDD.

2. **Injeção de Dependência Manual (Factory Pattern):**
   - *Por quê?* Evita a necessidade de carregar bibliotecas pesadas de DI como `tsyringe` ou `inversify` que exigem `reflect-metadata`. Vamos usar arquivos puros exportando instâncias preenchidas para uso nos Hooks.
   
3. **Estrutura de Repositórios e Storage na Infraestrutura:**
   - `LocalStorageAdapter` protegerá as operações com tokens (para prevenir bugs de Server Side Rendering no Next).

## Risks / Trade-offs

- **[Risco] Aumento na complexidade de boilerplates:** Migrar para Clean Arch em React exige criar Classes de Erro, Entidades e Interfaces, aumentando o número de arquivos e steps cognitivos iniciais.
  - *Mitigação:* Usaremos ferramentas como TypeScript `interface` e POJOs no lugar de classes pesadas do tipo OOP clássico, preferindo funções quando o caso de uso não guardar estado interno.

- **[Risco] Testes do RTL falharem na migração:** O ambiente `jsdom` do Vitest pode se comportar minimamente diferente do Jest, e mockar as chamadas via Fetch ou API pode quebrar os testes antigos.
  - *Mitigação:* Faremos a migração etapa por etapa. Primeiro configuramos Vitest. Rodamos o RTL. Só então refatoramos as camadas da API para UseCases.
