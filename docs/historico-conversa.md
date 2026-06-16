# Histórico da Conversa — Antigravity

## Objetivo
Construir um motor analítico B2B de logística com rastreamento inteligente, SLA e injeção de Chaos Engineering (FastAPI + Next.js).

## Arquitetura
- Clean Architecture / DDD (entidades de domínio, use cases, protocolos de repositório, infraestrutura)
- Async Python (FastAPI, SQLAlchemy async, asyncpg)
- PostgreSQL em produção, SQLite in-memory para testes
- JWT + bcrypt com controle de role (lojista, motorista)
- Código em Português (BR) para mensagens ao usuário
- Testes determinísticos (sem dependência flaky de datetime)
- **Frontend:** Next.js App Router + TypeScript + TailwindCSS + shadcn/ui + Vitest

---

## Bloco 1 — Qualidade dos Testes
**Objetivo:** Eliminar flaky tests, remover duplicatas, fortalecer asserções.

**O que foi feito:**
- Corrigidos testes com dependência de `datetime.utcnow` (substituído por `unittest.mock.patch`)
- Removidos testes duplicados em `test_security.py`
- Adicionados 13 testes unitários com `AsyncMock` nos use cases
- Adicionados testes de validação de FK e boundaries (22 casos parametrizados)
- Padronizados helpers do `conftest.py` (fixtures para lojista, motorista, db_session, client)
- Total: 58 → 89 testes

---

## Bloco 2 — PATCH /deliveries/{id}
**Objetivo:** Endpoint de atualização de entrega (status + posição) com máquina de estados e recálculo de ETA.

**O que foi feito:**
- `DeliveryRepository.get_by_id()` e `update()`
- Máquina de estados (`VALID_TRANSITIONS`) com transições válidas
- Haversine para calcular distância e ETA
- `EtaHistoryRepository` para registrar histórico de recálculos
- `ChaosEngine` integrado (eventos de caos ativos afetam ETA)
- `current_lat` / `current_lng` persistidos na entidade Delivery
- `DEFAULT_SPEED_KMH` configurável em `settings`
- Datetimes com timezone (elimina 44 deprecation warnings do SQLAlchemy)
- 3 testes unitários + 3 testes de integração

### Refinamentos do Bloco 2
- Extraída lógica de recálculo de ETA para `_eta_recalculation.py` (helper compartilhado)
- `UpdateDeliveryUseCase` e `InjectChaosUseCase` agora usam `recalculate_delivery_eta()`
- Razões: `"posicao_atualizada"` e `"caos_injetado"`

---

## Bloco 3 — POST /deliveries/{id}/chaos
**Objetivo:** Endpoint de injeção de caos com criação automática de alerta se crítico.

**O que foi feito:**
- `ChaosInject` schema com `event_type`, `impact_factor`, `delay_minutes`, coordenadas opcionais
- `ChaosRepository.create()` + protocolo
- `AlertRepository` (protocolo + implementação SQLAlchemy)
- `InjectChaosUseCase` — valida entrega, cria evento, recalcula ETA, cria alerta se crítico
- `api/chaos.py` rota `POST /deliveries/{delivery_id}/chaos`
- Alertas críticos: `impact_factor > 2.0` ou `delay_minutes > 60` (thresholds configuráveis via `settings`)
- 5 testes unitários + 4 testes de integração

---

## Bloco 4 — GET /alerts
**Objetivo:** Listagem de alertas com filtro opcional por delivery_id e paginação.

**O que foi feito:**
- `AlertRepository.list_all()` com parâmetros `delivery_id`, `limit`, `offset`
- `ListAlertsUseCase` — lista alertas ordenados por `created_at DESC`
- `api/alerts.py` rota `GET /alerts`
- Qualquer usuário autenticado pode acessar
- 2 testes unitários + 4 testes de integração

---

## Bloco 5 — Dashboard GET /dashboard
**Objetivo:** Endpoint agregado com totais de entregas, alertas e caos.

**O que foi feito:**
- `DashboardResponse` com: `total_deliveries`, `deliveries_by_status`, `delayed_deliveries`, `total_alerts`, `critical_alerts`, `active_chaos_events`, `chaos_by_type`
- `DeliveryRepository.count_by_status()`, `count_delayed()`
- `ChaosRepository.count_by_type()`
- `AlertRepository.count_all(is_critical=)`
- `GetDashboardUseCase` com queries paralelizadas via `asyncio.gather`
- Schemas: `DeliveryStatusCount` (renomeado de `StatusCount`), `ChaosTypeCount`
- 1 teste unitário + 1 teste de integração

