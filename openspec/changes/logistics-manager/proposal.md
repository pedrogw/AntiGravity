## Why

Projeto de TCC para Bacharelado em Sistemas de Informação (BSI) com carga de 60 horas. O setor logístico brasileiro sofre com imprevisibilidade no tempo de entrega — eventos como chuvas, alagamentos, engarrafamentos e acidentes alteram drasticamente o ETA sem que lojistas ou operadores tenham visibilidade em tempo real. Além disso, a segurança do motorista e da carga exige monitoramento contínuo para detecção rápida de anomalias (parada inesperada, desvio de rota).

## What Changes

- Criação de um sistema completo de gerenciamento logístico via API REST (FastAPI)
- Cálculo de ETA simulado (distância ÷ velocidade média) entre fábrica e loja
- Sistema multi-role com 3 perfis: Operador (admin), Lojista e Motorista
- Janela de recebimento configurável por loja (horários em que aceita entregas)
- Simulador de Caos com 4 tipos de evento: chuva, alagamento, engarrafamento, acidente
- Recálculo automático de ETA quando eventos de caos são injetados
- Safe-Check de segurança: ping com timer quando velocidade = 0 km/h, alerta imediato se desvio de rota
- Swagger UI customizado para demonstração na banca
- Endpoint de demo que simula o fluxo completo (rota → caos → recálculo → alerta)

## Capabilities

### New Capabilities
- `auth-multi-role`: Autenticação JWT com 3 roles (operador, lojista, motorista) e controle de acesso por endpoint
- `eta-calculator`: Motor de cálculo de ETA simulado com fórmula distância/velocidade e suporte a recálculo dinâmico
- `delivery-management`: CRUD de entregas, atribuição de motorista, rastreamento de status do ciclo de vida
- `receiving-window`: Configuração de janela de recebimento por loja com validação de horário
- `chaos-simulator`: Injeção de eventos de caos (chuva, alagamento, engarrafamento, acidente) que afetam ETA em tempo real
- `safe-check`: Monitoramento de segurança com ping/timer em parada e alerta por desvio de rota
- `demo-endpoint`: Endpoint de demonstração que orquestra o fluxo completo para apresentação

### Modified Capabilities
_(nenhuma — projeto greenfield)_

## Impact

- **Banco de dados**: Schema PostgreSQL com tabelas para usuários, fábricas, lojas, rotas, entregas, eventos de caos, janelas de recebimento e alertas
- **APIs**: ~30 endpoints REST organizados por domínio (auth, deliveries, chaos, safe-check, demo)
- **Dependências**: FastAPI, SQLAlchemy 2.0 async, asyncpg, Pydantic V2, python-jose (JWT), passlib
- **Infraestrutura**: PostgreSQL local, sem dependências externas de APIs de mapas
