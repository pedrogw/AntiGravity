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
- `UpdateDeliveryUseCase` e `InjectChaosUseCase` usam `recalculate_delivery_eta()` via sync fallback; com Redis disponível, enfileiram `EtaRecalculationRequested` no worker ARQ
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
**Situação:** Concluído ✅
- Idempotência no chaos injection via header `Idempotency-Key`
- Nova tabela `idempotency_keys` (key PK, response JSON, created_at)
- `IdempotencyRepository` (protocolo + SQLAlchemy) com TTL de 24h
- `InjectChaosUseCase` verifica key antes de criar evento; se cache hit, retorna response original sem efeito colateral
- 2 testes unitários (cache hit, cache miss + save) + 1 teste de integração (mesma key → mesmo chaos_event_id)
- 164 testes, 0 falhas, 97% cobertura total

**Por que não fizemos optimistic lock:**
- Lost update em PATCH é raro (cada motorista atualiza a própria entrega)
- Idempotency Key tem impacto real imediato (duplicata de caos corrompe ETA)
- Lock otimista pode vir depois se houver evidência de contenção

### Pendente 5 — Cache não injetado na produção
**Situação:** Concluído ✅
- `app.state.cache_service` setado no lifespan de `main.py`
- Rota `GET /deliveries` injeta `cache_service` via `getattr(request.app.state, "cache_service", None)`
- Fallback seguro: se Redis caiu, `cache_service` é `None` → fallback para DB direto
- `CacheInvalidationListener` continua funcionando (já estava wireado)
- 164 testes, 0 falhas — nenhum teste precisou ser alterado

---

### 🔙 Backend

#### Pendente 6 — Worker Queue Async
**Situação:** Fase 1 (event handlers) ✅ + Fase 2 (ETA recalc) ✅ + Fase 3 (alert creation) ✅
- Fase 1: `arq` + `app/infrastructure/worker.py` + EventBus enqueue + worker em docker-compose
- Fase 2: `EtaRecalculationRequested` + `handle_eta_recalculation()` com DB session + sync fallback
- Fase 3: `AlertCreationRequested(delivery_id, message, is_critical)` + `handle_alert_creation()` no worker; decisão `is_critical` inline (pure domain), apenas persistência no worker
- **202 testes, 0 falhas, 99% cobertura**
- **P6 completo ✅**

#### Pendente 8 — Cobertura de Infraestrutura Real (<80%)
**Situação:** Concluído ✅
- Todos os 6 arquivos-alvo agora estão em **100%**:
  - `main.py` (69% → **100%**) — lifespan success/failure, 3 exception handlers, health check
  - `bootstrap.py` (67% → **100%**) — `get_db` generator, `dispose_engine`
  - `redis_client.py` (50% → **100%**) — ambos branches de `get_redis` e `close_redis`
  - `cache_invalidation_listener.py` (62% → **100%**) — `handle` com `DeliveryCreatedEvent` e `DeliveryStatusChangedEvent`
  - `worker.py` (73% → **100%**) — cache invalidation com redis, `handle_alert_creation`, `handle_eta_recalculation` (found + not-found)
  - `audit_listener.py` (já 100%)
- **20 novos testes, 0 alterações em arquivos de produção**
- Técnica: mocks de infraestrutura externa (Redis, engine, sessão DB), testagem direta de handlers (sem TestClient), reset de estado module-level
- Cobertura total: **99%**

#### Migration `idempotency_keys`
**Situação:** Concluído ✅
- `app/db/base.py` agora importa `IdempotencyKey` — Alembic detecta a tabela para auto-generate
- Migration `05147e3ad5de_add_idempotency_keys.py` criada em `migrations/versions_pedro/` (diretório writable pelo pedro)
- `alembic.ini` atualizado com `version_locations = migrations/versions/:migrations/versions_pedro/` (separador `:` no Linux)
- `upgrade()` → `alembic upgrade head`: aplica todas as migrações + cria `idempotency_keys`
- `downgrade()` → `alembic downgrade base`: remove todas as tabelas
- **202 testes, 0 falhas, 99% cobertura**
- **Problema de root-owned resolvido estruturalmente** — novas migrations vão para `versions_pedro/`

---

### 🔙 Frontend

#### Pendente 7 — Housekeeping
- Testes faltantes para `useDeliveries` e `usePlaces` no frontend
- `src/use_cases/getRouteByRole.ts` legado (poderia ser movido para constants ou router config)

#### Pendente 9 — Linting Frontend (24 problemas: 16 erros, 8 warnings)
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

## Bloco 18 — Domínio Rico (Fase D.1: Coordinates)
**Objetivo:** Eliminar anemic domain começando pelos Value Objects.

**O que foi feito:**
- `Coordinates.__post_init__()` — valida bounds inclusivos (`-90≤lat≤90`, `-180≤lng≤180`)
- `Coordinates.distance_to(other)` — delega ao Haversine (lazy import para evitar circular import)
- Duplicata de validação removida de `haversine.py:7-10` (agora redundante)
- **145 testes, 0 falhas, 96% cobertura** — mantido
- Cobertura de `coordinates.py`: 85% (linhas 17-18 do `distance_to` sem chamada direta nos testes)

