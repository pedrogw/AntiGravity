# AntiGravity — Logistics Analytics Engine

**Autor:** Pedro Gabriel Wojtyla Moreira Silva  
**Curso:** Sistemas de Informação — 5º Período — CEFET MG  
**Período de Desenvolvimento:** Março a Junho de 2026

---

## Resumo

O AntiGravity é um motor analítico B2B de logística que conecta lojistas e motoristas em uma plataforma unificada de rastreamento de entregas. O sistema oferece desde o cadastro de fábricas e lojas até o ciclo completo de uma entrega — criação, aceitação pelo motorista, rota em trânsito, confirmação de entrega e conclusão — com suporte a cancelamento e reporte de problemas em tempo real. Cada etapa é governada por uma máquina de estados rigorosa, e o cálculo de ETA considera distância geodésica (Haversine), eventos de caos simulados e recálculos assíncronos via fila de background.

Construído sobre Clean Architecture e Domain-Driven Design, o projeto separa rigidamente as camadas de domínio, aplicação, infraestrutura e API, garantindo testabilidade e manutenibilidade. O backend em FastAPI (Python assíncrono) se comunica com PostgreSQL via SQLAlchemy async e utiliza Redis para cache distribuído e fila de workers ARQ. O frontend em Next.js App Router (TypeScript + TailwindCSS + shadcn/ui) segue a mesma arquitetura limpa, com hooks, use cases e repositórios desacoplados. Toda a esteira é automatizada via GitHub Actions: testes, build Docker, push para DockerHub e deploy em Render (backend) e Vercel (frontend).

---

## Problema

Pequenas e médias empresas de logística enfrentam dificuldades para rastrear entregas em tempo real, comunicar motoristas e lojistas, e reagir a imprevistos como trânsito, acidentes ou falhas mecânicas. Sistemas prontos são caros e fechados; planilhas não escalam. O AntiGravity propõe uma alternativa open-source com rastreamento inteligente, SLA mensurável e injeção de Chaos Engineering para testar a resiliência do sistema sob condições adversas.

---

## Arquitetura

O projeto segue Clean Architecture / DDD com dependências apontando para o centro (domínio):

```
backend/
├── domain/           → Entidades, Value Objects, serviços, protocolos, eventos
│   ├── entities/     → Delivery, Alert, User, ChaosEventLog, Place
│   ├── value_objects/→ Coordinates (VO imutável)
│   ├── repositories/ → Protocolos de repositório
│   └── services/     → EtaService
├── use_cases/        → Orquestradores (1 arquivo por agregado coeso)
├── schemas/          → Pydantic (entrada/saída da API)
├── api/              → Rotas FastAPI (thin: validação + delegação)
├── infrastructure/   → Repositórios SQLAlchemy, ORM, cache, listeners, worker
├── core/             → Config, security, exceptions, logging, event bus, rate limiter
└── main.py           → App factory, lifespan, routers, exception handlers

frontend/
├── domain/           → Entidades, protocolos, erros, VOs
├── application/      → Use cases
├── infrastructure/   → ApiClient, repositórios HTTP, storage, DI
├── hooks/            → useAuth, useDeliveries, usePlaces, useAlerts, useUsers
└── components/       → LoginForm, AuthGuard, Dashboard, Driver, ui (shadcn)
```

### Fluxo de dados

```
Cliente → API Router → Use Case → Domínio (entidade) → Repositório (protocolo)
                                                          ↓
                                                   SQLAlchemy (infra)
                                                          ↓
                                                   PostgreSQL / Neon
```

Eventos de domínio são publicados em um barramento in-process e consumidos por listeners de auditoria, invalidação de cache e fila ARQ para processamento assíncrono.

---

## Stack Tecnológica

| Camada | Tecnologia |
|--------|-----------|
| Backend | Python 3.12, FastAPI, SQLAlchemy 2.0 (async), Alembic |
| Frontend | Next.js 15 (App Router), TypeScript, TailwindCSS, shadcn/ui |
| Banco | PostgreSQL (Neon serverless), SQLite (testes) |
| Cache | Redis 7 (cache-aside + fila ARQ) |
| Testes | Pytest (backend, 98% cobertura), Vitest + MSW (frontend) |
| Deploy | Docker, Render (backend), Vercel (frontend) |
| CI/CD | GitHub Actions (test → docker → deploy) |
| Ferramentas | Ruff (lint), uv (build), Leaflet (mapas) |

---

## Funcionalidades

