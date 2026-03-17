## 1. Setup do Projeto (Monorepo & Docker)

- [ ] 1.1 Criar estrutura de pastas root: `backend/` e `frontend/`
- [ ] 1.2 Criar arquivo `docker-compose.yml` na raiz mapeando os serviços `db` (postgres:15-alpine), `backend` e `frontend`.
- [ ] 1.3 No `backend/`: Inicializar projeto Python com pyproject.toml, dependências (fastapi, uvicorn, sqlalchemy, asyncpg, pydantic, python-jose, passlib, alembic)
- [ ] 1.4 Criar `Dockerfile` do backend para desenvolvimento local.
- [ ] 1.5 Criar estrutura de diretórios do backend (app/core, app/auth, app/deliveries, app/chaos, app/safe_check, app/locations, app/demo)
- [ ] 1.6 Configurar core/config.py com settings via Pydantic BaseSettings (DATABASE_URL, SECRET_KEY, etc.)
- [ ] 1.7 Configurar core/database.py com engine async + sessionmaker + Base declarative (TIMESTAMP WITH TIME ZONE)
- [ ] 1.8 Configurar core/pagination.py com dependency reutilizável (limit default=20, offset default=0)
- [ ] 1.9 Configurar Alembic para migrações async com PostgreSQL
- [ ] 1.10 Criar app/main.py com FastAPI app, CORS, inclusão de routers e metadata para Swagger customizado

## 2. Autenticação Multi-Role

- [ ] 2.1 Criar models.py com modelo User (id, email, hashed_password, role, created_at UTC)
- [ ] 2.2 Criar schemas.py com UserCreate, UserLogin, UserResponse, TokenResponse (Pydantic V2)
- [ ] 2.3 Criar core/security.py com hash de senha (passlib/bcrypt), criação e validação de JWT, dependency get_current_user
- [ ] 2.4 Criar dependencies de role: require_operador, require_lojista, require_motorista
- [ ] 2.5 Criar router.py com POST /auth/register e POST /auth/login
- [ ] 2.6 Criar service.py com lógica de registro e autenticação
- [ ] 2.7 Gerar migração Alembic para tabela users

## 3. Locations (Fábricas e Lojas)

- [ ] 3.1 Criar models.py com Factory (id, name, lat, lng) e Store (id, name, lat, lng, owner_id FK→User)
- [ ] 3.2 Criar schemas.py com CRUD schemas restritos (Pydantic V2)
- [ ] 3.3 Criar router.py com CRUD endpoints e paginação (limit/offset)
- [ ] 3.4 Criar service.py com lógica de CRUD
- [ ] 3.5 Gerar migração Alembic para tabelas factories e stores

## 4. Janela de Recebimento

- [ ] 4.1 Criar modelo ReceivingWindow (id, store_id FK, day_of_week, start_time UTC, end_time UTC)
- [ ] 4.2 Criar schemas para configuração de janela
- [ ] 4.3 Criar endpoints POST/GET/PUT/DELETE em /stores/{id}/receiving-window
- [ ] 4.4 Criar função de validação de horário UTC
- [ ] 4.5 Gerar migração Alembic para tabela receiving_windows

## 5. Motor de ETA

- [ ] 5.1 Criar utils/haversine.py com cálculo de distância (lat/lng)
- [ ] 5.2 Criar service de cálculo de ETA: distância / velocidade_média
- [ ] 5.3 Criar função de recálculo dinâmico (impact_factor e delay_minutes)

## 6. Gerenciamento de Entregas

- [ ] 6.1 Criar modelo Delivery (id, factory_id, store_id, driver_id, status, eta_original, eta_current, route_type, created_at, departed_at, delivered_at)
- [ ] 6.2 Criar schemas Pydantic V2
- [ ] 6.3 Criar router.py com operações CRUD restritas
- [ ] 6.4 Integrar validação de janela de recebimento na criação
- [ ] 6.5 Gerar migração Alembic para tabela deliveries

## 7. Reroute pelo Motorista

- [ ] 7.1 Criar endpoint POST /deliveries/{id}/reroute (lat/lng)
- [ ] 7.2 Implementar lógica: calcular nova distância via Haversine, aplicar eventos ativos

## 8. Histórico de ETA

- [ ] 8.1 Criar modelo EtaHistory (id, delivery_id FK, eta_before, eta_after, reason, timestamp UTC)
- [ ] 8.2 Integrar registro em: injeção de caos, remoção de caos e reroute
- [ ] 8.3 Criar endpoint GET /deliveries/{id}/eta-history
- [ ] 8.4 Gerar migração Alembic para tabela eta_history

## 9. Simulador de Caos

- [ ] 9.1 Criar modelo ChaosEvent (id, delivery_id FK, type enum, impact_factor, delay_minutes, created_at, is_active)
- [ ] 9.2 Criar schemas ChaosEventCreate, ChaosEventResponse, ChaosEventTypeInfo
- [ ] 9.3 Criar endpoints para injetar/remover evento e recalcular ETA
- [ ] 9.4 Gerar migração Alembic

## 10. Log de Caos para ML

- [ ] 10.1 Criar modelo ChaosEventLog (id, delivery_id, event_type, impact_factor, delay_minutes, lat_start, lng_start, lat_end, lng_end, timestamp)
- [ ] 10.2 Integrar criação/finalização automática no fluxo de Caos
- [ ] 10.3 Gerar migração Alembic para tabela chaos_event_log

## 11. Safe-Check com Lazy Evaluation

- [ ] 11.1 Criar modelos PositionUpdate, SafeCheckPing e Alert
- [ ] 11.2 Criar endpoint POST /safe-check/position e lógica de ping (5 min expirado)
- [ ] 11.3 Implementar lazy evaluation na leitura dos alertas
- [ ] 11.4 Implementar detecção de desvio de rota (> 2 km)
- [ ] 11.5 Gerar migração Alembic

## 12. Frontend (Next.js MVP)

- [ ] 12.1 No `frontend/`: Inicializar Next.js App Router com TypeScript, Tailwind CSS
- [ ] 12.2 Criar `Dockerfile` do frontend para desenvolvimento local.
- [ ] 12.3 Configurar shadcn/ui base (`npx shadcn-ui@latest init` em non-interactive)
- [ ] 12.4 Criar lib de chamadas API usando fetch (conectando no backend FastAPI)
- [ ] 12.5 Instalar componentes shadcn/ui úteis (button, card, table, dialog, alert)
- [ ] 12.6 Criar Tela 1: **Painel do Operador** (Tabela de entregas em andamento, botão para Injetar Caos/Eventos, lista de Alertas Safe-Check)
- [ ] 12.7 Criar Tela 2: **Visão do Motorista** (Botão gigante de "Informar Reroute" e "Atualizar Posição" para testes de pings)
- [ ] 12.8 Ajustar CORS no backend para permitir conexão local do Next (geralmente localhost:3000)

## 13. Endpoint de Demo e Finalização

- [ ] 13.1 Criar endpoint POST /demo/simulate que orquestra fluxo completo no backend
- [ ] 13.2 Adicionar seed script para popular banco com dados de teste
- [ ] 13.3 Testar a orquestração subindo todo o ambiente com `docker-compose up -d --build`
- [ ] 13.4 Documentar README.md no root do monorepo com instruções de rodar backend+frontend via Docker