## Bloco 19 — Domínio Rico (Fase D.2: User)
**Objetivo:** Tipar `role` com `UserRole` enum e adicionar métodos de consulta.

**O que foi feito:**
- `User.role: str` → `User.role: UserRole` (aproveita enum existente que era ignorado)
- `User.is_motorista() -> bool` e `User.is_lojista() -> bool`
- `UserRole` duplicado removido de `infrastructure/orm/user.py` — agora importa do domínio
- `RegisterUserUseCase.role: str` → `RegisterUserUseCase.role: UserRole`
- `security.py`: type hints aceitam `Union[str, UserRole]`
- `user_repo.py`: conversão explícita `UserRole(model.role)` no reconstrutor
- `seed.py` e `admin_seed.py`: imports corrigidos, `.value` removidos
- `api/auth.py`: `.value` removido (use case já aceita `UserRole`)
- **145 testes, 0 falhas, 96% cobertura** — mantido
- Cobertura `user.py`: 89% (linhas 21,24 — `is_motorista`/`is_lojista` sem chamada direta)

## Bloco 20 — Domínio Rico (Fase D.3: Alert)
**Objetivo:** Encapsular lógica de criticalidade em factory method na entidade.

**O que foi feito:**
- `Alert.critical(delivery_id, message, impact_factor, delay_minutes, factor_threshold, delay_threshold)` — factory `@classmethod` que calcula `is_critical` internamente
- Thresholds continuam no `config.py` e são passados como parâmetros (entity testável sem depender de settings)
- `InjectChaosUseCase` refatorado: montagem da mensagem preservada, criação do alerta delegada ao factory, persistência condicional a `alert.is_critical`
- **145 testes, 0 falhas** — NENHUM teste precisou ser alterado
- `alert.py`: **100% cobertura**, `chaos_use_cases.py`: **100% cobertura**

## Bloco 21 — Domínio Rico (Fase D.4a: Delivery.change_status)
**Objetivo:** Encapsular máquina de estados na entidade Delivery.

**O que foi feito:**
- `VALID_TRANSITIONS` movido de constante de módulo para `ClassVar` dentro de `Delivery`
- `Delivery.change_status(new_status)` — valida transição, seta `status` e `departed_at` automaticamente
- `ClassVar` usado para evitar que vire campo de instância (preserva `DeliveryEntity(**item)` no cache)
- `UpdateDeliveryUseCase` refatorado: 7 linhas de validação inline substituídas por `delivery.change_status(status)`
- Import morto de `InvalidTransitionException` e `datetime` removidos do use case
- **145 testes, 0 falhas** — NENHUM teste precisou ser alterado
- `delivery.py`: **100% cobertura**, `deliveries_use_cases.py`: **100% cobertura**

## Bloco 22 — Domínio Rico (Fase D.4b: Delivery.update_position)
**Objetivo:** Encapsular atualização de posição na entidade.

**O que foi feito:**
- `Delivery.update_position(lat, lng)` — método que seta `current_lat` e `current_lng`
- `UpdateDeliveryUseCase` refatorado: `delivery.current_lat = lat; delivery.current_lng = lng` → `delivery.update_position(lat, lng)`
- **145 testes, 0 falhas** — NENHUM teste alterado
- `delivery.py`: **100% cobertura**, `deliveries_use_cases.py`: **100% cobertura**

## Estado Atual
- **164 testes backend**, 0 falhas, 8 warnings (cache deprecated)
- **Cobertura total:** 97%
- **Domínio (entities, VOs, services, haversine, safe_check, chaos): 100%**
- **Use cases:** ~99%, **Schemas:** 100%, **API:** 100%
- **Infraestrutura:** ~89% (pendentes <80% listados abaixo)
- **Frontend:** ~10 testes (Vitest), MSW para mock de API
- **Entidades com comportamento:** `Coordinates`, `User`, `Alert`, `Delivery` (todos os 4 métodos), `ChaosEventLog` (aggregate)
- **Fase D (Domínio Rico): 9/9 tarefas concluídas ✅**
- **P4 (Robustez): Concluído ✅** — Idempotency Key no chaos injection
- **P5 (Cache produção): Concluído ✅** — Cache injetado via `app.state`

## Bloco 23 — Domínio Rico (Fases D.4c, D.4d, D.2t)
**Objetivo:** Completar migração de comportamento anêmico para domínio rico em Delivery e eliminar dead code.

**O que foi feito:**

### D.4c — Delivery.apply_chaos()
- `@staticmethod apply_chaos(current_eta, impact_factor, delay_minutes)` movido de `domain/chaos.py` para `Delivery`
- `Delivery.apply_chaos` usado em `_eta_recalculation.py` e `test_simulation.py`
- `chaos.py:apply_chaos_to_eta` virou delegate (depois removido)

