## ADDED Requirements

### Requirement: Hooks agnósticos de Rede
Custom hooks da aplicação (ex: `useAuth`, `useDeliveries`) MUST importar exclusivamentes instâncias de `UseCases` através da Factory/DI, e NUNCA devem importar pacotes HTTP (`axios`, `fetch`) ou de storage.

#### Scenario: Execução do Login no Hook
- **WHEN** o componente React invoca a função `login(email, pass)` exposta pelo `useAuth`
- **THEN** o hook atualiza seu estado `isLoading` para true, aguarda a execução assíncrona do `LoginUseCase.execute`, e atualiza o estado com a `UserEntity` se sucesso, ou expõe a mensagem de erro da `InvalidCredentialsError` se falha.
