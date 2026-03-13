# Stitch Prompts: Logistics Manager Dashboard (Refined)

Estes prompts foram refinados para incluir a experiência completa de autenticação e fluxos personalizados por função (*role*), mantendo a estética **minimalista e industrial**.

---

## 1. Tela de Login (Acesso Unificado)

> **Prompt:**
> "Crie uma tela de login ultra-minimalista para um sistema de logística industrial. Centralize um card branco com bordas sutis (#E2E8F0) sobre um fundo fosco (#EFF6FF). Inclua campos limpos para 'Usuário' e 'Senha' com foco em tipografia Fira Sans. Abaixo, adicione um seletor visual discreto ou abas (Tabs) para escolher o tipo de acesso: 'Motorista', 'Lojista' ou 'Fornecedor/Operador'. O botão de 'Entrar' deve ser Primário (#2563EB) com transição de 200ms no hover. Sem logos complexos, use apenas um ícone de 'Caminhão' estilizado em SVG no topo."

---

## 2. Layouts por Função (Pós-Login)

### A. Visão do Motorista (Caminhoneiro) - *Mobile-First*
> **Prompt:**
> "Gere a interface para o Motorista (uso em smartphone). Foco total em uma única entrega ativa. Destaque um card grande com o 'ETA Atual' em fonte Fira Code negrito. Abaixo, um botão de destaque Laranja (#F97316) para 'Reportar Evento (Caos)'. Inclua uma seção de 'Safe-Check' com um sinalizador de status pulsante verde. Minimalismo extremo: remova barras laterais, use apenas navegação inferior com ícones: 'Entrega', 'Mapa', 'Perfil'."

### B. Visão do Lojista (Shopkeeper) - *Gestão de Recebimento*
> **Prompt:**
> "Crie o dashboard do Lojista. Foco em 'Cargas Planejadas'. Use um layout de colunas limpo (Board estilo Kanban) para separar: 'A Caminho', 'Na Janela' e 'Recebido'. Cada card de entrega deve mostrar o ETA e o ID. Adicione um pequeno painel superior para 'Configurar Janela de Recebimento' com seletores de horário minimalistas. Cores calmas (Azul Secundário #3B82F6) para indicar organização e pontualidade."

### C. Visão do Fornecedor/Operador (Admin) - *Torre de Controle*
> **Prompt:**
> "Crie a 'Torre de Controle' para o Operador. Interface de alta densidade de dados (tabelas e mapas compactos). Painel lateral fixo à direita contendo o 'Simulador de Caos' com botões rápidos. Lista de alertas críticos no topo com bordas vermelhas sutis (#EF4444). Use o layout 'Bento Box' para agrupar métricas globais de frota e status das fábricas. Estética técnica e profissional (Fira Code para todos os números)."

---

## 3. Diretrizes de Fluxo e Transição (Stitch Logic)

Para o prototipador entender a transição entre telas:

- **Login to Dashboard:** "Ao clicar em 'Entrar', simule um fade-out suave da tela de Login e carregue o layout correspondente à aba selecionada (Motorista/Lojista/Operador)."
- **Feedback de Erro:** "Se os campos estiverem vazios, mostre um contorno vermelho fino no input com uma mensagem de erro minimalista abaixo ('Campo obrigatório')."
- **Navigation:** "Mantenha a barra de navegação superior (Operador/Lojista) ou inferior (Motorista) consistente em todas as telas internas para evitar deslocamento visual."

---

> [!IMPORTANT]
> **Consistência:** Certifique-se de que o seletor de função no Login (`Motorista`, `Lojista`, `Operador`) dite qual prompt de layout (A, B ou C) será renderizado em seguida. Isso ajuda a criar um protótipo coeso no Stitch.
