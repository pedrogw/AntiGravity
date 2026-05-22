## ADDED Requirements

### Requirement: Tratamento de Erro baseada em Intenção
Os Componentes de Interface MUST reagir aos erros verificando suas classes (Type Guards do TypeScript / `instanceof`) em vez de decodificar mensagens de status HTTP (como `error.response.status === 400`).

#### Scenario: Erro de Validação Visível
- **WHEN** a submissão de um formulário falha porque a entidade de domínio jogou um erro de validação de negócios (ex: `ValidationError`)
- **THEN** o componente captura esse erro e o formata para exibição em texto vermelho específico ao input afetado, sem precisar logar códigos HTTP.