### D.4d — Delivery.recalculate_eta()
- `Delivery.recalculate_eta(origin, store_location, speed_kmh, chaos_events, reason)` → retorna `EtaHistory | None`
- Método puro: recebe `Coordinates`, calcula distância via `origin.distance_to()`, ETA via Haversine, agrega caos, seta `eta_current`/`eta_original`
- `_eta_recalculation.py` reduzido de 55 para 15 linhas (orquestrador thin: busca store+chaos, delega ao entity, persiste history)
- 9 testes de domínio puros (sem async, sem DB)

### D.2t — Testes User
- `test_user_entity.py`: 2 testes para `is_motorista()` / `is_lojista()` — `user.py` 100%

### Cleanup
- `chaos.py`: removido `apply_chaos_to_eta` (dead code); só resta `remove_chaos_from_eta`
- **156 testes, 0 falhas, 96% cobertura total**
- **Domínio inteiro em 100%** (entities, VOs, services, haversine, safe_check, chaos)

---

## Bloco 24 — Domínio Rico (Fase D.5: ChaosEventLog.aggregate)
**Objetivo:** Encapsular lógica de agregação de eventos de caos na entidade.

**O que foi feito:**
- `ChaosAggregate` dataclass com `total_impact_factor`, `total_delay_minutes`, `event_count`, `count_by_type`
- `ChaosEventLog.aggregate(events)` — `@staticmethod` que calcula fator total (produto), atraso total (soma), contagem por tipo
- `Delivery.recalculate_eta()` refatorado: loop inline de 6 linhas substituído por `ChaosEventLog.aggregate(chaos_events)` (lazy import)
- `test_delivery_entity.py`: `FakeChaos` removido, testes usam `ChaosEventLog` real
- `test_chaos_entity.py`: 5 testes para aggregate (lista vazia, único, múltiplos, defaults, fator 1.0)
- **161 testes, 0 falhas, 96% cobertura total**
- **Fase D completa (9/9 tarefas)**

---

## Bloco 25 — Robustez (P4: Idempotency Key no Chaos Injection)
**Objetivo:** Evitar duplicatas de eventos de caos em caso de retry de rede ou duplo clique.

**O que foi feito:**
- `IDEMPOTENCY_KEY_TTL_HOURS = 24` em `config.py`
- `IdempotencyKey` ORM model (`idempotency_keys` tabela com key PK, response JSON, created_at)
- `IdempotencyRepositoryProtocol` no domínio
- `IdempotencyRepository` SQLAlchemy com `get()` e `save()` — serializa `ChaosEventLogEntity` para JSON, TTL check no retrieve
- `InjectChaosUseCase`: se `idempotency_key` fornecida e cache hit → retorna cached sem side effects; se cache miss → executa e salva
- Header `Idempotency-Key` opcional em `POST /deliveries/{id}/chaos`
- 2 testes unitários (hit + miss) + 1 teste de integração (mesma key → mesmo id)
- `chaos_use_cases.py`: **100% cobertura**, `idempotency_repo.py`: **96%** (1 miss: TTL cutoff)
- **164 testes, 0 falhas, 97% cobertura total**

---

## Bloco 26 — Cache injetado na produção (P5)
**Objetivo:** Completar o wiring do cache-aside em `GET /deliveries` para produção.

**O que foi feito:**
- `main.py`: `app.state.cache_service = cache_service` dentro do `try` do lifespan (após criar `CacheService(redis)`)
- `api/deliveries.py`: rota `list_deliveries` agora aceita `request: Request` e obtém `cache = getattr(request.app.state, "cache_service", None)`
- `ListDeliveriesUseCase` recebe `cache_service=cache` — quando `None` (Redis caiu), fallback para `repo.list_all()`
- Nenhum teste precisou ser alterado — em testes o lifespan não conecta Redis, `cache_service` fica `None`, fluxo cai para DB
- **164 testes, 0 falhas**

