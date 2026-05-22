## ADDED Requirements

### Requirement: Camadas da Arquitetura Limpa
O frontend MUST adotar o pattern de Clean Architecture através de quatro diretórios primários em `src/`: `domain`, `application`, `infrastructure`, e `presentation`.

#### Scenario: Organização do Código
- **WHEN** um novo feature é adicionado no frontend
- **THEN** a lógica de negócio estrita DEVE residir em `domain` (entidades e erros puros), o fluxo em `application` (UseCases), a conversão HTTP em `infrastructure`, e a exibição em `presentation`.

### Requirement: Injeção de Dependências
Os Hooks e Componentes React MUST interagir apenas com os Casos de Uso através de Injeção de Dependência manual, NUNCA invocando instâncias de Axios diretamente.

#### Scenario: Componente chamando API
- **WHEN** o componente `LoginForm` dispara o login
- **THEN** ele invoca o `useAuth`, que invoca o `LoginUseCase` importado de um arquivo de configuração de dependências em vez de chamar a URL da API diretamente.
