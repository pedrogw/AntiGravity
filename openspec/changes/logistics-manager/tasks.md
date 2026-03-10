## 1. Setup do Projeto

- [ ] 1.1 Inicializar projeto Python com pyproject.toml, dependências (fastapi, uvicorn, sqlalchemy, asyncpg, pydantic, python-jose, passlib, alembic)
- [ ] 1.2 Criar estrutura de diretórios (app/core, app/auth, app/deliveries, app/chaos, app/safe_check, app/locations, app/demo)
- [ ] 1.3 Configurar core/config.py com settings via Pydantic BaseSettings (DATABASE_URL, SECRET_KEY, etc.)
- [ ] 1.4 Configurar core/database.py com engine async + sessionmaker + Base declarative
- [ ] 1.5 Configurar Alembic para migrações async com PostgreSQL
- [ ] 1.6 Criar app/main.py com FastAPI app, CORS, inclusão de routers e metadata para Swagger customizado

## 2. Autenticação Multi-Role

- [ ] 2.1 Criar models.py com modelo User (id, email, hashed_password, role, created_at)
- [ ] 2.2 Criar schemas.py com UserCreate, UserLogin, UserResponse, TokenResponse
- [ ] 2.3 Criar core/security.py com hash de senha (passlib/bcrypt), criação e validação de JWT, dependency get_current_user
- [ ] 2.4 Criar dependencies de role: require_operador, require_lojista, require_motorista
- [ ] 2.5 Criar router.py com POST /auth/register e POST /auth/login
- [ ] 2.6 Criar service.py com lógica de registro e autenticação
- [ ] 2.7 Gerar migração Alembic para tabela users

## 3. Locations (Fábricas e Lojas)

- [ ] 3.1 Criar models.py com Factory (id, name, lat, lng) e Store (id, name, lat, lng, owner_id FK→User)
- [ ] 3.2 Criar schemas.py com CRUD schemas para Factory e Store
- [ ] 3.3 Criar router.py com CRUD endpoints para fábricas (operador) e lojas (operador + lojista own)
- [ ] 3.4 Criar service.py com lógica de CRUD
- [ ] 3.5 Gerar migração Alembic para tabelas factories e stores

## 4. Janela de Recebimento

- [ ] 4.1 Criar modelo ReceivingWindow (id, store_id FK, day_of_week, start_time, end_time)
- [ ] 4.2 Criar schemas para configuração de janela
- [ ] 4.3 Criar endpoints POST/GET/PUT/DELETE em /stores/{id}/receiving-window
- [ ] 4.4 Criar função de validação: dado um datetime, verificar se cai dentro da janela da loja
- [ ] 4.5 Gerar migração Alembic para tabela receiving_windows

## 5. Motor de ETA

- [ ] 5.1 Criar utils/haversine.py com função de cálculo de distância entre dois pontos (lat/lng)
- [ ] 5.2 Criar service de cálculo de ETA: distância / velocidade_média, retornando timedelta
- [ ] 5.3 Criar configuração de velocidades médias por tipo (urbana=40, rodovia=80)
- [ ] 5.4 Criar função de recálculo dinâmico considerando impact_factor e delay_minutes de eventos ativos

## 6. Gerenciamento de Entregas

- [ ] 6.1 Criar modelo Delivery (id, factory_id, store_id, driver_id, status, eta_original, eta_current, route_type, created_at, departed_at, delivered_at)
- [ ] 6.2 Criar schemas com DeliveryCreate, DeliveryResponse, DeliveryStatusUpdate
- [ ] 6.3 Criar enum DeliveryStatus (pendente, em_transito, entregue, cancelada) com validação de transição
- [ ] 6.4 Criar router.py com POST criar, GET listar (filtrado por role), GET detalhe, PATCH status
- [ ] 6.5 Criar service.py com lógica de criação (calcula ETA), listagem filtrada e transição de status
- [ ] 6.6 Integrar validação de janela de recebimento na criação e recálculo (flag dentro/fora_da_janela)
- [ ] 6.7 Gerar migração Alembic para tabela deliveries

## 7. Simulador de Caos

- [ ] 7.1 Criar modelo ChaosEvent (id, delivery_id FK, type enum, impact_factor, delay_minutes, created_at, is_active)
- [ ] 7.2 Criar schemas ChaosEventCreate, ChaosEventResponse, ChaosEventTypeInfo
- [ ] 7.3 Criar endpoint GET /chaos/event-types retornando catálogo dos 4 tipos
- [ ] 7.4 Criar endpoint POST /chaos/events para injetar evento (valida entrega em_transito, recalcula ETA)
- [ ] 7.5 Criar endpoint DELETE /chaos/events/{id} para remover evento (recalcula ETA)
- [ ] 7.6 Criar endpoint GET /chaos/events?delivery_id= para listar eventos ativos
- [ ] 7.7 Gerar migração Alembic para tabela chaos_events

## 8. Safe-Check

- [ ] 8.1 Criar modelo PositionUpdate (id, delivery_id, driver_id, lat, lng, speed, timestamp)
- [ ] 8.2 Criar modelo SafeCheckPing (id, delivery_id, driver_id, created_at, expires_at, status enum, response_reason)
- [ ] 8.3 Criar modelo Alert (id, delivery_id, driver_id, type, level, status, created_at, resolved_at, note)
- [ ] 8.4 Criar endpoint POST /safe-check/position para atualização de posição
- [ ] 8.5 Implementar lógica: se speed=0, criar ping com timer de 5 min
- [ ] 8.6 Criar endpoint POST /safe-check/ping/{id}/respond para resposta do motorista
- [ ] 8.7 Implementar detecção de desvio de rota (distância ponto-a-reta > 2 km → alerta CRÍTICO)
- [ ] 8.8 Criar endpoints GET /safe-check/alerts e PATCH /safe-check/alerts/{id} para operador
- [ ] 8.9 Gerar migração Alembic para tabelas position_updates, safe_check_pings, alerts

## 9. Endpoint de Demo

- [ ] 9.1 Criar endpoint POST /demo/simulate que orquestra fluxo completo
- [ ] 9.2 Implementar lógica: cria entrega temporária → calcula ETA → injeta caos (se solicitado) → recalcula → verifica janela → retorna JSON consolidado
- [ ] 9.3 Suporte a múltiplos tipos de caos com resultado parcial de cada etapa

## 10. Swagger UI e Finalização

- [ ] 10.1 Customizar Swagger UI com título, descrição, tags agrupadas por domínio e tema
- [ ] 10.2 Adicionar exemplos ricos em cada schema Pydantic (model_config com json_schema_extra)
- [ ] 10.3 Criar seed script para popular banco com dados de demonstração (fábricas, lojas, motoristas, janelas)
- [ ] 10.4 Testar fluxo completo via Swagger UI
- [ ] 10.5 Documentar README.md com instruções de setup, execução e uso
