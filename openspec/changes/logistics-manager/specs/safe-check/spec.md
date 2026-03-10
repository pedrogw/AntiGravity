## ADDED Requirements

### Requirement: Atualização de posição do motorista
O sistema SHALL aceitar atualizações periódicas de posição (lat/lng e velocidade) do motorista. Cada atualização MUST registrar timestamp, coordenadas e velocidade atual.

#### Scenario: Motorista atualiza posição normalmente
- **WHEN** motorista faz POST em `/safe-check/position` com lat, lng e speed=80
- **THEN** o sistema registra posição, retorna HTTP 200 com status "ok"

### Requirement: Detecção de parada (velocidade zero)
O sistema SHALL detectar quando o motorista reporta velocidade = 0 km/h ou não atualiza posição por mais de 10 minutos. Ao detectar, MUST criar um ping com timer de 5 minutos exigindo resposta.

#### Scenario: Motorista para e sistema envia ping
- **WHEN** motorista reporta speed=0 em entrega ativa
- **THEN** o sistema cria um registro de ping com expires_at = now + 5 minutos e retorna status "ping_pendente"

#### Scenario: Motorista responde ao ping dentro do timer
- **WHEN** motorista faz POST em `/safe-check/ping/{ping_id}/respond` com motivo
- **THEN** o sistema marca ping como "respondido", retorna HTTP 200, nenhum alerta gerado

#### Scenario: Motorista não responde ao ping
- **WHEN** ping expira sem resposta (timer de 5 minutos esgotado)
- **THEN** o sistema gera alerta nível ALTO com tipo "sem_resposta" visível para operador

### Requirement: Detecção de desvio de rota
O sistema SHALL calcular a distância entre a posição atual do motorista e a rota esperada (linha reta fábrica→loja). Se o desvio exceder 2 km, MUST gerar alerta CRÍTICO imediato.

#### Scenario: Motorista dentro da rota
- **WHEN** motorista reporta posição a 500m da linha fábrica→loja
- **THEN** o sistema retorna status "ok", nenhum alerta

#### Scenario: Motorista desvia da rota
- **WHEN** motorista reporta posição a 3 km da linha fábrica→loja
- **THEN** o sistema gera alerta nível CRÍTICO com tipo "desvio_rota" imediatamente, visível para operador

### Requirement: Consulta de alertas
O sistema SHALL permitir ao operador listar todos os alertas ativos e históricos. Cada alerta MUST conter: tipo, nível, delivery_id, driver_id, timestamp e status (ativo/resolvido).

#### Scenario: Operador lista alertas ativos
- **WHEN** operador faz GET em `/safe-check/alerts?status=ativo`
- **THEN** o sistema retorna todos os alertas ativos ordenados por nível (CRÍTICO primeiro)

#### Scenario: Operador resolve alerta
- **WHEN** operador faz PATCH em `/safe-check/alerts/{id}` com status="resolvido" e nota
- **THEN** o sistema marca alerta como resolvido com timestamp e nota do operador
