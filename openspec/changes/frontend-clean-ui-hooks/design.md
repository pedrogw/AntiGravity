## Context

O frontend atual funciona bem e tem cobertura de testes com Jest e RTL, mas sua arquitetura interna tende a misturar responsabilidades. Com o crescimento das funcionalidades (entregas, perfis, relatórios), os arquivos `page.tsx` se tornarão monolitos imodificáveis e difíceis de cobrir por testes unitários focados.

## Goals / Non-Goals

**Goals:**
- Separar regras lógicas de regras visuais.
- Centralizar o ciclo de vida de entidades (fetching, loading, error state) em *Custom Hooks*.
- Construir componentes visuais independentes e passíveis de teste unitário limpo.

**Non-Goals:**
- Adotar um gerenciador de estado global (como Redux) desnecessariamente. Manteremos os Hooks simples acoplados ao ciclo do React.
- Migrar o framework de testes de Jest para Vitest (ainda que Vitest seja mais rápido, a refatoração agora não exige essa quebra de tooling).

## Decisions

### Decisão 1: Abordagem de Estado
**Escolha**: Criaremos "Application Hooks" (ex: `useAuth`, `useDeliveries`) na pasta `src/hooks/`. Eles gerenciarão internamente `useState` e `useEffect` para se comunicarem com a API, retornando objetos simples (`{ data, isLoading, error, actions }`).
**Por quê**: Mantém a simplicidade do React nativo sem a complexidade de stores globais. Favorece o padrão RORO (Receive Object, Return Object) também no frontend.

### Decisão 2: Anatomia dos Componentes UI
**Escolha**: Componentes na pasta `src/components/` serão, por padrão, *dumb components*. Eles devem receber dados visuais via `props` e despachar eventos via `onAction`. O Hook consumirá a API e entregará os dados para a `page.tsx`, que por sua vez repassará as *props* aos componentes.
**Por quê**: Isso facilita o teste do componente isolado via React Testing Library, precisando apenas passar um objeto mock nas *props*.

## Risks / Trade-offs

| Risco | Mitigação |
|---|---|
| Boilerplate de Hooks | O excesso de hooks pode fragmentar lógicas adjacentes. Mitigação: usar hooks focados em domínios agregados (um hook por caso de uso, e não um por endpoint). |

## Migration Plan
1. Analisar o arquivo `src/app/page.tsx` para identificar a lógica de Autenticação/Login.
2. Extrair o estado de credenciais e requisição para `src/hooks/useAuth.ts`.
3. Extrair a renderização do formulário para `src/components/LoginForm.tsx`.
4. Refatorar o `page.tsx` original para orquestrar as duas peças.
5. Garantir que os testes existentes no Jest (ex: `login.test.tsx`) continuem passando (TDD/Refactoring flow).
