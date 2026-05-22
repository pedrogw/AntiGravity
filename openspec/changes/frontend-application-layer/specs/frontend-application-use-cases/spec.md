## ADDED Requirements

### Requirement: Centralização de Regras nos Casos de Uso
A lógica de negócio da interface MUST residir em classes localizadas sob `src/application/use_cases/`. Componentes visuais não podem executar lógicas de validações complexas relacionadas ao Domínio ou processar APIs diretamente.

#### Scenario: Submissão de Formulário
- **WHEN** o formulário de login é submetido
- **THEN** a UI aciona o `execute(input)` do `LoginUseCase` que validará as credenciais, fará a persistência nativa do token localmente usando a abstração injetada e retornará a classe `User`.

### Requirement: Isolamento Absoluto (Zero UI/HTTP dependencies)
Os Casos de Uso MUST NÃO conter nenhuma importação de `react` (ex: `useState`), nem de bibliotecas HTTP (ex: `axios`), importando exclusivamente as entidades/interfaces do Domínio.

#### Scenario: Execução em Testes Unitários Rígidos
- **WHEN** rodamos o Vitest sobre um Caso de Uso
- **THEN** o teste pode providenciar repositórios "Mock" em memória e validar 100% dos caminhos sem envolver a rede ou React.
