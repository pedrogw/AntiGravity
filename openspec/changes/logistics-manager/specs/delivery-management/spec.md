## ADDED Requirements

### Requirement: CRUD de entregas
O sistema SHALL permitir ao operador criar, listar, atualizar e cancelar entregas. Cada entrega MUST ter: fábrica de origem, loja de destino, motorista atribuído, status e ETA calculado.

#### Scenario: Criar entrega
- **WHEN** operador faz POST em `/deliveries/` com factory_id, store_id e driver_id
- **THEN** o sistema cria a entrega com status "pendente", calcula ETA e retorna HTTP 201

#### Scenario: Listar entregas por role com paginação
- **WHEN** lojista autenticado faz GET em `/deliveries/?limit=10&offset=0`
- **THEN** o sistema retorna apenas entregas destinadas às lojas desse lojista, com campos total, limit, offset e items

#### Scenario: Listar entregas com paginação padrão
- **WHEN** lojista faz GET em `/deliveries/` sem parâmetros de paginação
- **THEN** o sistema usa defaults limit=20 e offset=0

#### Scenario: Motorista visualiza suas entregas
- **WHEN** motorista autenticado faz GET em `/deliveries/`
- **THEN** o sistema retorna apenas entregas atribuídas a esse motorista

### Requirement: Ciclo de vida da entrega
O sistema SHALL gerenciar os seguintes estados: pendente → em_transito → entregue (ou cancelada). Transições de estado MUST ser validadas. Todos os timestamps MUST ser armazenados em UTC.

#### Scenario: Iniciar transporte
- **WHEN** motorista faz PATCH em `/deliveries/{id}/status` com status="em_transito"
- **THEN** o sistema atualiza status, registra departed_at em UTC e inicia monitoramento de safe-check

#### Scenario: Confirmar entrega
- **WHEN** motorista faz PATCH em `/deliveries/{id}/status` com status="entregue"
- **THEN** o sistema registra delivered_at em UTC e encerra monitoramento

#### Scenario: Transição inválida
- **WHEN** motorista tenta mudar status de "entregue" para "em_transito"
- **THEN** o sistema retorna HTTP 422 "Transição de status inválida"

### Requirement: Reroute pelo motorista
O sistema SHALL aceitar reroute via POST `/deliveries/{id}/reroute` com posição atual do motorista. O ETA MUST ser recalculado com a nova distância restante.

#### Scenario: Motorista faz reroute
- **WHEN** motorista faz POST em `/deliveries/{id}/reroute` com lat e lng
- **THEN** o sistema recalcula distância (posição → loja), recalcula ETA com eventos ativos e retorna novo ETA

#### Scenario: Reroute registrado no histórico
- **WHEN** motorista faz reroute com sucesso
- **THEN** o sistema registra mudança de ETA em eta_history com reason="reroute_motorista"
