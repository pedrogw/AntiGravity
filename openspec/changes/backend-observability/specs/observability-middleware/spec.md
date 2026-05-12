## ADDED Requirements

### Requirement: Request ID Tracking
A API SHALL garantir que toda requisição possua um identificador único de rastreio (`X-Request-ID`), injetado no log e retornado no cabeçalho de resposta.

#### Scenario: Injeção automática de Request ID
- **WHEN** uma requisição chega à API sem o header `X-Request-ID`
- **THEN** o middleware MUST gerar um UUID válido, incluí-lo no contexto de logs, e devolvê-lo na resposta HTTP com o header `X-Request-ID`

#### Scenario: Preservação de Request ID do cliente
- **WHEN** uma requisição chega à API contendo o header `X-Request-ID`
- **THEN** o middleware MUST respeitar o ID enviado pelo cliente e utilizá-lo no contexto de log e na resposta

### Requirement: Logging Estruturado de Requisições
O sistema SHALL registrar informações vitais de todas as requisições que transitam pela API, medindo tempo de processamento.

#### Scenario: Registro padrão de requisição
- **WHEN** o servidor processa e finaliza uma requisição HTTP
- **THEN** um log no nível `INFO` DEVE ser gerado contendo Método, Caminho (Path), Status Code HTTP, Tempo de Processamento (em ms) e o Request ID correspondente.

### Requirement: Data Masking Seguro em Logs
A geração de logs estruturados SHALL proteger informações sensíveis de usuários em todas as camadas de inspeção.

#### Scenario: Prevenção de vazamento de credenciais
- **WHEN** uma requisição carrega campos conhecidos como sensíveis (ex: `password`, `token`, `authorization`) no payload JSON ou Form Data
- **THEN** o sistema de logs DEVE mascarar o valor destes campos com identificadores genéricos (ex: `***`) antes da persistência do log no console/arquivo.

### Requirement: Monitoramento de Vivacidade (Healthcheck)
A API SHALL fornecer um endpoint público e leve para checagem de integridade e estabilidade do sistema.

#### Scenario: Consulta de status do servidor
- **WHEN** o cliente faz uma requisição `GET` para a rota `/health`
- **THEN** a API MUST responder `200 OK` retornando um payload JSON indicando a integridade da aplicação e disponibilidade do banco de dados (se aplicável).
