# Processos em Andamento

Itens que estão sendo ativamente trabalhados, mas ainda não concluídos.
Consulte `docs/historico-conversa.md` para o histórico completo.

| Processo | Status | Observação |
|---|---|---|
| Pendente 3 — Segurança | Concluído ✅ | Rate limiting, validação de dono, refresh token JWT — tudo implementado |
| **Fase D — Domínio Rico** (eliminar anemic domain) | **Concluído ✅** (9/9 tarefas) | Todas as entidades agora têm comportamento encapsulado. Domínio 100% coberto. |
| **Pendente 4 — Robustez** | **Concluído ✅** | Idempotency Key no chaos injection. Header `Idempotency-Key` evita duplicatas. |

### Fase D — Domínio Rico (sub-tarefas)

| ID | Tarefa | Status | Análise de Impacto |
|---|---|---|---|
| D.1 | `Coordinates` — validar lat/lng em `__post_init__` + `distance_to(other)` | ✅ Concluída | ✅ Concluída |
| D.2 | `User` — `role: UserRole` (enum) + `is_motorista()` / `is_lojista()` | ✅ Concluída | ✅ Concluída |
| D.2t | `User` — testes de domínio para `is_motorista()` e `is_lojista()` | ✅ Concluída | ✅ Concluída |
| D.3 | `Alert` — factory method `critical()` com cálculo interno de criticalidade | ✅ Concluída | ✅ Concluída |
| D.4a | `Delivery` — `change_status()` com máquina de estados encapsulada | ✅ Concluída | ✅ Concluída |
| D.4b | `Delivery` — `update_position(lat, lng)` | ✅ Concluída | ✅ Concluída |
| D.4c | `Delivery` — `apply_chaos(impact_factor, delay_minutes)` | ✅ Concluída | ✅ Concluída |
| D.4d | `Delivery` — `recalculate_eta(origin, store, speed, chaos_events)` → `EtaHistory` | ✅ Concluída | ✅ Concluída |
| D.5 | `ChaosEventLog` — `aggregate(events)` método estático | ✅ Concluída | ✅ Concluída |

**Regra:** Cada fase D.X só inicia implementação após análise de impacto concluída e mitigação documentada.

### Pendentes de Cobertura (Infraestrutura <80%)

Arquivos de infra que usam conectores reais (DB, Redis) e são substituídos por mocks nos testes — exigem infraestrutura real para cobertura >80%:

| Arquivo | Cobertura | Missing |
|---|---|---|
| `main.py` | 72% | inicialização FastAPI + wiring |
| `bootstrap.py` | 67% | `get_db`, `dispose_engine` |
| `redis_client.py` | 50% | `get_redis`, `close_redis` |
| `audit_listener.py` | 60% | audit logging |
| `cache_invalidation_listener.py` | 62% | cache invalidation |