### Backend
- **Autenticação:** JWT com access token (30 min) + refresh token (30 dias), bcrypt, roles (lojista, motorista, admin)
- **Entregas:** CRUD completo com máquina de estados de 5 status (`pendente → aceita → em_transito → entregue → concluida` + `cancelada`), validação de dono, recálculo de ETA com Haversine
- **Chaos Engineering:** Injeção de eventos de caos com idempotência via `Idempotency-Key`, impacto em ETA, alertas críticos automáticos
- **Alertas:** Criação automática em eventos críticos e reportes, dispensa pelo lojista, expiração após 7 dias
- **Dashboard:** Métricas agregadas com queries paralelas (`asyncio.gather`)
- **Cache Distribuído:** Redis com Cache-Aside, invalidação por evento, fallback transparente
- **Worker Assíncrono:** ARQ para recálculo de ETA e criação de alertas em background
- **Observabilidade:** Request ID, logging estruturado, mascaramento de dados sensíveis, health check
- **Rate Limiting:** 3/min (register), 5/min (login), 10/min (chaos injection)

### Frontend
- **Dashboard do Lojista:** Kanban de entregas, tabela com filtros, métricas, lista de alertas com badge crítico
- **Drive do Motorista:** Mapa interativo (Leaflet) com posição do motorista e marcador da loja, arrastável para simular posição, botões de ação por status, diálogo de reporte de problema com 6 tipos predefinidos
- **Autenticação:** Login com redirect por role, interceptor automático de refresh token, logout seguro
- **ChaosDevTools (test accounts):** Painel para injetar caos e simular posição, gated por email
- **Componentes:** shadcn/ui customizados, Dialog de criação de entrega com selects, Sidebar dinâmica

---

## Qualidade

| Métrica | Resultado |
|---------|-----------|
| Testes backend | **266** passando, 0 falhas |
| Cobertura backend | **98%** total (domínio 100%, use cases 100%) |
| Testes frontend | **143** passando, 0 falhas |
| TypeScript | **0 erros** (`tsc --noEmit`) |
| ESLint (frontend) | **0 erros, 0 warnings** |
| Ruff (backend) | **All checks passed** |
| Warnings pytest | **0** (eliminados todos os deprecation warnings do fakeredis) |

---

## Deploy

| Serviço | URL | Função |
|---------|-----|--------|
| Backend | `https://logistics-engine-latest.onrender.com` | API FastAPI |
| Frontend | `https://anti-gravity-beryl.vercel.app` | Aplicação Next.js |
| Banco | Neon (sa-east-1) | PostgreSQL serverless |
| Imagem Docker | `pedrogw/logistics-engine:latest` | DockerHub |
| CI/CD | GitHub Actions | Test → Docker → Render → Vercel |

### Pipeline CI/CD
```
git push → pytest + npm test → docker build & push → Render deploy → Vercel deploy
```

---

## Como Rodar Localmente

### Pré-requisitos
- Docker e Docker Compose
- Git

### Passos

```bash
git clone <repo-url>
cd antigravity

# Iniciar todos os serviços
docker compose up -d

# Rodar seed de dados (lojista, motorista, admin)
docker compose exec api python seed.py
docker compose exec api python admin_seed.py

# Acessar
# Frontend: http://localhost:3000
# Backend:  http://localhost:8000
# Health:   http://localhost:8000/health
```

### Credenciais Padrão

| Papel | Email | Senha |
|-------|-------|-------|
| Lojista | `lojista@antigravity.com` | `admin123` |
| Motorista | `motorista@antigravity.com` | `driver123` |
| Admin | `admin@antigravity.com` | `admin123` |

---

## Lições Aprendidas

- **Domínio rico elimina use cases complexos:** Mover a máquina de estados, validação de coordenadas e lógica de criticalidade para as entidades reduziu os use cases a orquestradores finos de I/O, eliminou código duplicado e simplificou os testes.
- **Testes determinísticos exigem disciplina:** O uso de `datetime.utcnow` em produção exige `unittest.mock.patch` nos testes — `monkeypatch` não funciona em built-ins C-level. Datas fixas (ex: 2050) garantem previsibilidade em testes de caos.
- **Cache-aside com invalidação por evento é simples e eficaz:** Redis como cache com fallback transparente para o banco evita complexidade de cache coherence, e a invalidação via domain events mantém a consistência eventual sem poluir os use cases.
- **Idempotency-Key previne estragos em cenários de retry:** Em vez de optimistic lock (que resolve lost update mas não duplicata), o header `Idempotency-Key` no estilo Stripe previne duplicação de eventos de caos com impacto direto no ETA.
- **DDD não precisa ser dogmático:** Algumas decisões — como lazy imports para evitar circular dependencies entre `Coordinates` e Haversine, ou o event bus in-process em vez de message broker externo — sacrificam pureza arquitetural por pragmatismo sem comprometer a testabilidade.
- **frontend seguindo clean architecture é viável:** A mesma separação em camadas (domain → application → infrastructure → components) usada no backend se aplica bem ao frontend React, com hooks atuando como "use cases" da UI e componentes puramente de apresentação.
