# Processos em Andamento

## Planejado

| Processo | Status | Depende de |
|---|---|---|
| **Block C — Listar places + drivers** (frontend) | 📋 Planejado | A, B |
| **Block D — Dialog "Criar Entrega"** (frontend) | 📋 Planejado | C |
| **Block E — Status `aceita`** (backend + frontend) | 📋 Planejado | — |
| **Block F — Concluir Entrega** (frontend) | 📋 Planejado | E |

### Detalhamento dos Blocos

| Bloco | Arquivos | TDD |
|-------|----------|-----|
| **A** ✅ | `user_repo.py` (protocolo + infra), `users.py` (API novo), `main.py`, `test_users.py` | `test_list_drivers_returns_only_motorista`, `test_list_drivers_requires_auth`, `test_list_drivers_empty_when_no_motorista` |
| **B** ✅ | `ApiPlaceRepository.ts`, `ApiPlaceRepository.test.ts` | `test_createFactory_calls_POST`, `test_createFactory_network_error`, `test_createStore_calls_POST`, `test_createStore_network_error` |
| **C** | `UserRepositoryProtocol.ts` (novo), `ApiUserRepository.ts` (novo), `ListDriversUseCase.ts` (novo), `useUsers.ts` (novo), `PlaceRepositoryProtocol.ts`, `usePlaces.ts`, `factories.ts` | Testes de use cases + hooks |
| **D** | `CriarEntregaDialog.tsx` (novo), `dashboard/page.tsx` | Testes de render + submit |
| **E** | `delivery.py`, `DeliveryStatus.ts`, `DeliveryCard.tsx`, `drive/page.tsx`, `test_use_cases.py` | `pendente→aceita→em_transito`, botão "Aceitar" |
| **F** | `drive/page.tsx` | `onComplete` wired |

---

## Concluídos

| Processo | Status |
|---|---|
| **Block B — ApiPlaceRepository real** (frontend) | ✅ **Concluído** |
| **Block A — GET /users/drivers** (backend) | ✅ **Concluído** |
| **Plano 4 — Deploy Vercel + Render + CI/CD** | ✅ **Concluído** |

| Serviço | URL | Status |
|---------|-----|--------|
| DockerHub | `pedrogw/logistics-engine:latest` | ✅ Atualizada (2026-06-24 15:42, digest `sha256:21321...`) |
| Render (backend) | `https://logistics-engine-latest.onrender.com` | ✅ Health 200, login funciona |
| Neon (DB) | (via Render) | ✅ Conexão confirmada (login OK) |
| Vercel (frontend) | `https://anti-gravity-beryl.vercel.app` | ✅ Página de login servida |
| CORS | Render → localhost:3000 | ✅ Funciona |
| CORS | Render → Vercel | ✅ Configurado — `ALLOWED_ORIGINS` no Render com ambos os origins |

### Plano 4 — Deploy Vercel + Render + CI/CD

| Item | Status | Detalhe |
|------|--------|---------|
| 1. CORS configurável (config.py + main.py) | ✅ Concluído | `ALLOWED_ORIGINS` lido de env var em vez de hardcoded. |
| 2. Build + push DockerHub | ✅ Concluído | Build com uv, push autenticado via access token. |
| 3. Render: env vars + redeploy | ✅ Concluído | `ALLOWED_ORIGINS=http://localhost:3000,https://anti-gravity-beryl.vercel.app`. CORS verificado. |
| 4. Vercel: `NEXT_PUBLIC_API_URL` + redeploy | ✅ Concluído | `NEXT_PUBLIC_API_URL=https://logistics-engine-latest.onrender.com`. Frontend servindo. |
| 5. CI/CD workflow | ✅ Concluído | GitHub Actions: `test → docker → deploy`. Pipeline completa com sucesso (run ID 28123517822). |
| 6. CORS regex para previews Vercel | ✅ Concluído | `allow_origin_regex` aceita qualquer `*.vercel.app`. Testado com pytest (3/3). |
| 7. Vercel auto-deploy no CI/CD | ✅ Concluído | Step `Trigger Vercel Deploy` adicionado após Render. Pipeline: `test → docker → deploy (Render) → deploy (Vercel)`. |

---

## Concluídos

| Processo | Status |
|---|---|
| **Plano 3 — Bloqueantes Frontend (Login + Sidebar + ChaosDevTools)** | ✅ **Concluído** |
| Pendente 3 — Segurança | ✅ Concluído |
| Fase D — Domínio Rico (9/9 tarefas) | ✅ Concluído |
| Pendente 4 — Robustez (Idempotency Key) | ✅ Concluído |
| Pendente 5 — Cache em produção | ✅ Concluído |
| Pendente 6 — Worker Queue Async (3 fases) | ✅ Concluído |
| Pendente 8 — Cobertura Infraestrutura ≥80% | ✅ Concluído |
| Migration `idempotency_keys` | ✅ Concluído |
| **P7 — Housekeeping (Frontend)** | ✅ **Concluído** |
| **P9 — Linting Frontend** | ✅ **Concluído** |
| **F.1 — Dockerfile Otimizado** (multi-stage + uv) | ✅ **Concluído** |
| **F.2 — Neon (PostgreSQL online)** | ✅ **Concluído** |
| **F.3 — DockerHub (Imagem)** | ✅ **Concluído** |
| **F.4 — Render (Deploy online)** | ✅ **Concluído** |
| **CI/CD Pipeline** (testes → DockerHub → Render) | ✅ **Concluído** |

---

## Concluídos — Correções de Média Severidade (Blocos 4–6 ✅)

| Bloco | Item | Status |
|-------|------|--------|
| **4a** | M2 — Auth em `GET /deliveries/` | ✅ Concluído |
| **4b** | M2 — Auth em `GET /places/factories` | ✅ Concluído |
| **4c** | M2 — Auth em `GET /places/stores` | ✅ Concluído |
| **5** | M3 — Renomear `Alert.critical()` → `Alert.from_chaos()` | ✅ Concluído |
| **6.1** | M5 — Criar schema `DeliveryCacheItem` | ✅ Concluído |
| **6.2** | M5 — Adicionar `get_list`/`set_list` ao CacheService | ✅ Concluído |
| **6.3** | M5 — Migrar `ListDeliveriesUseCase` para cache tipado | ✅ Concluído |
| **6.4** | M5 — Atualizar testes | ✅ Concluído |
| **6.5** | M5 — Verificar (pytest + ruff) | ✅ Concluído |
| **6.6** | M5 — Atualizar docs | ✅ Concluído |

### Plano 3 — Bloqueantes Frontend

| Item | Status | Detalhe |
|------|--------|---------|
| 1. Login E2E | ✅ Resolvido | Todas as 6 camadas investigadas (backend, CORS, bundle, rede, logs, axios): 100% funcionais. Causa provável: cache corrompido do build Docker. Login funciona no navegador. |
| 2. Remover Control Tower | ✅ Commitado | `db85e90`: `app/control-tower/` + `components/control-tower/` (11 arquivos) deletados; `Sidebar.tsx` reduzido. |
| 3. ChaosDevTools gated | ✅ Commitado | `db85e90`: `ChaosDevTools.tsx` com gate por test account; logout cleanup em `Sidebar.tsx` + `drive/page.tsx`. |
