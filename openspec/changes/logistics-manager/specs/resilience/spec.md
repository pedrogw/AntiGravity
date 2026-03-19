## ADDED Requirements

### Requirement: Tratamento Global de Falhas de Infraestrutura
O sistema backend SHALL implementar um Exception Handler global para isolar e tratar erros originados por serviços externos ou internos de infraestrutura (como falhas de conexão com o banco de dados PostgreSQL). A aplicação MUST NUNCA expor stack traces ou detalhes mecânicos do erro na resposta HTTP do cliente.

#### Scenario: Banco de Dados PostgreSQL indisponível
- **GIVEN** que o banco de dados PostgreSQL está offline, gerando timeout, ou atingiu o limite máximo de conexões (Ex: `asyncpg.exceptions.ConnectionDoesNotExist`)
- **WHEN** qualquer usuário ou motorista dispara uma requisição que requer persistência ou leitura no banco (ex: POST em `/safe-check/position`)
- **THEN** a camada de Exception Handler do FastAPI **MUST** interceptar a falha graciosamente, registrar o erro interno no logger do servidor, e retornar uma resposta HTTP 503 (Service Unavailable) com a mensagem amigável: *"Serviço temporariamente indisponível. Tente novamente em instantes."*

### Requirement: Validação Restrita do Contrato de Dados (Client-Side e Server-Side)
O sistema SHALL proteger a integridade dos dados trafegados garantindo duas camadas de validação. O Frontend MUST validar os inputs antes de iniciar qualquer chamada de rede. O Backend MUST validar estritamente (Pydantic v2) todos os payloads recebidos. O sistema MUST retornar HTTP 422 em caso de falha de validação na API.

#### Scenario: Frontend retém requisição malformada (Client-Side)
- **GIVEN** que o painel do operador está ativo na sessão de injeção de caos
- **WHEN** o operador tenta submeter (POST) o formulário de um evento de caos sem preencher os campos obrigatórios (ex: omite a seleção da entrega ou o tipo do evento)
- **THEN** a interface **MUST** reter a ação via validação nativa (ex: Zod/React Hook Form), bloqueando a chamada de rede e destacando visualmente em vermelho na UI os campos faltantes.

#### Scenario: Backend rejeita requisição inválida (Server-Side)
- **GIVEN** que uma requisição POST é disparada para `/chaos/events` via script automatizado ou bypass no frontend
- **WHEN** o payload recebido pela API não contém a chave obrigatória `type` do evento de caos
- **THEN** a camada de validação estrutural do FastAPI (Pydantic v2) **MUST** rejeitar a requisição imediatamente antes de processar qualquer lógica de negócio, retornando HTTP 422 (Unprocessable Entity) com o detalhamento estrito do campo ausente ou tipagem violada.
