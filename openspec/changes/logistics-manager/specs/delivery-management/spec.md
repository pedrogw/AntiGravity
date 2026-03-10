## ADDED Requirements

### Requirement: CRUD de entregas
O sistema SHALL permitir ao operador criar, listar, atualizar e cancelar entregas. Cada entrega MUST ter: fábrica de origem, loja de destino, motorista atribuído, status e ETA calculado.

#### Scenario: Criar entrega
- **WHEN** operador faz POST em `/deliveries/` com factory_id, store_id e driver_id
- **THEN** o sistema cria a entrega com status "pendente", calcula ETA e retorna HTTP 201

#### Scenario: Listar entregas por role
- **WHEN** lojista autenticado faz GET em `/deliveries/`
- **THEN** o sistema retorna apenas entregas destinadas às lojas desse lojista

#### Scenario: Motorista visualiza suas entregas
- **WHEN** motorista autenticado faz GET em `/deliveries/`
- **THEN** o sistema retorna apenas entregas atribuídas a esse motorista

### Requirement: Ciclo de vida da entrega
O sistema SHALL gerenciar os seguintes estados: pendente → em_transito → entregue (ou cancelada). Transições de estado MUST ser validadas.

#### Scenario: Iniciar transporte
- **WHEN** motorista faz PATCH em `/deliveries/{id}/status` com status="em_transito"
- **THEN** o sistema atualiza status, registra hora de saída e inicia monitoramento de safe-check

#### Scenario: Confirmar entrega
- **WHEN** motorista faz PATCH em `/deliveries/{id}/status` com status="entregue"
- **THEN** o sistema registra hora de entrega e encerra monitoramento

#### Scenario: Transição inválida
- **WHEN** motorista tenta mudar status de "entregue" para "em_transito"
- **THEN** o sistema retorna HTTP 422 "Transição de status inválida"
