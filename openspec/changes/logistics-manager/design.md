## Context

Projeto greenfield para TCC de BSI (60h). Não há código existente. O sistema será uma API REST de gerenciamento logístico que calcula tempo de entrega (fábrica → loja), permite simulação de eventos de caos que recalculam ETA, monitora segurança do motorista em rota, e acumula dados estruturados de incidentes para futura aplicação de modelos preditivos.

**Constraints:**
- 60 horas de desenvolvimento total
- Sem dependência de APIs externas (mapas simulados)
- API-only (sem frontend separado), mas com Swagger UI customizado
- PostgreSQL obrigatório para estabilidade
- Todos os timestamps em UTC internamente

## Goals / Non-Goals

**Goals:**
- Arquitetura modular com domínios bem separados (future-proof)
- API REST completa e bem documentada via OpenAPI/Swagger
- Multi-role transparente (operador, lojista, motorista)
- Simulador de caos que recalcula ETA em tempo real (rota fixa, só tempo muda)
- Reroute pelo motorista quando ele efetivamente muda de rota
- Histórico de ETA + log de caos para acúmulo de dados de ML futuro
- Sistema de safe-check com lazy evaluation para segurança do motorista
- Paginação com defaults em todos os endpoints de listagem
- Endpoint de demonstração para apresentação na banca

**Non-Goals:**
- Frontend separado (SPA, React, etc.)
- Integração com APIs de mapas reais
- Eventos de caos customizáveis pelo operador (só os 4 pré-definidos)
- Treinamento de modelos de ML (só acúmulo de dados)
- Legislação de descanso obrigatório (CLT/Lei do Motorista)
- Notificações push ou WebSocket (fora do escopo das 60h)

## Decisions

### 1. Estrutura modular por domínio

**Decisão:** Organizar o código em módulos por domínio de negócio, não por camada técnica.

```
app/
├── main.py
├── core/               # Config, security, database, pagination
│   ├── config.py
│   ├── database.py
│   ├── security.py
│   └── pagination.py
├── auth/               # Autenticação multi-role
│   ├── router.py
│   ├── service.py
│   ├── models.py
│   └── schemas.py
├── deliveries/          # Entregas, ETA e reroute
│   ├── router.py
│   ├── service.py
│   ├── models.py
│   └── schemas.py
├── chaos/              # Simulador de caos + log para ML
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

### 3. Mecanismo de caos — rota fixa, só tempo muda

**Decisão:** Cada evento de caos tem um `impact_factor` (multiplicador de tempo) e um `delay_minutes` (atraso fixo adicional). A rota NÃO muda — eventos só afetam o tempo estimado.

| Evento | impact_factor | delay_minutes |
|---|---|---|
| Chuva | 1.3 (30% mais lento) | 0 |
| Alagamento | 1.0 (bloqueio) | 45 |
| Engarrafamento | 1.5 (50% mais lento) | 15 |
| Acidente | 1.0 (bloqueio) | 60 |

**Recálculo:** `novo_ETA = (ETA_restante × impact_factor) + delay_minutes`

Múltiplos eventos se acumulam multiplicativamente nos `impact_factor` e aditivamente nos `delay_minutes`.

**Alagamento/Acidente:** São bloqueios — motorista espera liberar (delay fixo). Se o motorista optar por mudar de rota, usa o endpoint de reroute.

### 4. Reroute pelo motorista

**Decisão:** O motorista pode informar que mudou de rota via `POST /deliveries/{id}/reroute` com sua posição atual (lat/lng). O sistema recalcula a distância restante (posição atual → loja) usando Haversine, aplica eventos de caos ativos e registra no histórico de ETA.

**Rationale:** Mantém a rota fixa como padrão (simples), mas permite ao motorista "resetar" a rota quando efetivamente decide ir por outro caminho.

### 5. Safe-Check com lazy evaluation

**Decisão:** Quando o motorista reporta velocidade = 0 km/h (ou não atualiza posição por > 10 min), o sistema gera um `ping` com timer de 5 minutos. A expiração do ping é verificada por **lazy evaluation** — quando qualquer consulta é feita ao ping, o sistema compara `now() > expires_at`. Se expirou, gera o alerta naquele momento. Se posição desviar > 2 km da rota, alerta CRÍTICO imediato.

**Alternativas consideradas:**
- Background task / cron para checar pings — descartado por overhead e complexidade
- Apenas alerta automático sem ping — descartado por excesso de falsos positivos
- GPS real-time contínuo — descartado por complexidade (necessitaria WebSocket)

**Rationale:** Lazy evaluation = zero overhead em idle. O alerta é criado sob demanda, quando alguém consulta.

### 6. Autenticação JWT multi-role

**Decisão:** JWT com claims de `role` (operador/lojista/motorista). Dependency injection do FastAPI para guards por role.

**Rationale:** Padrão FastAPI, sem overhead de OAuth2 completo. Suficiente para demonstrar controle de acesso.

### 7. PostgreSQL com SQLAlchemy 2.0 async + UTC

**Decisão:** asyncpg + SQLAlchemy 2.0 async ORM. Alembic para migrações. Todos os campos de data/hora usam `TIMESTAMP WITH TIME ZONE` e armazenam em UTC.

**Rationale:** Performance async nativa, type safety com mapped_column, migrações versionadas. UTC evita bugs de timezone em sistema nacional (Manaus UTC-4, São Paulo UTC-3, etc.).

### 8. Paginação com defaults

**Decisão:** Todos os endpoints de listagem aceitam `limit` (default=20) e `offset` (default=0). Resposta inclui `total`, `limit`, `offset` e `items`. Implementado como dependency reutilizável em `core/pagination.py`.

**Rationale:** Padrão profissional, não sobrecarrega sistema nem exige configuração do consumidor.

### 9. Histórico de ETA + log de caos para ML

**Decisão:** Duas tabelas adicionais:
- `eta_history`: registra cada mudança de ETA (before, after, reason, timestamp) — permite visualizar "jornada do ETA"
- `chaos_event_log`: backup permanente de todos os eventos de caos com contexto geográfico — nunca deletado, acumula dados para futura análise de ML

**Rationale:** O `eta_history` é valor imediato (demonstração na banca: "veja como o ETA mudou"). O `chaos_event_log` é visão de futuro (TCC pode argumentar "dados estruturados preparados para modelos preditivos").

## Risks / Trade-offs

- **[Escopo de 60h]** → Manter YAGNI estrito; features só entram se completam um ciclo funcional inteiro. Os 5 gaps adicionais somam ~8h, dentro da margem.
- **[Simulação vs realidade]** → O ETA simulado não reflete rotas reais → clarificar na documentação do TCC que é um modelo simplificado
- **[Safe-check sem GPS real]** → O motorista atualiza posição manualmente via API → na apresentação, simular com o endpoint de demo
- **[Lazy evaluation de pings]** → Se ninguém consultar o ping, o alerta atrasa → aceitável pois operador faz polling periódico
- **[Log de ML sem modelo]** → Acumula dados mas não treina modelo → clarificar no TCC que é preparação para trabalho futuro
- **[Sem WebSocket]** → Lojista precisa fazer polling para ver atualizações de ETA → aceitável para MVP

## Open Questions

_(todas resolvidas durante exploração)_
