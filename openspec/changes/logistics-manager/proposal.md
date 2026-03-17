## Why

Projeto de TCC para Bacharelado em Sistemas de Informação (BSI) com carga de 60 horas. O setor logístico brasileiro sofre com imprevisibilidade no tempo de entrega — eventos como chuvas, alagamentos, engarrafamentos e acidentes alteram drasticamente o ETA sem que lojistas ou operadores tenham visibilidade em tempo real. Além disso, a segurança do motorista e da carga exige monitoramento contínuo para detecção rápida de anomalias (parada inesperada, desvio de rota). O sistema também acumula dados estruturados de incidentes para futura aplicação de modelos preditivos (ML).

## What Changes

- Criação de um sistema completo de gerenciamento logístico via API REST (FastAPI) com tipagem estrita via Pydantic v2
- Criação de uma interface Frontend em Next.js (App Router), TypeScript obrigatório, TailwindCSS e shadcn/ui.
- Orquestração completa via Docker e docker-compose (Frontend, Backend, PostgreSQL).
- Banco de dados PostgreSQL acessado via SQLAlchemy 2.0 (async).
- Cálculo de ETA simulado (distância ÷ velocidade média) entre fábrica e loja via Haversine
- Sistema multi-role com 3 perfis: Operador (admin), Lojista e Motorista
- Janela de recebimento configurável por loja (horários em que aceita entregas)
- Simulador de Caos com 4 tipos de evento: chuva, alagamento, engarrafamento, acidente
- Rota fixa — eventos de caos só recalculam tempo, não alteram a rota
- Recálculo automático de ETA quando eventos de caos são injetados (múltiplos eventos se acumulam)
- Reroute pelo motorista: motorista pode informar mudança de rota, sistema recalcula distância restante
- Histórico de ETA registrado a cada mudança (jornada do ETA ao longo da entrega)
- Log de eventos de caos permanente para acúmulo de dados de ML futuro
- Safe-Check de segurança: ping com lazy evaluation quando velocidade = 0 km/h, alerta imediato se desvio de rota
- Paginação com limit/offset e defaults em todos os endpoints de listagem
- Timestamps internos em UTC (TIMESTAMP WITH TIME ZONE)
- Endpoint de demo que simula o fluxo completo (rota → caos → recálculo → alerta)

## Capabilities

### New Capabilities
- `auth-multi-role`: Autenticação JWT com 3 roles (operador, lojista, motorista) e controle de acesso por endpoint
- `eta-calculator`: Motor de cálculo de ETA simulado com Haversine, recálculo dinâmico e histórico de ETAs
- `delivery-management`: CRUD de entregas, ciclo de vida, reroute pelo motorista e paginação com defaults
- `receiving-window`: Configuração de janela de recebimento por loja com validação de horário em UTC
- `chaos-simulator`: Injeção de eventos de caos que afetam ETA em tempo real + log permanente para ML futuro
- `safe-check`: Monitoramento de segurança com ping/lazy evaluation e alerta por desvio de rota
- `demo-endpoint`: Endpoint de demonstração que orquestra o fluxo completo para apresentação
- `frontend-dashboard`: Interface web (Next.js/Tailwind/shadcn) consumindo a API para visualização e injeção do caos (Operador/Lojista).

### Modified Capabilities
_(nenhuma — projeto greenfield)_

## Impact

- **Banco de dados**: Schema PostgreSQL com tabelas para usuários, fábricas, lojas, entregas, eventos de caos, janelas de recebimento, alertas, histórico de ETA e log de caos para ML. Todos os timestamps em UTC. Postgres gerenciado via SQLAlchemy 2.0.
- **APIs**: ~35 endpoints REST (FastAPI) organizados por domínio (auth, deliveries, chaos, safe-check, demo) com validação estrita via Pydantic v2.
- **Frontend**: Aplicação Next.js (App Router) em TypeScript para consumo visual das rotas, focada nas visões de Operador (painel de caos) e Motorista. Estilização apenas via TailwindCSS e componentes baseados no ecossistema shadcn/ui.
- **Dependências**: FastAPI, SQLAlchemy 2.0 async, asyncpg, Pydantic V2, python-jose (JWT), Alembic. No Front: Next.js, React, Tailwind, lucide-react.
- **Infraestrutura**: Orquestração via `docker-compose`. Containers independentes para `backend`, `frontend`, e `db` (PostgreSQL local). Monorepo contendo pastas `backend` e `frontend`, sem dependência de APIs externas de mapas.