---

## Bloco 6 — Consistência Transacional
**Objetivo:** Corrigir bug onde `flush()`-only perdia dados em caso de erro posterior.

**O que foi feito:**
- `ChaosRepository.create()` e `AlertRepository.create()` alterados de `flush()` para `commit()` + `refresh()`
- Todos os 6 repositórios agora usam `commit()` consistentemente
- Evita que eventos de caos ou alertas sejam perdidos se uma transação maior falhar

---

## Bloco 7 — Documentação (REVERTIDO)
**Objetivo:** Adicionar docstrings em todas as camadas.

**O que foi feito e revertido:**
- Docstrings adicionadas em ~25 arquivos (domain, use cases, schemas, API, core)
- **Solicitado reversão** pelo usuário — Bloco 7 completamente removido
- Nenhuma lógica foi alterada, apenas comentários

---

## Bloco 8 — Backend Clean Arch Refinements
**Objetivo:** Refatorar value objects, protocols de repositório e imports para alinhamento com DDD puro.

**O que foi feito:**
- `Coordinates` como Value Object (dataclass imutável com `lat`, `lng`)
- Protocolos de repositório realocados para `domain/repositories/`
- Importes dos use cases ajustados para os novos paths
- Testes mantidos verdes

---

## Bloco 9 — Observabilidade e Exception Handling
**Objetivo:** Logging estruturado, correlação de requisições, tratamento global de erros e proteção de dados sensíveis.

**O que foi feito:**
- `ObservabilityMiddleware`: request ID (UUID4), timing, logging por requisição, header `X-Request-ID` na resposta
- `setup_logging()`: formato estruturado com timestamp, logger hierárquico (`antigravity.*`)
- `DataMaskingFilter`: mascara `password`, `token`, `secret` etc. nos logs via regex
- `DomainException` (base, 500), `EntityNotFoundException` (404), `InvalidCredentialsException` (401), `ConflictException` (409), `InvalidTransitionException` (422)
- 3 global exception handlers: `DomainException` (status dinâmico), `OperationalError` (503), `Exception` (500)
- Health endpoint: `GET /health`
- AuditListener ligado ao event bus para logging de criação/mudança de entregas

---

## Bloco 10 — Event Bus e Domain Events
**Objetivo:** Implementar barramento de eventos in-process para desacoplar efeitos colaterais (auditoria, cache).

**O que foi feito:**
- `DomainEvent` (base): `id` UUID + `occurred_at` automáticos
- `EventHandler` protocol: `async handle(event)`
- `EventBus`: subscribe / unsubscribe / publish com isolamento de falha por handler
- Eventos concretos: `DeliveryCreatedEvent`, `DeliveryStatusChangedEvent`
- `AuditListener`: loga criação e mudança de status
- `CacheInvalidationListener`: invalida cache Redis ao criar entrega
- Wiring no `main.py` via `event_bus.subscribe()`
- 8 testes (publicação, unsubscribe, múltiplos handlers, isolamento de falha)

---

## Bloco 11 — ETA Service (Camada de Domínio)
**Objetivo:** Extrair cálculo de ETA para serviço de domínio reutilizável.

**O que foi feito:**
- `app/domain/services/eta_service.py`: `calculate_eta_between_coordinates(origin, destination, speed_kmh)`
- Usa `Coordinates` e funções raw de `haversine.py`
- `CreateDeliveryUseCase` passou a usar o service
- 6 testes no `test_eta_service.py`

---

## Bloco 12 — Cache Distribuído (Redis + Cache-Aside)
**Objetivo:** Cachear listagens de entregas para reduzir carga no banco.

**O que foi feito:**
- `RedisClient`: singleton async via `redis.asyncio.Redis.from_url()`, com fallback graceful se Redis indisponível
- `CacheService`: `get_json/set_json`, `get/set` (Pydantic), `invalidate_prefix` (SCAN + DEL), TTL configurável
- Cache-Aside em `ListDeliveriesUseCase.execute()`: check cache → DB → populate cache
- `CacheInvalidationListener`: invalida prefixo `deliveries:list` ao criar entrega
- `fakeredis` para testes (47 + 62 linhas de teste)
- Serviço Redis no docker-compose (`redis:7-alpine`)
- **Pendência:** cache não injetado na rota de produção `GET /deliveries` (api/deliveries.py não passa `cache_service`)

---

## Bloco 13 — Frontend Clean Architecture
**Objetivo:** Implementar frontend com Next.js, Clean Architecture, shadcn/ui e Vitest.