---

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
| Validação de bounds em `Coordinates.__post_init__` (inclusiva `<=`) | Defense-in-depth; Pydantic valida na API, VO valida em qualquer caminho interno |
| Lazy import (`from app.domain.haversine import ...` dentro do método) | Evita circular import entre `Coordinates` e `haversine` |
| `User.role: UserRole` em vez de `str` | Aproveita enum já existente; `UserRole(str, Enum)` é compatível com JSON e str |
| `UserRole` removido do ORM, importado do domain | Elimina duplicata; único ponto de verdade para o enum |
| `Alert.critical()` factory method | Encapsula regra de criticalidade na entidade; thresholds passados como parâmetro p/ manter testabilidade sem depender de `settings` |
| `VALID_TRANSITIONS` como `ClassVar` dentro de `Delivery` | `ClassVar` impede dataclass de tratá-lo como campo; `DeliveryEntity(**item)` do cache continua funcionando |
| `Delivery.change_status()` no domínio | Validação de transição e set de `departed_at` encapsulados; use case vira orquestrador simples |
| `Delivery.update_position()` no domínio | Método simples, mas prepara o terreno para validação futura de coordenadas na entidade |
| `Delivery.apply_chaos()` como `@staticmethod` | Lógica pura independente de estado da instância; pode ser chamada de `_eta_recalculation.py` sem precisar construir Delivery |
| `Delivery.recalculate_eta()` no domínio | Método puro que recebe VOs e retorna `EtaHistory`; use case vira orquestrador I/O |
| Lazy import de `calculate_eta` dentro de `recalculate_eta` | Consistente com padrão já usado em `Coordinates.distance_to()`; evita import circular |
| `from __future__ import annotations` em `delivery.py` | Necessário para forward reference de `EtaHistory` (definida após `Delivery` no mesmo módulo) |
| Remoção de `apply_chaos_to_eta` de `chaos.py` | Dead code: todos os call-sites migrados para `Delivery.apply_chaos()` |
| `ChaosEventLog.aggregate()` como `@staticmethod` | Lógica de agregação (produto de fatores, soma de delays, contagem por tipo) encapsulada na entidade; `Delivery.recalculate_eta()` consome via lazy import |
| `ChaosAggregate` como dataclass separado | Objeto de retorno rico que pode ser usado por dashboards e outros consumidores futuros |
| `Idempotency-Key` header em vez de uniqueness constraint na tabela chaos | Header é padrão REST (Stripe, etc.); não acopla idempotência ao schema de domínio; tabela separada `idempotency_keys` |
| `IdempotencyRepository` opcional no use case (`None` por padrão) | Backward compatibility: testes existentes não precisam passar o repo; só ativado quando header é enviado |
| TTL de 24h com verificação no `get()` | Evita acúmulo infinito de keys sem precisar de job de cleanup; cutoff é verificado no retrieve |
| JSON serialization da resposta em vez de FK para `chaoseventlog` | `ChaosRepository` não tem `get_by_id`; serializar evita acoplar repositórios; resposta pode ser reconstruída sem consulta adicional |
| Cache injetado via `app.state` em vez de `Depends()` | `CacheService` é criado no lifespan (após conectar Redis); `app.state` é o mecanismo padrão do FastAPI para compartilhar instâncias entre lifespan e rotas; `getattr` com fallback seguro se Redis caiu |

## Arquivos Relevantes

### Backend — Domínio
- `app/domain/entities/alert.py`: `Alert` (com `critical()` factory method)
- `app/domain/entities/user.py`: `User` (com `is_motorista()`/`is_lojista()`, `role: UserRole`)
- `app/domain/entities/delivery.py`: `Delivery` (com `change_status()` + `update_position()` + `apply_chaos()` + `recalculate_eta()`, máquina de estados como `ClassVar`), `EtaHistory`
- `app/domain/entities/chaos.py`: `ChaosEventLog` (com `aggregate()` estático), `ChaosAggregate`
- `app/domain/entities/place.py`: `Factory`, `Store`
- `app/domain/events.py`: `DeliveryCreatedEvent`, `DeliveryStatusChangedEvent`
- `app/domain/value_objects/coordinates.py`: `Coordinates` (VO imutável com `__post_init__` valida bounds + `distance_to()`)
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
- `app/infrastructure/repositories/`: Implementações SQLAlchemy (7 repositórios, incluindo `idempotency_repo.py`)
- `app/infrastructure/orm/`: Modelos SQLAlchemy (incluindo `idempotency_key.py`)
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
- `tests/unit/test_use_cases.py`: 28 testes
- `tests/unit/test_event_bus.py`: 8 testes
- `tests/unit/test_worker.py`: 13 testes
- `tests/unit/test_cache_service.py`: testes de cache
- `tests/unit/test_list_deliveries_cache.py`: testes de cache-aside
- `tests/api/test_integration.py`: 21 testes E2E
- `tests/api/test_security.py`: 6 testes
- `tests/api/test_validation.py`: ~22 casos parametrizados
- `tests/domain/`: test_simulation.py, test_engine.py, test_extreme.py, test_eta_service.py, test_delivery_entity.py, test_chaos_entity.py, test_user_entity.py
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

---

## Bloco 22 — P6 Fase 2: ETA Recalculation em Background
**Objetivo:** Mover recálculo de ETA do request-response para worker ARQ, com sync fallback para testes.

**O que foi feito:**
- `app/domain/events.py`: novo `EtaRecalculationRequested(delivery_id, lat, lng, reason)`
- `app/infrastructure/worker.py`: `handle_eta_recalculation()` — cria DB session, busca delivery+store+chaos, chama `recalculate_delivery_eta()`, persiste `EtaHistory` + `Delivery.eta_current`
- `app/use_cases/deliveries_use_cases.py`: `UpdateDeliveryUseCase` aceita `event_bus`; condiciona recálculo (enfileira se `worker_pool` setado, senão inline)
- `app/use_cases/chaos_use_cases.py`: `InjectChaosUseCase` aceita `event_bus`; mesma lógica condicional
- `app/api/deliveries.py` e `app/api/chaos.py`: passam `event_bus` para os use cases
- `WorkerSettings.functions` atualizado para incluir `handle_eta_recalculation`

