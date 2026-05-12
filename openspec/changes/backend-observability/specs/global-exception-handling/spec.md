## ADDED Requirements

### Requirement: Captura Global de Exceções de Domínio
O sistema SHALL possuir um mecanismo centralizado capaz de interceptar exceções disparadas pelas camadas de Use Case ou Domínio, prevenindo que cheguem ao usuário como "Internal Server Error" (500).

#### Scenario: Conversão de exceção customizada para HTTP
- **WHEN** um Caso de Uso dispara uma exceção do tipo `EntityNotFoundException` (ou similar)
- **THEN** o interceptor global MUST capturá-la e converter em uma resposta HTTP 404, contendo um payload de erro padronizado

#### Scenario: Padronização de estrutura de erro
- **WHEN** qualquer erro tratado é gerado pela aplicação
- **THEN** o payload JSON de resposta MUST possuir uma chave `"detail"` (ou equivalente) clara e amigável ao usuário

### Requirement: Isolamento de Stacktraces
A API SHALL impedir o vazamento de detalhes técnicos sensíveis de infraestrutura em caso de falhas inesperadas.

#### Scenario: Ocultação de detalhes de falhas nativas
- **WHEN** uma exceção não mapeada (ex: `KeyError`, falha de banco desconhecida) atinge a borda da aplicação
- **THEN** a resposta HTTP DEVE ser padronizada (ex: "Internal Error") e o stacktrace real DEVE ser gravado apenas nos logs internos do servidor, usando o Request ID.
