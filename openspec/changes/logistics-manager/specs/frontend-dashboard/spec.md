## Context

Esta spec define a aplicação Frontend em Next.js para controle do sistema logístico.

## ADDED Requirements

### Requirement: Dashboard do Lojista Analítico
O sistema SHALL prover uma interface web reativa B2B em Tailwind/shadcn onde o dono da carga monitora a frota viva aguardando os cruzamentos entre ETA vs Janela de Recebimentos.

#### Scenario: Lojista visualiza painel de SLAs
- **GIVEN** um Lojista validamente autenticado no token
- **WHEN** acessa livre a hierarquia visual por `/dashboard`
- **THEN** o sistema SHALL renderizar a Data Table de entregas amarradas a ele. Trazendo ETA atual e os alertas de estouro do Safe-Check lazy.

#### Scenario: Injeção Tática (Modo Banca / DevTools)
- **GIVEN** um avaliador demonstrando resiliência matemática na tela de entrega ativa
- **WHEN** aciona as DevTools visuais (Botão Caos Invisível) injetando um "Acidente (Delay de 1h)"
- **THEN** o frontend dispara hook server-action atualizando sem refresh e mudando badge do painel lido pelo lojista.

#### Scenario: Recepção passiva Lojista SLA Críticos
- **GIVEN** Lojista com dashboard aberto localmente
- **WHEN** o Safe-Check de Back-end expirar o Lojista no lazy evaluation de delta timestamps
- **THEN** card vermelho em destaque na lib Shadcn-UI notifica "Contato Perdido / Reroute"

### Requirement: Visão do Motorista (Simulador Mobile)
O sistema SHALL prover uma interface dedicada ao motorista para simular suas interações de campo (reroute e paradas) a fim de alimentar o sistema de Safe-Check.

#### Scenario: Motorista informa Reroute
- **GIVEN** o motorista autenticado visualizando as informações de sua carga atual
- **WHEN** o motorista clica no grande botão "Informar Rota Alternativa / Reroute" preenchendo as coordenadas atuais lat/lng
- **THEN** o frontend envia os dados para a API, que recalcula a distância restante e devolve o ETA atualizado para a interface do motorista

#### Scenario: Motorista força parada prolongada
- **GIVEN** o motorista em rota constante
- **WHEN** o motorista pressiona o botão "Informar Parada (Velocidade 0km/h)"
- **THEN** o frontend aciona o endpoint de posição com velocidade 0, engatilhando as regras estruturais de lazy evaluation (ping) do backend

## Implementation Details

- O Frontend rodará nativamente na raiz `/frontend` do repositório (Monorepo).
- O comando padrão de execução será `npm run dev`.
- O CORS do backend (FastAPI) em `app/main.py` será configurado explicitamente para liberar o tráfego do `http://localhost:3000`.
- Para poupar tempo nas 60h, as telas de configurações de `Locais` (Fábrica/Lojas) e criação de `Entregas` podem ser omitidas do Frontend e criadas exclusivamente via Swagger GUI. O frontend foca na exibição do Monitoramento e na prova de conceito do Caos/Reroute.
- As chamadas de fetch deverão encaminhar o token Bearer JWT amarrado ao Lojista ou Motorista autenticado.
