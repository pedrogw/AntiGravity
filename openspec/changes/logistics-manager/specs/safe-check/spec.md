## ADDED Requirements

### Requirement: Atualização de posição do motorista
O sistema SHALL aceitar atualizações periódicas de posição (lat/lng e velocidade) do motorista. Cada atualização MUST registrar timestamp em UTC, coordenadas e velocidade atual.

#### Scenario: Motorista atualiza posição normalmente
- **WHEN** motorista faz POST em `/safe-check/position` com lat, lng e speed=80
- **THEN** o sistema registra posição, retorna HTTP 200 com status "ok"

### Requirement: Detecção de parada com lazy evaluation
O sistema SHALL detectar quando o motorista reporta velocidade = 0 km/h ou não atualiza posição por mais de 10 minutos. Ao detectar, MUST criar um ping com timer de 5 minutos exigindo resposta. A expiração do ping SHALL ser verificada por lazy evaluation — o sistema compara `now() > expires_at` quando o ping é consultado, não via background task.

#### Scenario: Motorista para e sistema envia ping
- **WHEN** motorista reporta speed=0 em entrega ativa
- **THEN** o sistema cria um registro de ping com expires_at = now + 5 minutos e retorna status "ping_pendente"

#### Scenario: Motorista responde ao ping dentro do timer
- **WHEN** motorista faz POST em `/safe-check/ping/{ping_id}/respond` com motivo
- **THEN** o sistema marca ping como "respondido", retorna HTTP 200, nenhum alerta gerado

#### Scenario: Ping expirado detectado por lazy evaluation ao consultar
- **WHEN** operador faz GET em `/safe-check/alerts` e há um ping com expires_at < now() sem resposta
- **THEN** o sistema cria alerta nível ALTO com tipo "sem_resposta" naquele momento e o inclui na resposta

#### Scenario: Ping expirado detectado por lazy evaluation ao motorista atualizar posição
- **WHEN** motorista faz POST em `/safe-check/position` e há ping pendente expirado para sua entrega
- **THEN** o sistema cria alerta nível ALTO antes de processar a nova posição

### Requirement: Detecção de desvio de rota
O sistema SHALL calcular a distância entre a posição atual do motorista e a rota esperada (linha reta fábrica→loja). Se o desvio exceder 2 km, MUST gerar alerta CRÍTICO imediato.

#### Scenario: Motorista dentro da rota
- **WHEN** motorista reporta posição a 500m da linha fábrica→loja
- **THEN** o sistema retorna status "ok", nenhum alerta

#### Scenario: Motorista desvia da rota
- **WHEN** motorista reporta posição a 3 km da linha fábrica→loja
- **THEN** o sistema gera alerta nível CRÍTICO com tipo "desvio_rota" imediatamente, visível para operador

### Requirement: Consulta de alertas com paginação
O sistema SHALL permitir ao operador listar todos os alertas ativos e históricos com paginação (limit/offset com defaults). Cada alerta MUST conter: tipo, nível, delivery_id, driver_id, timestamp (UTC) e status (ativo/resolvido).

#### Scenario: Operador lista alertas ativos
- **WHEN** operador faz GET em `/safe-check/alerts?status=ativo&limit=20&offset=0`
- **THEN** o sistema retorna alertas ativos paginados, ordenados por nível (CRÍTICO primeiro)

#### Scenario: Operador lista alertas com paginação padrão
- **WHEN** operador faz GET em `/safe-check/alerts?status=ativo` sem limit/offset
- **THEN** o sistema usa defaults limit=20 e offset=0

#### Scenario: Operador resolve alerta
- **WHEN** operador faz PATCH em `/safe-check/alerts/{id}` com status="resolvido" e nota
- **THEN** o sistema marca alerta como resolvido com resolved_at em UTC e nota do operador
