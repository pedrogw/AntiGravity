## 1. Setup do Projeto

- [ ] 1.1 Inicializar projeto Python com pyproject.toml, dependências (fastapi, uvicorn, sqlalchemy, asyncpg, pydantic, python-jose, passlib, alembic)
- [ ] 1.2 Criar estrutura de diretórios (app/core, app/auth, app/deliveries, app/chaos, app/safe_check, app/locations, app/demo)
- [ ] 1.3 Configurar core/config.py com settings via Pydantic BaseSettings (DATABASE_URL, SECRET_KEY, etc.)
- [ ] 1.4 Configurar core/database.py com engine async + sessionmaker + Base declarative (TIMESTAMP WITH TIME ZONE em todas as colunas datetime)
- [ ] 1.5 Configurar core/pagination.py com dependency reutilizável (limit default=20, offset default=0)
- [ ] 1.6 Configurar Alembic para migrações async com PostgreSQL
- [ ] 1.7 Criar app/main.py com FastAPI app, CORS, inclusão de routers e metadata para Swagger customizado

## 2. Autenticação Multi-Role

- [ ] 2.1 Criar models.py com modelo User (id, email, hashed_password, role, created_at UTC)
- [ ] 2.2 Criar schemas.py com UserCreate, UserLogin, UserResponse, TokenResponse
- [ ] 2.3 Criar core/security.py com hash de senha (passlib/bcrypt), criação e validação de JWT, dependency get_current_user
- [ ] 2.4 Criar dependencies de role: require_operador, require_lojista, require_motorista
- [ ] 2.5 Criar router.py com POST /auth/register e POST /auth/login
- [ ] 2.6 Criar service.py com lógica de registro e autenticação
- [ ] 2.7 Gerar migração Alembic para tabela users

## 3. Locations (Fábricas e Lojas)

- [ ] 3.1 Criar models.py com Factory (id, name, lat, lng) e Store (id, name, lat, lng, owner_id FK→User)
- [ ] 3.2 Criar schemas.py com CRUD schemas para Factory e Store
- [ ] 3.3 Criar router.py com CRUD endpoints e paginação (limit/offset) para fábricas (operador) e lojas (operador + lojista own)
- [ ] 3.4 Criar service.py com lógica de CRUD
- [ ] 3.5 Gerar migração Alembic para tabelas factories e stores

## 4. Janela de Recebimento

- [ ] 4.1 Criar modelo ReceivingWindow (id, store_id FK, day_of_week, start_time UTC, end_time UTC)
- [ ] 4.2 Criar schemas para configuração de janela
- [ ] 4.3 Criar endpoints POST/GET/PUT/DELETE em /stores/{id}/receiving-window
- [ ] 4.4 Criar função de validação: dado um datetime UTC, verificar se cai dentro da janela da loja
- [ ] 4.5 Gerar migração Alembic para tabela receiving_windows

## 5. Motor de ETA

- [ ] 5.1 Criar utils/haversine.py com função de cálculo de distância entre dois pontos (lat/lng)
- [ ] 5.2 Criar service de cálculo de ETA: distância / velocidade_média, retornando timedelta
- [ ] 5.3 Criar configuração de velocidades médias por tipo (urbana=40, rodovia=80)
- [ ] 5.4 Criar função de recálculo dinâmico considerando impact_factor e delay_minutes de eventos ativos

## 6. Gerenciamento de Entregas

- [ ] 6.1 Criar modelo Delivery (id, factory_id, store_id, driver_id, status, eta_original, eta_current, route_type, created_at UTC, departed_at UTC, delivered_at UTC)
- [ ] 6.2 Criar schemas com DeliveryCreate, DeliveryResponse (com paginação: total/limit/offset/items), DeliveryStatusUpdate
- [ ] 6.3 Criar enum DeliveryStatus (pendente, em_transito, entregue, cancelada) com validação de transição
- [ ] 6.4 Criar router.py com POST criar, GET listar (paginado, filtrado por role), GET detalhe, PATCH status
- [ ] 6.5 Criar service.py com lógica de criação (calcula ETA), listagem filtrada paginada e transição de status
- [ ] 6.6 Integrar validação de janela de recebimento na criação e recálculo (flag dentro/fora_da_janela)
- [ ] 6.7 Gerar migração Alembic para tabela deliveries

## 7. Reroute pelo Motorista

- [ ] 7.1 Criar endpoint POST /deliveries/{id}/reroute (aceita lat/lng da posição atual do motorista)
- [ ] 7.2 Implementar lógica: calcular nova distância (posição → loja) via Haversine, aplicar eventos ativos, retornar novo ETA
- [ ] 7.3 Validar que a entrega está em_transito (HTTP 422 se não estiver)

