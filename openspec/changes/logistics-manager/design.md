## Context

Projeto greenfield para TCC de BSI (60h). Não há código existente. O sistema será uma API REST de gerenciamento logístico que calcula tempo de entrega (fábrica → loja), permite simulação de eventos de caos que recalculam ETA, e monitora segurança do motorista em rota.

**Constraints:**
- 60 horas de desenvolvimento total
- Sem dependência de APIs externas (mapas simulados)
- API-only (sem frontend separado), mas com Swagger UI customizado
- PostgreSQL obrigatório para estabilidade

## Goals / Non-Goals

**Goals:**
- Arquitetura modular com domínios bem separados (future-proof)
- API REST completa e bem documentada via OpenAPI/Swagger
- Multi-role transparente (operador, lojista, motorista)
- Simulador de caos que recalcula ETA em tempo real
- Sistema de safe-check para segurança do motorista
- Endpoint de demonstração para apresentação na banca

**Non-Goals:**
- Frontend separado (SPA, React, etc.)
- Integração com APIs de mapas reais
- Eventos de caos customizáveis pelo operador
- Legislação de descanso obrigatório (CLT/Lei do Motorista)
- Notificações push ou WebSocket (fora do escopo das 60h)

## Decisions

### 1. Estrutura modular por domínio

**Decisão:** Organizar o código em módulos por domínio de negócio, não por camada técnica.

```
app/
├── main.py
├── core/               # Config, security, database
│   ├── config.py
│   ├── database.py
│   └── security.py
├── auth/               # Autenticação multi-role
│   ├── router.py
│   ├── service.py
│   ├── models.py
│   └── schemas.py
├── deliveries/          # Entregas e ETA
│   ├── router.py
│   ├── service.py
│   ├── models.py
│   └── schemas.py
├── chaos/              # Simulador de caos
│   ├── router.py
│   ├── service.py
│   ├── models.py
│   └── schemas.py
├── safe_check/         # Monitoramento de segurança
│   ├── router.py
│   ├── service.py
│   ├── models.py
│   └── schemas.py
├── locations/          # Fábricas, lojas, janelas
│   ├── router.py
│   ├── service.py
│   ├── models.py
│   └── schemas.py
└── demo/               # Endpoint de demonstração
    ├── router.py
    └── service.py
```

**Alternativas consideradas:**
- Monolito por camada (models/, routes/, services/) — descartado por baixa coesão ao escalar
- Microserviços — descartado por overhead excessivo para 60h

**Rationale:** Cada módulo é auto-contido com seus modelos, schemas, serviços e rotas. Facilita testes, manutenção e futura migração para microserviços.

### 2. Cálculo de ETA simulado

**Decisão:** `ETA = distância_km / velocidade_media_kmh` com coordenadas (lat/lng) usando fórmula de Haversine para distância.

**Alternativas consideradas:**
- API de mapas real (Google/ORS) — descartado por dependência externa e custo
- Distância em linha reta sem Haversine — descartado por imprecisão em distâncias grandes

**Rationale:** Haversine dá precisão suficiente para demonstração. Velocidade média configurável por tipo de rota (urbana: 40 km/h, rodovia: 80 km/h).

### 3. Mecanismo de caos

**Decisão:** Cada evento de caos tem um `impact_factor` (multiplicador de tempo) e um `delay_minutes` (atraso fixo adicional).

| Evento | impact_factor | delay_minutes |
|---|---|---|
| Chuva | 1.3 (30% mais lento) | 0 |
| Alagamento | 1.0 (bloqueio) | 45 |
| Engarrafamento | 1.5 (50% mais lento) | 15 |
| Acidente | 1.0 (bloqueio) | 60 |

**Recálculo:** `novo_ETA = (ETA_original × impact_factor) + delay_minutes`

Múltiplos eventos se acumulam multiplicativamente nos `impact_factor` e aditivamente nos `delay_minutes`.

### 4. Safe-Check com ping/timer

**Decisão:** Quando o motorista reporta velocidade = 0 km/h (ou não atualiza posição por > 10 min), o sistema gera um `ping` com timer de 5 minutos. Se não responder, gera alerta nível ALTO. Se posição desviar > 2 km da rota, alerta CRÍTICO imediato.

**Alternativas consideradas:**
- Apenas alerta automático sem ping — descartado por excesso de falsos positivos
- GPS real-time contínuo — descartado por complexidade (necessitaria WebSocket)

**Rationale:** O motorista faz atualizações periódicas via API (simula o app do motorista). O safe-check analisa essas atualizações.

### 5. Autenticação JWT multi-role

**Decisão:** JWT com claims de `role` (operador/lojista/motorista). Dependency injection do FastAPI para guards por role.

**Rationale:** Padrão FastAPI, sem overhead de OAuth2 completo. Suficiente para demonstrar controle de acesso.

### 6. PostgreSQL com SQLAlchemy 2.0 async

**Decisão:** asyncpg + SQLAlchemy 2.0 async ORM. Alembic para migrações.

**Rationale:** Performance async nativa, type safety com mapped_column, migrações versionadas.

## Risks / Trade-offs

- **[Escopo de 60h]** → Manter YAGNI estrito; features só entram se completam um ciclo funcional inteiro
- **[Simulação vs realidade]** → O ETA simulado não reflete rotas reais → clarificar na documentação do TCC que é um modelo simplificado
- **[Safe-check sem GPS real]** → O motorista atualiza posição manualmente via API → na apresentação, simular com o endpoint de demo
- **[Sem WebSocket]** → Lojista precisa fazer polling para ver atualizações de ETA → aceitável para MVP

## Open Questions

- Timer do safe-check: 5 minutos é adequado? (decisão razoável, pode ajustar)
- Distância de desvio: 2 km é o limiar correto? (depende do tipo de rota)