**Testes:**
- 3 novos testes: serialização `EtaRecalculationRequested`, dispatch no worker para ETA recalc, async path no use case
- 11 testes unitários alterados: adicionado `event_bus=None` aos construtores
- **178 testes, 0 falhas, 96% cobertura**
- `chaos_use_cases.py`: 100%, `deliveries_use_cases.py`: 100%, `events.py`: 100%

**Riscos mitigados:**
- Concorrência: eventos carregam lat/lng no momento da criação, ordem de execução não importa
- DB leak: `async with AsyncSessionLocal()` garante cleanup
- Sync fallback: sem Redis, comportamento idêntico ao anterior

---

## Bloco 23 — P6 Fase 3: Alert Creation em Background
**Objetivo:** Mover persistência de alertas críticos do request-response para worker ARQ, mantendo decisão `is_critical` inline.

**O que foi feito:**
- `app/domain/events.py`: novo `AlertCreationRequested(delivery_id, message, is_critical)`
- `app/infrastructure/worker.py`: `handle_alert_creation()` — cria DB session, instancia `Alert`, persiste via `AlertRepository`
- `app/use_cases/chaos_use_cases.py`: bloco de alerta condiciona:
  - Decisão `is_critical` continua inline (pure domain, sem I/O)
  - `worker_pool` setado → enfileira `AlertCreationRequested`
  - `worker_pool` None → `alert_repo.create()` sync fallback
- `WorkerSettings.functions` inclui `handle_alert_creation`

**Testes:**
- 2 novos testes: roundtrip serialização `AlertCreationRequested`, dispatch no worker, async path no use case
- **0 alterações em testes existentes** — sync fallback preserva comportamento
- **180 testes, 0 falhas, 95% cobertura**

**Riscos mitigados:**
- Duplicata de alerta prevenida por idempotency key no chaos injection
- DB leak: `async with AsyncSessionLocal()` garante cleanup
- Eventual consistency aceitável para alertas

---

## Bloco 24 — P8: Cobertura de Infraestrutura (≥80%)
**Objetivo:** Elevar cobertura dos 6 arquivos de infraestrutura para ≥80% sem alterar código de produção.

**Contexto:** 5 arquivos usavam conectores reais (DB, Redis, FastAPI) e eram substituídos por mocks nos testes, deixando branches sem cobertura. `audit_listener.py` já estava em 100%.

**O que foi feito (20 novos testes, 0 alterações em produção):**

### `tests/unit/test_redis_client.py` (4 testes)
- `get_redis()` quando `_redis is None` → cria `AsyncRedis.from_url()`
- `get_redis()` quando `_redis` já setado → retorna instância existente
- `close_redis()` quando `_redis is not None` → fecha e reseta para `None`
- `close_redis()` quando `_redis is None` → no-op

### `tests/unit/test_bootstrap.py` (2 testes)
- `dispose_engine()` → mock `engine` completo (slot-based), verifica `dispose()`
- `get_db()` → mock `AsyncSessionLocal` como async context manager, verifica yield + cleanup

### `tests/unit/test_cache_invalidation_listener.py` (2 testes)
- `handle(DeliveryCreatedEvent)` → `invalidate_prefix` chamado com `CACHE_PREFIX`
- `handle(DeliveryStatusChangedEvent)` → `invalidate_prefix` não chamado

### `tests/unit/test_main.py` (6 testes)
- `lifespan` success path → Redis pinga, ARQ pool criado, `CacheService` em `app.state`, `event_bus.worker_pool` setado; cleanup fecha pool
- `lifespan` failure path → `get_redis()` lança exceção, log "Redis indisponível"
- `domain_exception_handler` → retorna `JSONResponse` com status 400 e detail
- `db_connection_exception_handler` → retorna 503 com "Database Unavailable"
- `unhandled_exception_handler` → retorna 500 com "Erro interno do servidor"
- `health_check` → retorna `{"status": "ok", "environment": "dev"}`

### `tests/unit/test_worker.py` (6 testes novos)
- Cache invalidation com `{"redis": mock}` no ctx → `CacheInvalidationListener.handle` chamado
- Cache invalidation sem redis no ctx → handler não chamado
- Cache invalidation com falha → log "Cache invalidation failed in worker"
- `handle_alert_creation` → `AlertRepository.create` chamado com `AlertEntity` correto
- `handle_eta_recalculation` delivery not found → log warning
- `handle_eta_recalculation` delivery found → `recalculate_delivery_eta` + `update` chamados

**Resultado final:** **200 testes, 0 falhas, 99% cobertura total.** Todos os 6 arquivos em 100%.

---

## Bloco 25 — Migration `idempotency_keys`
**Objetivo:** Gerar migration física para a tabela `idempotency_keys` e corrigir bloqueio de diretório root-owned.

