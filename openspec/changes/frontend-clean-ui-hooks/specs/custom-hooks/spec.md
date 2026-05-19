## ADDED Requirements

### Requirement: Centralização de Estado e I/O
O sistema SHALL extrair toda a lógica de estado do React (`useState`, `useEffect`) relacionada a chamadas de rede e ciclo de vida de negócio para dentro de funções isoladas denominadas Hooks Customizados.

#### Scenario: Gestão Pura de Login
- **WHEN** um usuário tenta fazer login no sistema
- **THEN** o arquivo de UI (`page.tsx`) MUST delegar o controle de carregamento, manipulação de erro e submissão da credencial para um hook dedicado (ex: `useAuth`), sem orquestrar regras HTTP localmente.