**O que foi feito:**
- Next.js App Router + TypeScript + TailwindCSS + shadcn/ui
- **Domínio:** entidades (`User`, `Place`, `Delivery`, `Coordinates`), erros (`AppError`, `ValidationError`, `NetworkError`, `UnauthorizedError`, `InvalidCredentialsError`), protocolos de repositório (`AuthRepositoryProtocol`, `PlaceRepositoryProtocol`, `DeliveryRepositoryProtocol`)
- **Application:** `LoginUseCase`, `LogoutUseCase`, `CreateDeliveryUseCase`, `ListDeliveriesUseCase`, `CreateFactoryUseCase`, `CreateStoreUseCase`, `UpdateDeliveryUseCase` + factories DI
- **Infrastructure:** Axios client com Bearer token, repositórios (`ApiAuthRepository`, `ApiPlaceRepository`, `ApiDeliveryRepository`), `TokenStorageAdapter`, factory DI
- **Hooks:** `useAuth`, `useDeliveries`, `usePlaces`
- **Componentes:** `LoginForm`, `AuthGuard`; Dashboard (KanbanBoard, DeliveryDataTable, Sidebar, MetricCard, StatsFooter); Driver (DeliveryCard, ActiveDeliveryView, EtaDisplay, SafeCheckToggle, BottomNav); Control Tower (7 widgets, SimuladorCaos, AlertasCriticos)
- **Testes:** MSW configurado, testes de login flow, redirect por role, auth guard, hook useAuth, apiClient
- **Pendência:** `useDeliveries` e `usePlaces` sem testes unitários

---

## Bloco 14 — API Integration Validation
**Objetivo:** Scripts de seed e testes de integração E2E completos.

**O que foi feito:**
- `seed.py`: cria lojista, motorista, fábrica e loja
- `admin_seed.py`: cria admin `admin@antigravity.com`
- `test_integration.py` (418 linhas, 21 testes): auth, places, deliveries, chaos, alerts, dashboard
- `test_security.py` (66 linhas): role-based access, token expirado, token ausente
- `test_validation.py` (103 linhas): 22 casos parametrizados de validação 422
- Fixtures `conftest.py`: lojista, motorista, db_session, client, fakeredis, cache_service

---

## Bloco 15 — Rate Limiting (slowapi)
**Objetivo:** Proteger endpoints sensíveis contra abuso com limites de requisição.

**O que foi feito:**
- `slowapi>=0.1.9` adicionado ao `requirements.txt`
- `app/core/rate_limiter.py`: `Limiter` com `get_remote_address` (identificação por IP)
- Integrado no `main.py`: `app.state.limiter` + exception handler `RateLimitExceeded`
- `POST /auth/register` → 3 requisições/minuto
- `POST /auth/login` → 5 requisições/minuto
- `POST /deliveries/{id}/chaos` → 10 requisições/minuto
- `limiter.enabled = False` nos testes existentes (via `conftest.py`) para não quebrar a suite
- `limiter.reset()` para limpar storage entre testes de rate limiting
- 3 testes em `test_rate_limiting.py` validando 429 ao exceder cada limite

---

## Bloco 16 — Validação de Dono da Entrega
**Objetivo:** Restringir `PATCH /deliveries/{id}` para apenas o motorista responsável pela entrega.

**O que foi feito:**
- `ForbiddenException` (403) em `app/core/exceptions.py`
- `UpdateDeliveryUseCase.execute()` agora recebe `current_user_id` e valida contra `delivery.driver_id`
- Rota `PATCH /deliveries/{id}` extrai `current_user["id"]` e repassa ao use case
- Lojistas e motoristas não-donos recebem 403 com mensagem clara
- 142 testes backend (2 novos: lojista → 403, motorista errado → 403)
- Testes existentes ajustados para usar headers do motorista dono

---

## Bloco 17 — Refresh Token JWT
**Objetivo:** Implementar rotação de tokens com refresh token para renovação de sessão sem novo login.

**O que foi feito:**

### Backend
- `REFRESH_TOKEN_EXPIRE_DAYS: int = 30` em `app/core/config.py`
- `create_refresh_token()` e `decode_refresh_token()` em `app/core/security.py` (JWT com `type: "refresh"`)
- `RefreshTokenUseCase` — valida refresh token, busca usuário, retorna novo par access+refresh (rotação)
- `LoginUserUseCase` agora retorna `refresh_token` junto com `access_token`
- `POST /auth/refresh` em `app/api/auth.py`
- `get_by_id` adicionado ao `UserRepositoryProtocol` + implementação
- Decodificação rejeita access token usado como refresh (`type != "refresh"`)
- 3 testes de integração: refresh válido, refresh inválido (401), access token rejeitado como refresh

