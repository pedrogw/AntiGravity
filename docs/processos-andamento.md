# Processos em Andamento

## Em andamento

| Processo | Status |
|---|---|
| **Plano 4 — Deploy Vercel + Render + CI/CD** | 🟡 Em andamento |

### Plano 4 — Deploy Vercel + Render + CI/CD

| Item | Status | Detalhe |
|------|--------|---------|
| 1. CORS configurável (config.py + main.py) | ✅ Concluído | `ALLOWED_ORIGINS` lido de env var em vez de hardcoded. |
| 2. Build + push DockerHub | ✅ Concluído | Build com uv, push autenticado via access token (sudo docker login). Image digest: `sha256:21321bf29c975d86ea375ebffdfe7d8003300f8743f700ff77f26d178857a993` |
| 3. Render: adicionar env vars + redeploy | 🔴 Aguardando usuário | Necessário: dashboard Render → Environment → `ALLOWED_ORIGINS=http://localhost:3000,https://anti-gravity-beryl.vercel.app` → Manual Deploy |
| 4. Vercel: adicionar `NEXT_PUBLIC_API_URL` + redeploy | 🔴 Aguardando usuário | Necessário: dashboard Vercel → Settings → `NEXT_PUBLIC_API_URL=https://logistics-engine-latest.onrender.com` → Redeploy |
| 5. CI/CD (`.github/workflows/ci.yml`) | 🔴 Pendente | Aguarda conclusão dos itens 3 e 4; precisa verificar secrets `DOCKER_USER`, `DOCKER_PASSWORD`, `RENDER_DEPLOY_HOOK` no GitHub |

| Serviço | URL | Status |
|---------|-----|--------|
| DockerHub | `pedrogw/logistics-engine:latest` | ✅ Atualizada (2026-06-24 15:42, digest `sha256:21321...`) |
| Render (backend) | `https://logistics-engine-latest.onrender.com` | ✅ Health 200, login funciona |
| Neon (DB) | (via Render) | ✅ Conexão confirmada (login OK) |
| Vercel (frontend) | `https://anti-gravity-beryl.vercel.app` | ✅ Página de login servida |
| CORS | Render → localhost:3000 | ✅ Funciona |
| CORS | Render → Vercel | ❌ **Não configurado** — `access-control-allow-origin` só tem `localhost:3000` |

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
