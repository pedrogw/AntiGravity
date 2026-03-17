## ADDED Requirements

### Requirement: CRUD de entregas
O sistema SHALL permitir ao operador criar, listar, atualizar e cancelar entregas. Cada entrega MUST ter: fábrica de origem, loja de destino, motorista atribuído, status e ETA calculado.

#### Scenario: Criar entrega
- **GIVEN** que os IDs fornecidos (factory_id, store_id e driver_id) existem e são válidos no banco de dados
- **WHEN** o operador faz POST em `/deliveries/` com esses dados
- **THEN** o sistema cria a entrega com o status inicial "pendente", calcula o ETA via Haversine e retorna HTTP 201

#### Scenario: Listar entregas por role com paginação
- **GIVEN** um lojista autenticado que possui múltiplas lojas sob sua jurisdição
- **WHEN** este lojista faz GET em `/deliveries/?limit=10&offset=0`
- **THEN** o sistema filtra e retorna apenas as entregas destinadas às lojas desse lojista específico, incluindo a metadata de paginação (total, limit, offset e items)

#### Scenario: Listar entregas com paginação padrão
- **GIVEN** que o endpoint de listagem de entregas requer controle de paginação
- **WHEN** um lojista faz GET em `/deliveries/` omitindo os parâmetros `limit` e `offset`
- **THEN** o sistema aplica com sucesso os defaults de limit=20 e offset=0 para a query no banco

#### Scenario: Motorista visualiza suas entregas
- **GIVEN** um motorista autenticado via JWT
- **WHEN** este motorista faz GET em `/deliveries/`
- **THEN** o sistema restringe o escopo e retorna única e exclusivamente as entregas atribuídas ao ID deste motorista contido no token

### Requirement: Ciclo de vida da entrega
O sistema SHALL gerenciar os seguintes estados: pendente → em_transito → entregue (ou cancelada). Transições de estado MUST ser validadas. Todos os timestamps MUST ser armazenados em UTC.

#### Scenario: Iniciar transporte
- **GIVEN** uma entrega com o status atual "pendente"
- **WHEN** o motorista designado faz PATCH em `/deliveries/{id}/status` enviando status="em_transito"
- **THEN** o sistema atualiza o status, registra o carimbo `departed_at` em UTC e inicia o monitoramento ativo de safe-check

#### Scenario: Confirmar entrega
- **GIVEN** uma entrega cujo status atual é "em_transito"
- **WHEN** o motorista faz PATCH em `/deliveries/{id}/status` enviando status="entregue"
- **THEN** o sistema finaliza o ciclo registrando `delivered_at` em UTC e encerra as obrigações de ping do monitoramento de segurança

#### Scenario: Transição inválida
- **GIVEN** uma entrega que já foi concluída e encontra-se com o status "entregue"
- **WHEN** o motorista tenta retroceder o status fazendo PATCH para "em_transito"
- **THEN** o sistema bloqueia a alteração de estado e retorna HTTP 422 "Transição de status inválida"

### Requirement: Reroute pelo motorista
O sistema SHALL aceitar reroute via POST `/deliveries/{id}/reroute` com posição atual do motorista. O ETA MUST ser recalculado com a nova distância restante.

#### Scenario: Motorista faz reroute
- **GIVEN** que uma entrega está ativamente "em_transito"
- **WHEN** o motorista faz POST em `/deliveries/{id}/reroute` enviando suas novas coordenadas `lat` e `lng`
- **THEN** o sistema descarta a rota original, recalcula a distância direta (posição atual → loja), reaplica os eventos de caos ativos e retorna o novo ETA

#### Scenario: Reroute registrado no histórico
- **GIVEN** um motorista executando uma chamada de reroute perfeitamente válida
- **WHEN** o sistema conclui o novo cálculo de ETA
- **THEN** a aplicação registra obrigatoriamente essa mudança na tabela `eta_history` sinalizando `reason="reroute_motorista"`
