# Processos em Andamento

## Em andamento

| Processo | Status |
|---|---|
| **Plano 4 — Deploy Vercel + Render + CI/CD** | 🔴 Pendente |

### Plano 4 — Deploy Vercel + Render + CI/CD

| Item | Status | Detalhe |
|------|--------|---------|
| 1. CORS configurável (config.py + main.py) | ✅ Concluído | `ALLOWED_ORIGINS` lido de env var em vez de hardcoded. |
| 2. Build + push DockerHub | 🔴 Bloqueado | Build concluído (image `7c4f8d292ba3`). **Push negado:** `denied: requested access to the resource is denied`. Necessário login no DockerHub (`docker login --username pedrogw`) mas CLI não tem TTY interativo. |
| 3. Render: adicionar env vars + redeploy | 🔴 Pendente | Aguarda Item 2 (precisa da imagem atualizada no DockerHub) |
| 4. Vercel: adicionar `NEXT_PUBLIC_API_URL` + redeploy | 🔴 Pendente | Aguarda Item 3 (precisa do Render rodando com a imagem atualizada + CORS) |
| 5. CI/CD (`.github/workflows/ci.yml`) | 🔴 Pendente | Aguarda resolução dos itens anteriores |

**Bloqueante:** DockerHub push requer autenticação `pedrogw` — não foi possível fazer login via CLI sem TTY interativo.

| Serviço | URL | Status |
|---------|-----|--------|
| DockerHub | `pedrogw/logistics-engine:latest` | ✅ Imagem existe (atualizada 13:36) |
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

### Plano 3 — Bloqueantes Frontend

| Item | Status | Detalhe |
|------|--------|---------|
| 1. Login E2E | ✅ Resolvido | Todas as 6 camadas investigadas (backend, CORS, bundle, rede, logs, axios): 100% funcionais. Causa provável: cache corrompido do build Docker. Login funciona no navegador. |
| 2. Remover Control Tower | ✅ Commitado | `db85e90`: `app/control-tower/` + `components/control-tower/` (11 arquivos) deletados; `Sidebar.tsx` reduzido. |
| 3. ChaosDevTools gated | ✅ Commitado | `db85e90`: `ChaosDevTools.tsx` com gate por test account; logout cleanup em `Sidebar.tsx` + `drive/page.tsx`. |
