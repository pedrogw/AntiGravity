# UI/UX Design Proposal: Logistics Manager

Com base no projeto "Logistics Manager" e utilizando a skill `ui-ux-pro-max`, aqui está a proposta de Design System e experiência de usuário (UX) para a interface do sistema, focando em um painel profissional de logística e rastreamento em tempo real.

## 1. Padrão de Design (Design System)

- **Padrão (Pattern):** Dashboard Rico em Funcionalidades + Dados em Tempo Real
- **Estilo Visual:** Painel Financeiro / Tracking Profissional
- **Atributos:** Analítico, preciso, confiável, focado em monitoramento de métricas e alertas (caos/ETA).
- **Acessibilidade:** Padrão de contraste WCAG AAA para uso contínuo (modo claro/escuro com alto contraste).

## 2. Paleta de Cores

A paleta foi escolhida para mesclar "rastreamento e segurança" (Azul) com "alertas e chamadas para ação" (Laranja).

| Função | Cor Hexadecimal | Aplicação |
|--------|----------------|-----------|
| **Principal** | `#2563EB` (Azul) | Barra de navegação, botões primários, ícones de status "Em rota" |
| **Secundária** | `#3B82F6` (Azul Claro) | Elementos interativos secundários, backgrounds de ícones |
| **Atenção/CTA** | `#F97316` (Laranja) | Alertas de eventos de caos, atrasos no ETA, notificações críticas |
| **Fundo (Light)**| `#EFF6FF` (Azul Gelo) | Fundo da aplicação para reduzir o cansaço visual em relação ao branco puro |
| **Texto/Base** | `#1E40AF` (Azul Escuro) | Texto principal de dados e tabelas para garantir legibilidade |
| **Alerta Crítico**| `#EF4444` (Vermelho) | Safe-Check falho ou desvio de rota crítico detectado |

## 3. Tipografia

A escolha da tipografia visa passar a sensação de "precisão analítica e tecnológica".

- **Títulos e Dados (Números):** `Fira Code` (Monosapce)
  *Excelente para tabelas, contadores de tempo (ETA) e identificadores de carga.*
- **Corpo e Textos Longos:** `Fira Sans` (Sans-serif)
  *Garante legibilidade em telas com alta densidade de informações.*

**Importação CSS/Tailwind:**
```css
@import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500;600;700&family=Fira+Sans:wght@300;400;500;600;700&display=swap');
```

## 4. Efeitos e Animações (Micro-interações)

- **Contadores (ETA):** Animações suaves nos números ao recalcularem o ETA (ex: quando um evento de caos é injetado).
- **Indicadores de Tendência:** Setas para cima/baixo para tempo ganho ou perdido com mudança de cor suave.
- **Transições de Status:** O card de uma entrega deve pulsar levemente ou alterar o contorno (+ shadow) quando o "Simulador de Caos" for acionado ou o `Safe-Check` iniciar o ping.

## 5. Práticas e Anti-Padrões (O que EVITAR)

- 🚫 **Evitar Rastreamento Estático:** O dashboard não pode parecer morto. Mesmo sem WebSockets, use um *polling* visualmente confortável ou atualizações em lote.
- 🚫 **Evitar Cores Excessivas na Tabela:** Use cores (laranja/vermelho) apenas para exceções (caos/atraso) e mantenha entregas normais neutras.
- 🚫 **Uso de Emojis como Ícones:** Utilizar bibliotecas profissionais em SVG (ex: *Lucide Icons* ou *Heroicons*, nativos do `shadcn/ui`).
- 🚫 **Falta de Feedback no Hover:** Todas as linhas das tabelas (entregas) e botões devem responder em 150-300ms a interações do mouse.

## 6. Layout Recomendado por Role (Perfil)

Uma vez que o backend prevê 3 perfis, a interface (`Next.js` + `Shadcn/UI`) deve se adaptar:

1. **Operador (Admin):** 
   - Visão "Torre de Controle". Cards superiores com agregados (Entregas hoje, % Atrasadas, Alertas Ativos).
   - Tabela densa com paginação e busca.
   - Painel lateral de "Simulador de Caos" (botões rápidos de injeção de chuva, acidente, etc.).
2. **Lojista:** 
   - Focado apenas em suas cargas a receber.
   - Visão em Kanban simples (Pendente, A Caminho, Chegou) baseada em ETA.
   - Configuração visual para a "Janela de Recebimento".
3. **Motorista (Visão Mobile-First):**
   - Inteface limpa com "Ação Única": Botão "Reportar Rota/Congestionamento" bem saliente (CTA Laranja).
   - Indicador visual do `Safe-Check` em andamento.

---

> **Nota para integração:** Esta proposta expande os Objetivos do TCC para caso a construção do frontend completo (`Next.js` + `Tailwind` listado nas _tech stacks_) seja aprovada. Deseja incorporar este documento de design aos artefatos oficiais na pasta de mudanças do OpenSpec?