### Frontend
- `TokenStorageAdapter`: `getRefreshToken()`, `saveRefreshToken()`, `clearTokens()` (limpa ambos)
- `api_client.ts`: interceptor 401 → tenta refresh com `/auth/refresh` → em caso de sucesso, retry da request original; em caso de falha, redireciona ao login
- `AuthRepositoryProtocol`: login retorna `{ user, token, refresh_token }` + novo método `refreshToken()`
- `LoginUseCase`: persiste `refresh_token` no storage
- `LogoutUseCase`: usa `clearTokens()` em vez de `removeToken()`
- MSW handlers: mock de `/auth/refresh` com rotação

---

## Pendências

### Pendente 2 — Infraestrutura Real
**Situação:** Concluído ✅
- Migration `2a7f3c9e1d5d_add_current_lat_lng.py` criada em `backend/migrations/versions/`
- `backend/entrypoint.sh` — aguarda PostgreSQL, roda `alembic upgrade head`, executa CMD
- `backend/Dockerfile` atualizado com `ENTRYPOINT`
- `docker-compose.yml` com healthchecks (db, redis, api) + serviço `frontend` + `NEXT_PUBLIC_API_URL`
- CI/CD em `.github/workflows/ci.yml` (backend + frontend + docker build)

**Nota:** Testes não puderam ser validados por limitação de RAM da máquina (4GB RAM + 2GB Zram + 4GB swap). O pytest com coverage estourou a memória disponível.

### Pendente 3 — Segurança
**Situação:** Concluído ✅

> Processos em andamento são rastreados em `docs/processos-andamento.md`

### Pendente 4 — Robustez
**Situação:** Não iniciado
- Retry/lock para concorrência em atualizações simultâneas
- Idempotência no chaos injection (evitar duplicatas)

### Pendente 5 — Cache não injetado na produção
**Situação:** CacheService implementado e testado, mas a rota `GET /deliveries` em `api/deliveries.py` não passa `cache_service` ao `ListDeliveriesUseCase`

### Pendente 6 — Worker Queue Async
**Situação:** Não iniciado. Sem `arq`/`celery`/`rq` para processamento assíncrono em background.

### Pendente 7 — Housekeeping
- `remove_chaos_from_eta` é código morto (definido em `chaos.py`, só testado, sem rota/use case)
- Testes faltantes para `useDeliveries` e `usePlaces` no frontend
- `src/use_cases/getRouteByRole.ts` legado (poderia ser movido para constants ou router config)

### Pendente 8 — Linting Frontend (24 problemas: 16 erros, 8 warnings)
- **Erros (`@typescript-eslint/no-explicit-any`):**
  - `components/ui/dropdown-menu.tsx:27` (shadcn)
  - `hooks/useAuth.test.ts:22,29` (teste)
  - `infra/repositories/ApiDeliveryRepository.ts:5`
  - `mocks/handlers.ts:7,42` (MSW)
- **Warnings:**
  - `components/ui/avatar.tsx:17` — `<img>` sem `alt`, preferir `<Image>`
  - `components/ui/dialog.tsx:48` — `asChild` não usado
  - `hooks/usePlaces.ts:3` — `Factory`, `Store` importados não usados
  - `utils/jwt.ts:24` — `e` no catch não usado

---

## Estado Atual
- **145 testes backend**, 0 falhas, 8 warnings (timezone)
- **Cobertura total:** 96%
- **Cobertura por camada:** `app/use_cases/` 100%, `app/schemas/` 100%, `app/api/` 100%, `app/domain/` ~95%, `app/infrastructure/` ~88%
- **Frontend:** ~10 testes (Vitest), MSW para mock de API
- `remove_chaos_from_eta` é código morto (sem rota ou use case)

## Decisões-Chave
| Decisão | Motivo |
|---|---|
| `unittest.mock.patch` em vez de `monkeypatch` para `datetime.utcnow` | C-level built-in é imutável para monkeypatch |
| Datas em 2050 nos testes de caos | Garantir `remaining_time` determinístico |
| Qualquer user autenticado pode PATCH, POST chaos, GET alerts, GET dashboard | Simplicidade inicial; dono da entrega é Pendente 3 |
| Thresholds de caos em `settings` | Configurável sem alterar código |
| `commit()` + `refresh()` em todos os repositórios | Consistência transacional (Bloco 6) |
| Queries paralelas com `asyncio.gather` no dashboard | Performance |
| EventBus in-process com isolamento de falha por handler | Falha em listener não quebra o fluxo principal |
| Cache-Aside com invalidação por evento | Consistência eventual controlada |
| `ObservabilityMiddleware` + `DataMaskingFilter` | Rastreabilidade sem vazar PII |
| SQLite in-memory para testes (não PostgreSQL) | Velocidade e isolamento; mesmas queries (SQLAlchemy abstrai) |
| slowapi com `get_remote_address` | Rate limiting por IP; limites conservadores (3/min register, 5/min login, 10/min chaos) |

