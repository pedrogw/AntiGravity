## Context

Esta spec define a aplicação Frontend em Next.js para controle do sistema logístico.

## ADDED Requirements

### Requirement: Dashboard do Operador / Lojista
O sistema SHALL prover uma interface web para operadores e lojistas que exiba a listagem de entregas paginada, detalhes do ETA original/recalculado, injeção de caos e alertas críticos. A interface MUST ser construída exclusivamente com componentes TailwindCSS e shadcn/ui.

#### Scenario: Visualização do painel principal
- **GIVEN** um operador logístico validamente autenticado
- **WHEN** o operador acessa a rota `/dashboard`
- **THEN** o sistema SHALL carregar a tabela paginada de entregas ativas consumindo a API do backend via fetch com token JWT

#### Scenario: Injeção visual de caos
- **GIVEN** que o operador abriu os detalhes de uma entrega com status "em_transito"
- **WHEN** o operador seleciona o botão de "Injetar Caos" e escolhe a opção "Acidente"
- **THEN** o frontend dispara o POST para a API correspondente e atualiza imediatamente a UI refletindo o novo ETA afetado

#### Scenario: Recepção de Alertas Críticos
- **GIVEN** que o dashboard do operador está aberto e ativo
- **WHEN** o backend emite um alerta nível CRÍTICO (ex: desvio de rota do motorista)
- **THEN** a interface web MUST exibir visualmente esse card de alerta no painel consumindo o endpoint de polling de alertas

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
- As chamadas de fetch deverão encaminhar o token Bearer JWT de quem estiver autenticado (Operador, Lojista ou Motorista).
