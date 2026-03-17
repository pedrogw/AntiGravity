## Context

Projeto greenfield para TCC de BSI (60h). Não há código existente. O sistema é composto por uma API REST de gerenciamento logístico (FastAPI) e um Frontend Web (Next.js). A plataforma calcula tempo de entrega (fábrica → loja), permite simulação de eventos de caos que recalculam ETA, monitora segurança do motorista em rota, e acumula dados estruturados de incidentes para futura aplicação de modelos preditivos.

**Constraints:**
- 60 horas de desenvolvimento total
- Sem dependência de APIs externas (mapas simulados)
- PostgreSQL obrigatório para estabilidade no backend
- Frontend obrigatório desenvolvido em Next.js (App Router) com TypeScript
- Estilização restrita ao uso de Tailwind CSS e ecossistema shadcn/ui
- Orquestração completa local via Docker e docker-compose obrigatória
- Todos os timestamps em UTC internamente

## Goals / Non-Goals

**Goals:**
- Arquitetura de Monorepo (pastas `backend/` e `frontend/`) orquestrada via docker-compose
- API REST completa e bem documentada via OpenAPI/Swagger
- Frontend focado nas telas de demonstração da banca (Painel do Operador e Visão do Motorista)
- Multi-role transparente (operador, lojista, motorista)
- Simulador de caos que recalcula ETA em tempo real (rota fixa, só tempo muda)
- Reroute pelo motorista quando ele efetivamente muda de rota
- Histórico de ETA + log de caos para acúmulo de dados de ML futuro
- Sistema de safe-check com lazy evaluation para segurança do motorista
- Endpoint de demonstração para apresentação na banca

**Non-Goals:**
- Telas de configuração complexas no Frontend (ex: CRUD total de lojas e janelas será via API/Swagger para poupar escopo de UI nas 60h)
- Integração com APIs de mapas reais interativos no frontend (usaremos visualizações simplificadas)
- Eventos de caos customizáveis pelo operador (só os 4 pré-definidos)
- Treinamento de modelos de ML (só acúmulo de dados)
- Legislação de descanso obrigatório (CLT/Lei do Motorista)
- Notificações push ou WebSocket (fora do escopo das 60h, frontend usará polling se necessário)

## Decisions

### 1. Estrutura Monorepo e Orquestração Docker

**Decisão:** O repositório será um monorepo orquestrado integralmente via `docker-compose`. Haverá 3 containers principais: `backend` (FastAPI), `frontend` (Next.js) e `db` (PostgreSQL).

```
logistics-manager/
├── docker-compose.yml
├── backend/
│   ├── Dockerfile
│   ├── app/                # Código FastAPI modularizado
│   └── requirements.txt
└── frontend/
    ├── Dockerfile
    ├── src/                # Código Next.js
    ├── tailwind.config.ts
    └── package.json
```

**Rationale:** O uso do `docker-compose` empacota toda a complexidade de execução. Para a banca do TCC, qualquer avaliador com Docker instalado poderá subir o projeto inteiro (Banco, API e Interface) rodando apenas um `docker-compose up -d`. O backend manterá a organização modular por domínio de negócio dentro de `app/`.

### 2. Stack do Frontend: Next.js + Tailwind + shadcn/ui

**Decisão:** Uso exclusivo de Next.js (App Router) com TypeScript rigoroso. O design system será montado apenas com TailwindCSS e componentes copiáveis do `shadcn/ui` (ex: Cards, Buttons, Tables, Dialogs).

**Rationale:** Essa tech stack é uma exigência do projeto (BSI). O `shadcn/ui` garante uma interface visualmente profissional e acessível quase instantaneamente, compensando o tempo curto das 60h. O frontend será um "MVP Visual" concentrado na utilidade da demonstração.

### 3. Cálculo de ETA simulado

**Decisão:** `ETA = distância_km / velocidade_media_kmh` com coordenadas (lat/lng) usando fórmula de Haversine para distância no backend.

**Rationale:** Haversine dá precisão suficiente para demonstração. Velocidade média configurável (urbana: 40 km/h, rodovia: 80 km/h).

### 4. Mecanismo de caos — rota fixa, só tempo muda

**Decisão:** Cada evento de caos tem um `impact_factor` (multiplicador de tempo) e um `delay_minutes` (atraso fixo adicional). A rota NÃO muda — eventos só afetam o tempo estimado.

| Evento | impact_factor | delay_minutes |
|---|---|---|
| Chuva | 1.3 (30% mais lento) | 0 |
| Alagamento | 1.0 (bloqueio) | 45 |
| Engarrafamento | 1.5 (50% mais lento) | 15 |
| Acidente | 1.0 (bloqueio) | 60 |

**Recálculo:** `novo_ETA = (ETA_restante × impact_factor) + delay_minutes`

Múltiplos eventos se acumulam multiplicativamente. O frontend terá um painel exclusivo ("Painel de Caos") para injetar visualmente esses eventos em uma entrega ativa.

### 5. Reroute pelo motorista

**Decisão:** O motorista pode informar que mudou de rota via endpoint de reroute. O sistema recalcula a distância restante usando Haversine e aplica eventos de caos ativos.  No Frontend haverá uma tela "Driver View" com um grande botão de Pânico/Reroute simulando o app mobile.

### 6. Safe-Check com lazy evaluation

**Decisão:** Quando o motorista reporta velocidade = 0 km/h, o backend gera um `ping` com timer (5 min). A expiração é verificada por **lazy evaluation**. O frontend do operador fará polling na listagem de alertas para exibi-los no dashboard.

### 7. PostgreSQL com SQLAlchemy 2.0 async + UTC

**Decisão:** asyncpg + SQLAlchemy 2.0 async ORM. Alembic para migrações. Armazenamento persistente num container Postgres com volume montado no Docker. FastAPI servirá a validação com Pydantic V2 restrito.

**Rationale:** Exigência técnica BSI de alta performance e consistência transacional.

### 8. Paginação com defaults

**Decisão:** Todos os endpoints REST de listagem aceitam limit e offset. O frontend Next.js consumirá esses endpoints para gerar as tabelas shadcn (Data Tables).

### 9. Histórico de ETA + log de caos para ML

**Decisão:**
- `eta_history`: registra cada mudança de ETA (before, after, reason). Será exibido em um componente Timeline no frontend.
- `chaos_event_log`: backup permanente de todos os eventos para análise futura de ML.

## Risks / Trade-offs

- **[Escopo de 60h + Frontend + Docker]** → Desenvolver backend, frontend e orquestração Docker em 60h é desafiador. A mitigação é o MVP: o frontend terá apenas telas essenciais, e o Dockerfile focará apenas em execução local, sem pipelines CI/CD complexos.
- **[Simulação vs realidade]** → ETA simulado não reflete rotas reais.
- **[Sem WebSocket]** → O Next.js precisará fazer polling via hooks no cliente (como SWR ou React Query) para simular o tempo real das viaturas. Aceitável para MVP.
- **[Log de ML sem modelo]** → O TCC documentará apenas a coleta estruturada para trabalhos futuros.

## Open Questions

_(resolvidas após o realinhamento de arquitetura)_
