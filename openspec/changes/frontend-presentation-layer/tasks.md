## 1. Refatoração dos Hooks de Autenticação

- [x] 1.1 Modificar `src/hooks/useAuth.ts` para importar e instanciar os Casos de Uso (`LoginUseCase`, `LogoutUseCase`) a partir da factory.
- [x] 1.2 Remover dependências de Axios e localStorage do `useAuth.ts`.
- [x] 1.3 Implementar a captura das exceções de Domínio (ex: `catch (e) { if (e instanceof InvalidCredentialsError) ... }`).
- [x] 1.4 Testar `useAuth.ts` via Vitest e `@testing-library/react-hooks` ou diretamente no componente de mock.

## 2. Refatoração dos Hooks Secundários

- [x] 2.1 Refatorar/Criar `useDeliveries.ts` conectando-o aos seus Casos de Uso.
- [x] 2.2 Refatorar/Criar `usePlaces.ts` conectando-o aos seus Casos de Uso.
- [x] 2.3 Padronizar o retorno dos Hooks (sempre retornar Entidades puras ou primitives).

## 3. Adaptação dos Componentes de Apresentação (UI)

- [x] 3.1 Atualizar `LoginForm.tsx` para consumir as novas assinaturas de `useAuth` e exibir mensagens de erro amigáveis ao usuário caso `InvalidCredentialsError` ocorra.
- [x] 3.2 Atualizar listagens de dados (ex: Dashboard de motorista) para ler propriedades dos objetos de Entidade (e não mais JSON solto).
- [x] 3.3 Rodar e adaptar os testes de RTL (`__tests__/components/`) para garantir que os testes de UI passem interagindo perfeitamente com os novos hooks.
