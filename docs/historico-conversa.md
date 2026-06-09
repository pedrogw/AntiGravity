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

## Pendências

### Pendente 2 — Infraestrutura Real
**Situação:** Não iniciado
- `sudo chown -R pedro:pedro` em `migrations/versions/` e `.pytest_cache/` (root:root)
- `alembic revision --autogenerate` para colunas `current_lat` / `current_lng` (presentes no ORM, ausentes na migration)
- `alembic upgrade head` para PostgreSQL
- Docker compose com healthcheck, entrypoint com wait-for-it, upgrade automático
- CI/CD (GitHub Actions)

### Pendente 3 — Segurança
**Situação:** Não iniciado
- Rate limiting (ex.: slowapi)
- Refresh token JWT
- Validação de dono da entrega (só motorista dono pode atualizar)

### Pendente 4 — Robustez
**Situação:** Não iniciado
- Retry/lock para concorrência em atualizações simultâneas
- Idempotência no chaos injection (evitar duplicatas)

---

## Estado Atual
- **113 testes**, 0 falhas, 0 deprecation warnings
- **Cobertura:** `app/use_cases/` 100%, `app/schemas/` 100%, `app/api/` 100%
- **Exceto:** `_eta_recalculation.py:23` (early return), `place_repo.py:51` (update store)
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

## Arquivos Relevantes

### Domínio
- `app/domain/entities/`: Delivery (máquina de estados), EtaHistory, ChaosEventLog, Alert, Factory, Store, User, Coordinates
- `app/domain/haversine.py`, `app/domain/chaos.py`, `app/domain/safe_check.py`
- `app/domain/repositories/`: Protocolos para delivery, place, eta_history, chaos, alert, user

### Infraestrutura
- `app/infrastructure/repositories/`: Implementações SQLAlchemy (6 repositórios)
- `app/infrastructure/orm/`: Modelos SQLAlchemy

### Use Cases
- `app/use_cases/`: auth, deliveries, chaos, alert, dashboard + `_eta_recalculation.py`

### API
- `app/api/`: auth, places, deliveries, chaos, alerts, dashboard, deps
- `app/main.py`: FastAPI app com CORS, routers, exception handler

### Schemas
- `app/schemas/`: user, place, delivery, chaos, alert, dashboard

### Core
- `app/core/config.py` (Settings), `app/core/security.py` (JWT + bcrypt)

### Testes
- `tests/conftest.py`: Fixtures
- `tests/unit/test_use_cases.py`: 24 testes unitários
- `tests/api/test_integration.py`: 21 testes de integração
- `tests/api/test_security.py`: 6 testes
- `tests/api/test_validation.py`: ~22 casos parametrizados
- `tests/domain/`: test_simulation.py (19), test_engine.py (18), test_extreme.py (2)