## Arquivos Relevantes

### Backend — Domínio
- `app/domain/entities/`: Delivery (máquina de estados), EtaHistory, ChaosEventLog, Alert, Factory, Store, User
- `app/domain/events.py`: `DeliveryCreatedEvent`, `DeliveryStatusChangedEvent`
- `app/domain/value_objects/coordinates.py`: `Coordinates` (dataclass imutável)
- `app/domain/services/eta_service.py`: `calculate_eta_between_coordinates()`
- `app/domain/haversine.py`, `app/domain/chaos.py`, `app/domain/safe_check.py`
- `app/domain/repositories/`: Protocolos para delivery, place, eta_history, chaos, alert, user

### Backend — Core
- `app/core/config.py` (Settings com REDIS_URL, CACHE_TTL_SECONDS, CHAOS_THRESHOLDS etc.)
- `app/core/security.py` (JWT + bcrypt)
- `app/core/exceptions.py`: `DomainException`, `EntityNotFoundException`, `InvalidCredentialsException`, `ConflictException`, `InvalidTransitionException`
- `app/core/logging.py`: `setup_logging()`, `DataMaskingFilter`
- `app/core/events/base.py`: `DomainEvent`, `EventHandler`
- `app/core/events/bus.py`: `EventBus` (singleton `event_bus`)
- `app/core/rate_limiter.py`: `Limiter` com `get_remote_address`

### Backend — Infraestrutura
- `app/infrastructure/repositories/`: Implementações SQLAlchemy (6 repositórios)
- `app/infrastructure/orm/`: Modelos SQLAlchemy
- `app/infrastructure/cache/redis_client.py`, `cache_service.py`
- `app/infrastructure/events/audit_listener.py`, `cache_invalidation_listener.py`

### Backend — Use Cases
- `app/use_cases/`: auth, deliveries, chaos, alert, dashboard + `_eta_recalculation.py`

### Backend — API
- `app/api/`: auth, places, deliveries, chaos, alerts, dashboard, deps, middleware
- `app/main.py`: FastAPI app com CORS, routers, exception handlers, event bus wiring, cache init

### Backend — Schemas
- `app/schemas/`: user, place, delivery, chaos, alert, dashboard

### Backend — Testes
- `tests/conftest.py`: Fixtures (lojista, motorista, db_session, client, fakeredis, cache_service)
- `tests/unit/test_use_cases.py`: 24 testes
- `tests/unit/test_event_bus.py`: 8 testes
- `tests/unit/test_cache_service.py`: testes de cache
- `tests/unit/test_list_deliveries_cache.py`: testes de cache-aside
- `tests/api/test_integration.py`: 21 testes E2E
- `tests/api/test_security.py`: 6 testes
- `tests/api/test_validation.py`: ~22 casos parametrizados
- `tests/domain/`: test_simulation.py, test_engine.py, test_extreme.py, test_eta_service.py
- `tests/api/test_rate_limiting.py`: 3 testes de rate limiting (429 após exceder limite)

### Frontend
- `src/domain/entities/`: Entity, User, Place, Delivery
- `src/domain/errors/`: AppError, ValidationError, NetworkError, UnauthorizedError, InvalidCredentialsError
- `src/domain/repositories/`: AuthRepositoryProtocol, PlaceRepositoryProtocol, DeliveryRepositoryProtocol
- `src/domain/value_objects/coordinates.ts`
- `src/application/use_cases/`: LoginUseCase, LogoutUseCase, CreateDeliveryUseCase, ListDeliveriesUseCase, CreateFactoryUseCase, CreateStoreUseCase, UpdateDeliveryUseCase
- `src/infrastructure/api/api_client.ts`, `repositories/`, `storage/TokenStorageAdapter.ts`, `di/factories.ts`
- `src/hooks/`: useAuth, useDeliveries, usePlaces
- `src/components/`: LoginForm, AuthGuard, dashboard/, driver/, control-tower/, chaos/, ui/ (shadcn)
- `src/app/`: page.tsx (login), dashboard/, drive/, control-tower/
- `__tests__/`: login.test.tsx, unit/, integration/ (login_flow, motorista_redirect, auth_guard)
