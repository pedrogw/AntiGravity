## Context

Com o Domínio e a Aplicação prontos, a última milha é a integração com a UI. O Next.js e o React gerenciam estado (usando `useState`, `useReducer`, `useContext`), mas a invocação real da lógica deve ser terceirizada. Os Hooks Customizados (`useAuth`, `useDeliveries`) serão reescritos para orquestrar essa conexão.

## Goals / Non-Goals

**Goals:**
- Conectar os Custom Hooks às Factories de Injeção de Dependências.
- Adaptar o fluxo de erros nos componentes para usar as classes `instanceof DomainError`.
- Escrever testes de integração com RTL focados nesses novos Hooks e em seus componentes vitais.

**Non-Goals:**
- Não migraremos para Redux ou Context API complexos. Manteremos os Hooks locais e o gerenciamento simples atual, apenas modificando a fonte dos dados e as chamadas de mutação.

## Decisions

1. **Estado Assíncrono nos Hooks:**
   - *Decisão:* Os Hooks continuarão lidando com estados de `isLoading` e `error`. O UseCase processará a requisição em si, mas a responsabilidade de manter a flag de "carregando" na tela permanece no Hook.
   - *Por quê?* O UseCase não guarda estado. Ele é puro. O React precisa do Hook para engatilhar as re-renderizações baseadas no ciclo de vida da Promise do UseCase.

2. **Tratamento Global vs Local de Erros:**
   - *Decisão:* Erros de Domínio específicos (ex: `InvalidCredentialsError`) serão devolvidos pelo Hook para o Componente tratar localmente (exibir um span de erro vermelho abaixo do input). Erros de Sistema (ex: `NetworkError` ou `500 Internal Server Error`) poderão ser interceptados mais no topo e dispararão toasts genéricos.

## Risks / Trade-offs

- **[Risco] Re-renderizações acidentais:** Se a Injeção de Dependência criar novas instâncias do UseCase a cada renderização do componente, efeitos indesejados (`useEffect`) podem ser engatilhados.
  - *Mitigação:* Usaremos as instâncias exportadas diretamente como singletons ou caches da DI Factory, ou enveloparemos a injeção em `useMemo`/`useCallback` se a instância precisar ser criada on-the-fly pelo Hook.
