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

### 10. Global Exception Handling e Resiliência (Non-Functional)

**Decisão:**
A aplicação deve ser resiliente a falhas sistêmicas e imprecisões no contrato de dados.
- **Backend (FastAPI):** Um middleware ou exception handler global (`@app.exception_handler`) interceptará todas as falhas não tratadas. Erros de infraestrutura (ex: `asyncpg.exceptions.ConnectionDoesNotExist` ou timeout do PostgreSQL) retornarão HTTP 503 Service Unavailable, mascarando a stack trace do usuário. Erros de validação (Pydantic `ValidationError`) retornarão HTTP 422 padronizado.
- **Frontend (Next.js):** Todas as formulários e interações que enviam payload (ex: injeção de evento de caos) validarão os dados localmente (client-side) antes do envio. Caso o servidor responda com 503 ou 500, toasts da biblioteca shadcn/ui serão exibidos notificando a "Instabilidade na plataforma".

**Rationale:** Exigência de infraestrutura resiliente. Isola falhas de banco de dados para não expor segurança e economiza round-trips de rede validando dados incorretos no Next.js precocemente.

## Low-Level Engineering & Architecture

Para garantir precisão durante a fase de implementação e mitigar alucinações de código, a fundação técnica abaixo deve ser rigorosamente seguida.

### 1. Database Structure (PostgreSQL Schema)
Modelagem relacional focada em consistência via SQLAlchemy 2.0:
- **`users`**: `id` (UUID PK), `email` (VARCHAR, Unique), `password_hash` (VARCHAR), `role` (ENUM: operador, lojista, motorista), `created_at` (TIMESTAMPTZ UTC).
- **`factories`**: `id` (UUID PK), `name` (VARCHAR), `lat` (FLOAT), `lng` (FLOAT).
- **`stores`**: `id` (UUID PK), `name` (VARCHAR), `lat` (FLOAT), `lng` (FLOAT), `owner_id` (FK -> users.id).
- **`deliveries`**: `id` (UUID PK), `factory_id` (FK -> factories.id), `store_id` (FK -> stores.id), `driver_id` (FK -> users.id), `status` (ENUM: pendente, em_transito, entregue, cancelada), `eta_original` (TIMESTAMPTZ), `eta_current` (TIMESTAMPTZ), `departed_at` (TIMESTAMPTZ).
- **`eta_history`**: `id` (UUID PK), `delivery_id` (FK -> deliveries.id), `eta_before` (TIMESTAMPTZ), `eta_after` (TIMESTAMPTZ), `reason` (VARCHAR), `created_at` (TIMESTAMPTZ).
**Indices:** B-Tree em `deliveries.driver_id`, `deliveries.store_id` e `eta_history.delivery_id` para acelerar queries paginadas do painel.

### 2. TypeSafe Contracts (SQLAlchemy -> Pydantic)
- **Data Transfer Objects (DTOs):** A camada da API nunca retornará as instâncias brutas do SQLAlchemy. Pydantic v2 `BaseModel` será usado para filtrar dados.
- Exemplo prático: O modelo de banco `User` contém `password_hash`. A rota de login/listagem usará o schema Pydantic `UserResponse` que exclui a senha e expõe apenas `id`, `email` e `role`.
- O strict mode do Pydantic (`model_config = ConfigDict(strict=True)`) deve ser ativado para as rotas C-Level (caos, rotas).

### 3. Next.js Architecture (App Router Flow)
Uso pragmático de Server vs Client Components para isolar estado interativo de buscas de banco (SSR):
- **Server Components:** `app/dashboard/page.tsx` fará fetch server-side usando o token mantido em HttpOnly cookies. Não usará a diretiva `"use client"`. Transfere HTML limpo para o browser.
- **Client Components:** Só usado nos "galhos" da árvore. `components/dashboard/chaos-injector.tsx` usará `"use client"` para gerenciar o `useState` do select box e prender validações no front antes do `fetch()`.

### 4. Mapeamento de UI (shadcn/ui Allowlist)
Para manter o design system coeso e limpo nas 60h, fica PROIBIDO criar componentes interativos UI complexos em Tailwind puro se existir equivalente no shadcn.
**Lista de Componentes Autorizados:**
- `Button` (Ações gerais)
- `Card` (Para agrupar métricas e formulários)
- `Table` / `DataTable` (Listagem de entregas para operadores e lojistas)
- `Dialog` (Modal sobreposto para injeção visual do caos)
- `Badge` (Cores semânticas para Status: Pendente=Cinza, Em_Transito=Azul, Entregue=Verde)
- `Toast` (Para exibir erros 422/503 e sucesso nas operações de caos)

### 5. Topologia Docker (Network e Env Vars)
Estrutura exata do `docker-compose.yml` para blindagem de rede interna:
- **Rede `logistics-net`:** Bridge network customizada isolando os containeres.
- **Service `db`:** Imagem `postgres:15-alpine`. Portas `5432:5432` abertas apenas pro host local. Env: `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`.
- **Service `api`:** Build do `./backend`. Portas `8000:8000`. Depende via `depends_on: [db]`. Env crucial: `DATABASE_URL=postgresql+asyncpg://user:pass@db:5432/logistics`.
- **Service `web`:** Build do `./frontend`. Portas `3000:3000`. Depende via `depends_on: [api]`. Env crucial: `NEXT_PUBLIC_API_URL=http://localhost:8000`.

## Risks / Trade-offs

- **[Escopo de 60h + Frontend + Docker]** → Desenvolver backend, frontend e orquestração Docker em 60h é desafiador. A mitigação é o MVP: o frontend terá apenas telas essenciais, e o Dockerfile focará apenas em execução local, sem pipelines CI/CD complexos.
- **[Simulação vs realidade]** → ETA simulado não reflete rotas reais.
- **[Sem WebSocket]** → O Next.js precisará fazer polling via hooks no cliente (como SWR ou React Query) para simular o tempo real das viaturas. Aceitável para MVP.
- **[Log de ML sem modelo]** → O TCC documentará apenas a coleta estruturada para trabalhos futuros.

## Open Questions

_(resolvidas após o realinhamento de arquitetura)_
