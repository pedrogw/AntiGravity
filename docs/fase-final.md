# Fase Final — AntiGravity Logistics

## Objetivo
Preparar infraestrutura para deploy: Dockerfile otimizado, CI/CD, banco online (Neon), registro de imagem (DockerHub) e hospedagem (Render).

---

## Concluídos ✅

| ID | Tarefa | Detalhes |
|---|---|---|
| **F.1** | Dockerfile otimizado | Multi-stage build com `uv`, entrypoint inteligente (wait PostgreSQL só se local), sem `--reload` |
| **F.2** | DockerHub | Repositório público `pedrogw/logistics-engine:latest` criado e imagem pusheada |
| **F.3** | CI/CD Pipeline | GitHub Actions em `.github/workflows/ci.yml`: testes backend + frontend → build & push Docker |

---

## Pendentes 🔴

| ID | Tarefa | Prioridade | Depende de |
|---|---|---|---|
| **F.4** | Neon (PostgreSQL gratuito) | — | ✅ Já configurado |
| **F.5** | Render (hospedagem) | Alta | F.4 (DATABASE_URL) + F.2 (imagem Docker) |

### F.5 — Render
- [ ] Criar conta em render.com
- [ ] Criar WebService → "Existing Image" → `pedrogw/logistics-engine:latest`
- [ ] Configurar variáveis de ambiente (DATABASE_URL do Neon)
- [ ] Rodar migrations: `alembic upgrade head`

---

## Arquitetura Final

```
GitHub Push
    ↓
GitHub Actions (test + lint)
    ↓
DockerHub (pedrogw/logistics-engine:latest)
    ↓
Render.com (WebService)
    ↓
Neon (PostgreSQL)

Backend: FastAPI + SQLAlchemy async
Frontend: Next.js (separado ou integrado)
Redis: Opcional (worker ARQ desativado sem Redis)
```
