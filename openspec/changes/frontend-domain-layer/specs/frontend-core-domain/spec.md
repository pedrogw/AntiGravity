## ADDED Requirements

### Requirement: Padrões de Entidades
O frontend MUST possuir Entidades autossuficientes modeladas em TypeScript dentro da pasta `src/domain/entities/`. Estas entidades MUST NÃO possuir dependências do React ou de frameworks de fetching.

#### Scenario: Instanciamento Seguro
- **WHEN** uma resposta bruta (JSON) é recebida da camada HTTP
- **THEN** ela é parseada e convertida na classe de Entidade garantindo que os tipos (como strings e datas) sejam corretos antes do retorno.

### Requirement: Tratamento de Erros Semânticos
Todos os erros de negócio ou de conexão MUST ser padronizados usando extends da classe genérica `Error` base em `src/domain/errors/`.

#### Scenario: Throw de um Erro Tratável
- **WHEN** a infraestrutura identifica um HTTP 401 Unauthorized
- **THEN** ela deve invocar um `throw new UnauthorizedError('Credenciais inválidas')`.
