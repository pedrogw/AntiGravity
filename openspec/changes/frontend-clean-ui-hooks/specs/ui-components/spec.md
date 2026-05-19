## ADDED Requirements

### Requirement: Isolação de UI (Dumb Components)
O sistema SHALL quebrar grandes blocos de marcação JSX (como formulários extensos ou cards de dados densos) em componentes independentes, que recebem seus dados exclusivamente via propriedades (`props`) e comunicam ações via callbacks.

#### Scenario: Formulário Reutilizável e Testável
- **WHEN** o sistema renderiza o layout de Login
- **THEN** o formulário em si MUST ser um componente independente (`LoginForm`) que recebe `isLoading` e um callback `onSubmit` como propriedades, sem saber internamente qual endpoint da API será acionado para validar o usuário.
