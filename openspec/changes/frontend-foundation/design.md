# Design Técnico: Frontend Foundation & Clean Architecture

## 1. Stack e Tecnologia
- **Framework Core**: Next.js 15 (App Router).
- **Estilização Atômica**: Tailwind CSS.
- **Componentização e TDD**: React Testing Library + Jest + Shadcn UI para alta fidelidade gráfica imediata.

## 2. Clean Architecture no Ecossistema Visual
Para fugir da armadilha de ter regras de negócio jogadas no código dos botões, estruturaremos a pasta `src`:
*   `src/infrastructure/api` -> Onde o `axios` sequestrará os tokens e falará com a porta 8000 (Backend).
*   `src/domain` e `src/use_cases` -> Onde testaremos as regras que dizem "Se Papel==Motorista, vá para /drive".
*   `src/app` -> Camada de Apresentação visual limpa.

## 3. Filosofia de Gateway (Rota /) e Mapeamento
*   A página principal (`src/app/page.tsx`) é **estritamente dedicada à biometria digital da aplicação (Login)**. 
*   Sub-rotas planejadas (Mock):
    *   `/dashboard`: Reduto do Lojista (Administra inbound e fornecedores).
    *   `/drive`: Interface mobile-first agressiva do Caminhoneiro (Envia pings).

## 4. Retificação do Backend (Lacuna de Segurança)
Prevendo a nova vida em que a Fábrica é só Geografia e o Lojista é o Deus do seu Inbound, iremos preencher a pequena brecha encontrada mapeando o endpoint `/deliveries/` em `app/api/deliveries.py` para exigir via RBAC exclusivamente a chave mestre do `lojista`.

## 5. Estratégia de Testes: Unitários + Integração
A Suíte de Testes do Frontend será dividida em dois níveis complementares:

### 5.1 Testes Unitários (Isolamento de Componentes)
*   **Ferramenta**: Jest + React Testing Library.
*   **Foco**: Cada componente visual testado de forma isolada (sem rede, sem banco).
*   **Exemplos**:
    *   `LoginForm.test.tsx` → Verifica se o botão de "Entrar" existe na tela.
    *   `useAuth.test.ts` → Verifica se o hook de autenticação redireciona corretamente baseado na *role* retornada.
    *   `apiClient.test.ts` → Verifica se o cliente Axios injeta o header `Authorization` quando o token existe no `localStorage`.

### 5.2 Testes de Integração (Fluxos Ponta a Ponta no Frontend)
*   **Ferramenta**: React Testing Library com `msw` (Mock Service Worker) para simular as respostas do Backend FastAPI sem precisar que o servidor esteja ligado.
*   **Foco**: Testar o fluxo completo de uma interação do usuário atravessando múltiplas camadas (UI → `use_case` → `api_client` → resposta mockada).
*   **Exemplos de Fluxos Críticos**:
    *   `login_flow.test.tsx` → Preenche os campos de e-mail e senha, clica em "Entrar", a API mock devolve `role: lojista` e o teste verifica o redirecionamento para `/dashboard`.
    *   `motorista_redirect.test.tsx` → Mesma sequência, mas API mock devolve `role: motorista` e valida redirecionamento para `/drive`.
    *   `auth_guard.test.tsx` → Tenta acessar `/dashboard` sem token e verifica redirecionamento automático de volta para `/`.