## 8. Histórico de ETA

- [ ] 8.1 Criar modelo EtaHistory (id, delivery_id FK, eta_before, eta_after, reason, timestamp UTC)
- [ ] 8.2 Criar função auxiliar register_eta_change(delivery_id, before, after, reason)
- [ ] 8.3 Integrar registro de histórico em: injeção de caos, remoção de caos e reroute
- [ ] 8.4 Criar endpoint GET /deliveries/{id}/eta-history retornando lista ordenada por timestamp
- [ ] 8.5 Gerar migração Alembic para tabela eta_history

## 9. Simulador de Caos

- [ ] 9.1 Criar modelo ChaosEvent (id, delivery_id FK, type enum, impact_factor, delay_minutes, created_at UTC, is_active)
- [ ] 9.2 Criar schemas ChaosEventCreate, ChaosEventResponse, ChaosEventTypeInfo
- [ ] 9.3 Criar endpoint GET /chaos/event-types retornando catálogo dos 4 tipos
- [ ] 9.4 Criar endpoint POST /chaos/events para injetar evento (valida entrega em_transito, recalcula ETA, registra em eta_history)
- [ ] 9.5 Criar endpoint DELETE /chaos/events/{id} para remover evento (recalcula ETA, registra em eta_history)
- [ ] 9.6 Criar endpoint GET /chaos/events?delivery_id= para listar eventos ativos (paginado)

## 10. Log de Caos para ML

- [ ] 10.1 Criar modelo ChaosEventLog (id, delivery_id, event_type, impact_factor, delay_minutes, lat_start, lng_start, lat_end, lng_end, timestamp_start UTC, timestamp_end UTC)
- [ ] 10.2 Integrar criação automática de registro no log ao injetar evento de caos
- [ ] 10.3 Integrar atualização de timestamp_end ao remover evento (sem deletar registro)
- [ ] 10.4 Criar endpoint GET /chaos/log com paginação e filtros por tipo e período
- [ ] 10.5 Gerar migração Alembic para tabela chaos_event_log

## 11. Safe-Check com Lazy Evaluation

- [ ] 11.1 Criar modelo PositionUpdate (id, delivery_id, driver_id, lat, lng, speed, timestamp UTC)
- [ ] 11.2 Criar modelo SafeCheckPing (id, delivery_id, driver_id, created_at UTC, expires_at UTC, status enum, response_reason)
- [ ] 11.3 Criar modelo Alert (id, delivery_id, driver_id, type, level, status, created_at UTC, resolved_at UTC, note)
- [ ] 11.4 Criar endpoint POST /safe-check/position para atualização de posição
- [ ] 11.5 Implementar lógica: se speed=0, criar ping com expires_at = now + 5 min
- [ ] 11.6 Implementar lazy evaluation: ao consultar ping ou alertas, verificar pings expirados e gerar alertas sob demanda
- [ ] 11.7 Criar endpoint POST /safe-check/ping/{id}/respond para resposta do motorista
- [ ] 11.8 Implementar detecção de desvio de rota (distância ponto-a-reta > 2 km → alerta CRÍTICO)
- [ ] 11.9 Criar endpoints GET /safe-check/alerts (paginado, filtrado por status) e PATCH /safe-check/alerts/{id} para operador
- [ ] 11.10 Gerar migração Alembic para tabelas position_updates, safe_check_pings, alerts

## 12. Endpoint de Demo

- [ ] 12.1 Criar endpoint POST /demo/simulate que orquestra fluxo completo
- [ ] 12.2 Implementar lógica: cria entrega temporária → calcula ETA → injeta caos (se solicitado) → recalcula → verifica janela → retorna JSON consolidado com histórico de ETA
- [ ] 12.3 Suporte a múltiplos tipos de caos e reroute simulado com resultado parcial de cada etapa

## 13. Swagger UI e Finalização

- [ ] 13.1 Customizar Swagger UI com título, descrição, tags agrupadas por domínio e tema
- [ ] 13.2 Adicionar exemplos ricos em cada schema Pydantic (model_config com json_schema_extra)
- [ ] 13.3 Criar seed script para popular banco com dados de demonstração (fábricas, lojas, motoristas, janelas)
- [ ] 13.4 Testar fluxo completo via Swagger UI (incluindo reroute e histórico de ETA)
- [ ] 13.5 Documentar README.md com instruções de setup, execução e uso