**Causa raiz:**
- `app/db/base.py` não importava `IdempotencyKey` — Alembic não detectava a tabela para `--autogenerate`
- `migrations/versions/` era root-owned — impossível criar migrações novas

**O que foi feito:**

### `app/db/base.py`
- Adicionado `from app.infrastructure.orm.idempotency_key import IdempotencyKey`
- Agora todos os 7 modelos ORM estão centralizados (User, Factory, Store, Delivery, EtaHistory, ChaosEventLog, Alert, IdempotencyKey)

### `alembic.ini`
- `version_locations = migrations/versions/:migrations/versions_pedro/`
- `versions_pedro/` é writable pelo `pedro` — novas migrations vão para lá

### Migration `05147e3ad5de_add_idempotency_keys.py`
- `upgrade()`: `CREATE TABLE idempotency_keys (key VARCHAR(255) PRIMARY KEY, response TEXT NOT NULL, created_at DATETIME DEFAULT now())`
- `downgrade()`: `DROP TABLE idempotency_keys`
- Verificado: `alembic upgrade head` + `alembic downgrade base` funcionam em SQLite

### `tests/unit/test_schema.py` (2 testes)
- `test_table_is_registered`: `"idempotency_keys" in Base.metadata.tables`
- `test_table_columns`: key (String, PK), response (Text, NOT NULL), created_at (DateTime)

**Chain final de migrações:**
```
<base> → 17589825805b (Init)
       → 2a7f3c9e1d5d (current_lat/lng)
       → 05147e3ad5de (idempotency_keys) [head]
```

**Resultado:** **202 testes, 0 falhas, 99% cobertura.** Root-owned resolvido estruturalmente.

---

## Bloco 27 — Documento de Obrigações do Projeto

**Objetivo:** Criar um documento centralizado com as regras e convenções obrigatórias do projeto.

**O que foi feito:**
- `docs/obrigacoes.md` criado com:
  - Clean Architecture / DDD (camadas, dependências, protocolos, event bus)
  - Domínio Rico (entidades com comportamento, VOs imutáveis, proibição de domínio anêmico)
  - TDD (teste primeiro, determinístico, coberturas mínimas)
  - Cobertura mínima global de 80% em todas as camadas (100% domínio, 100% use cases, ≥80% infraestrutura)
  - Código em português BR para mensagens, inglês para nomes técnicos
  - Estrutura de diretórios e responsabilidades
  - Convenções de commit

---

## Bloco 28 — P7 Housekeeping (Frontend)

**Objetivo:** Eliminar lacunas de teste nos hooks do frontend e corrigir posicionamento arquitetural de `getRouteByRole`.

**O que foi feito:**

### P7.1 — Testes `useDeliveries` (10 cenários)
- `src/hooks/useDeliveries.test.ts` criado
- Cobertura: fetch (success, role param, AppError, generic error), create (success, AppError, generic error), update (success, AppError, generic error)

### P7.2 — Testes `usePlaces` (6 cenários + fix import)
- `src/hooks/usePlaces.test.ts` criado
- Cobertura: createFactory (success, AppError, generic error), createStore (success, AppError, generic error)
- Imports mortos de `Factory` e `Store` removidos de `usePlaces.ts:3`

### P7.3 — `getRouteByRole.ts` (clean-up arquitetural)
- `src/lib/routes.ts` criado com `getRouteByRole(role: UserRole)` type-safe
- `src/use_cases/getRouteByRole.ts` deletado
- Import em `useAuth.ts` atualizado para `'../lib/routes'`
- Teste existente atualizado com `as UserRole` para casos de fallback

**Arquivos:** 3 criados, 3 modificados, 1 deletado. Zero alteração de lógica de produção.

---

## Bloco 29 — P9 Linting Frontend

**Objetivo:** Resolver 24 problemas de lint no frontend sem supressões genéricas.

**O que foi feito:**

| ID | Arquivo | Correção |
|---|---|---|
| P9.1 | `dropdown-menu.tsx:27` | `ReactElement<any>` → `ReactElement<{ onClick?: () => void }>` |
| P9.2 | `useAuth.test.ts:22,29` | `mockExecute: any` → `ReturnType<typeof vi.fn>` + `as unknown as LoginUseCase` |
| P9.3 | `ApiDeliveryRepository.ts:5` | `raw: any` → interface `DeliveryApiResponse` |
| P9.4 | `handlers.ts:7,42` | `req.body as any` → `as { email: string; password: string }` |
| P9.5 | `useDeliveries.test.ts` + `usePlaces.test.ts` | `as any` → `as unknown as UseCaseType` (6 ocorrências) |
| P9.6 | `avatar.tsx:17` | `// eslint-disable-next-line` seletivo (shadcn) |
| P9.7 | `dialog.tsx:48` | `asChild` removido (prop não usada) |
| P9.8 | `jwt.ts:24` | `catch (e)` → `catch` sem parâmetro |

**Resultado:** Zero `as any` em produção. shadcn preservado com suppress por linha. Zero alteração de runtime.

---

## Bloco 30 — Início da Fase Final (Infraestrutura)

**Objetivo:** Preparar Dockerfile, CI/CD, Neon, DockerHub e Render para deploy.

---

## Bloco 31 — F.1 Dockerfile + F.2 DockerHub + F.3 CI/CD + F.4 Neon

### F.1 — Dockerfile Otimizado ✅
- Multi-stage build com `uv` em vez de `pip` (~300MB vs ~1.2GB)
- Entrypoint inteligente: wait PostgreSQL só se local (`db`/`localhost`/`127.0.0.1`)
- Sem `--reload` no CMD de produção
- `backend/Dockerfile` e `backend/entrypoint.sh` modificados

### F.2 — DockerHub ✅
- Repositório público `pedrogw/logistics-engine` criado
- Build: `sudo docker build -t pedrogw/logistics-engine:latest ...`
- Push: `sudo docker push pedrogw/logistics-engine:latest`

### F.3 — CI/CD Pipeline ✅
- `.github/workflows/ci.yml` criado e commitado
- Jobs: test (backend + frontend) → docker (build & push)
- Secrets no GitHub: `DOCKER_USER` e `DOCKER_PASSWORD` configurados

### F.4 — Neon ✅
- DATABASE_URL já existente no `.env`: Neon (sa-east-1, pooler)
- Migrations rodadas (`alembic upgrade head`) com sucesso
- Conexão verificada e banco acordado

### Pendente
- **F.5** — Render (WebService com existing image do DockerHub)

---

## Estado Atual (após Bloco 31)

- **202 testes backend**, 0 falhas, 99% cobertura
- **Frontend:** P7 ✅ + P9 ✅
- **Fase Final:** F.1 ✅ F.2 ✅ F.3 ✅ F.4 ✅ | **F.5 🔴 Pendente** (Render)

---

## Bloco 32 — Auditoria Geral + Correções (Backend + Frontend)

**Objetivo:** Varrer backend e frontend em busca de problemas de código, tipagem, arquitetura e lint; corrigir todos seguindo as obrigações do projeto.

### Auditoria

**Backend (17 problemas encontrados):**
| Severidade | Qtd | Principais |
|---|---|---|
| 🔴 Crítico | 1 | `worker_pool.close()` sem `await` — resource leak |
| 🟠 Alto | 1 | `FactoryResponse`/`StoreResponse` com `from_attributes=True` conflita com `location: Coordinates` (stale — tests já passam) |
| 🟡 Médio | 4 | `app/models/` com `.pyc` órfãos, `TestHandleDomainEvent` duplicado, type hints faltando em `map_factory`/`map_store`, `except: pass` silencioso no event bus |
| 🟢 Baixo | 11 | `__init__.py` faltando em 14 diretórios, `error.txt` stale, string UUID comparisons, etc. |

**Frontend (19 problemas encontrados):**
| Severidade | Qtd | Principais |
|---|---|---|
| 🔴 Alto | 1 | `TokenStorageProtocol` na infrastructure, importado pela application — viola Clean Arch |
| 🟡 Médio | 8 | `password?: string` opcional mas obrigatório, `Coordinates` vs `CoordinatesProps`, `login` sem `useCallback`, 3× unhandled rejection, `status: string` genérico |
| 🟢 Baixo | 10 | Mock incompleto, unused components, `src/use_cases/` vazio, `as any` em 4 lugares, `setState` em `useEffect` (4x), `Date.now()` impuro, `statusActions` unused, `<img>` sem `alt` |

### Correções

#### Backend (7 alterações)
| # | Arquivo | Correção |
|---|---------|----------|
| B1 | `app/main.py:48` | `worker_pool.close()` → `await worker_pool.close()` |
| B2 | `app/models/` | Diretório com `__pycache__` órfão removido |
| B3 | `tests/unit/test_worker.py:78-106` | Duplicata `TestHandleDomainEvent` removida; métodos órfãos (roundtrip) deletados |
| B4 | `app/api/places.py:15-19` | Type hints `FactoryEntity`/`StoreEntity` adicionados a `map_factory`/`map_store` |
| B5 | `app/core/events/bus.py:29` | `except: pass` → `logger.exception(...)` |
| B6 | 14 diretórios | `__init__.py` criados nos pacotes faltantes |
| B7 | `error.txt` | Deletado (stale de execução anterior) |

#### Frontend — Arquiteturais (9 alterações)
| # | Arquivo | Correção | Obrigação |
|---|---------|----------|-----------|
| F1 | `TokenStorageAdapter.ts` + `domain/repositories/TokenStorageProtocol.ts` | Interface movida da infrastructure para `domain/repositories/` | Clean Arch (protocolos no domínio) |
| F2 | `LoginUseCase.ts:8` | `password?: string` → `password: string` | Type hints |
| F3 | `CreateFactoryUseCase.ts:19` | Constrói `new Coordinates(input.location)` antes de passar ao protocolo | VO imutável no domínio |
| F4 | `CreateStoreUseCase.ts:20` | Mesmo que F3 | VO imutável |
| F5 | `ApiPlaceRepository.ts:6,11` | Aceita `Coordinates` (classe) em vez de `CoordinatesProps` | Protocolo é contrato |
| F6 | `useAuth.ts:12` | `login` envolvido em `useCallback([router])` | Performance React |
| F7 | 3× `handleLogout` (Sidebar, ControlTowerHeader, drive/page) | `try/catch` adicionado — falha de logout não bloqueia redirect | Tratamento de erros |
| F8 | `Delivery.ts` + `DeliveryRepositoryProtocol.ts` + `useDeliveries.ts` | `DeliveryStatus` union type criado em `src/domain/DeliveryStatus.ts` e tipado em toda a cadeia | Domínio rico |
| F9 | `LogoutUseCase.test.ts` + `src/use_cases/` | Mock completo (`refreshToken` adicionado) + diretório vazio deletado | Testes completos |

#### Frontend — Lint (10 erros zerados)
| # | Arquivo | Correção |
|---|---------|----------|
| L1 | `apiClient.test.ts:23,24,35,36` | 4× `as any` → tipo estrutural `AxiosInterceptorManager` |
| L2 | `drive/page.tsx:16,20` | `email` state + `useEffect` removidos (variável nunca usada) |
| L3 | `AuthGuard.tsx:19` | `useState(false)` → `useState(() => { ... lazy init ... })`; `useEffect` mantido só para side effects (redirect) |
| L4 | `ChaosDevTools.tsx:42` | `catch (err: any)` → `catch (err: unknown)` com tipo estrutural |
| L5 | `JanelaRecebimento.tsx:14` | `useEffect` → lazy initialization via `useState(fn)` |
| L6 | `KanbanCard.tsx:56` | `Date.now()` → `useState(Date.now)` + `setInterval` a cada 30s |
| L7 | `Sidebar.tsx:23` | `useEffect` → lazy initialization via `useState(fn)` |
| L8 | `DeliveryCard.tsx:18` | `statusActions` (Record) removido — variável nunca usada |
| L9 | `avatar.tsx:18` | `alt=""` adicionado ao `<img>` no shadcn AvatarImage |

### Infraestrutura
- Node.js 22.23.0 instalado via nvm (ambiente não tinha Node)
- `npm install` executado para restaurar dependências

### Resultado Final

| Projeto | Testes | Cobertura | Lint |
|---------|--------|-----------|------|
| **Backend** | **202 ✅** | **99%** | N/A |
| **Frontend** | **38 ✅** (13 arquivos) | N/A | **0 erros, 0 warnings** |

## Bloco 33 — Final: Docker Compose, Frontend Fixes, Login Problem

**Objetivo:** Subir todo o stack com Docker Compose e testar o fluxo de login E2E.

### O que foi feito:

#### Infraestrutura
- Node.js 22.23.0 instalado via nvm
- Frontend Dockerfile: `node:20-alpine` → `node:22-alpine` (lockfile v3 do npm 10 incompatível com npm 9)
- Backend Dockerfile: adicionado `COPY --from=builder /usr/local/bin /usr/local/bin` (CLI scripts `uvicorn`, `alembic`, `arq` não eram copiados — só `site-packages/`)
- `entrypoint.sh`: `.replace('+asyncpg', '')` no URL passado ao `asyncpg.connect()` (não entende scheme `postgresql+asyncpg://`); removido `2>/dev/null` para visibilidade; `alembic` → `python -m alembic`

#### Rotas do Frontend
- `ApiAuthRepository.ts`: `/api/v1/auth/login` → `/auth/login`; `/api/v1/auth/refresh` → `/auth/refresh`
- `api_client.ts`: URL de refresh no interceptor corrigida
- `docker-compose.yml`: `NEXT_PUBLIC_API_URL=http://api:8000` → `http://localhost:8000`

#### Problema Não Resolvido
- Login no navegador (`localhost:3000`) retorna "Erro de conexão com o servidor"
- `apiClient.baseURL = 'http://localhost:8000'` (default, bakeado em build time)
- Backend CORS permite `http://localhost:3000` → requisição cross-origin deveria funcionar
- Build com `--no-cache frontend` não resolveu
- API via `curl` direto no host deve ser testada para isolar se o problema é CORS ou rota

### Estado Atual
- `sudo docker compose up -d` → todos os 5 containers rodando (api healthy, frontend started)
- Seed já rodou anteriormente → `lojista@antigravity.com` / `admin123` e `motorista@antigravity.com` / `driver123` existem no banco
- Login via browser falha; pendente investigação (provável CORS ou baked URL errada no bundle)

### Pendências
- **F.5** — Render WebService (aguardando ação do usuário)
- **Login E2E** — Resolver "Erro de conexão com o servidor" no login do frontend
