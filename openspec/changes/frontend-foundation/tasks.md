# Tarefas de Implementação: Frontend Foundation

## 1. Ajuste de Fechadura no Backend (Lacuna)
- [ ] 1.1 Em `backend/app/api/deliveries.py`, adicionar a dependência `Depends(require_role("lojista"))` na função `create_delivery` para isolar a criação de rotas nas mãos do dono.

## 2. Boilerplate e Inicialização do Next.js
- [ ] 2.1 Na pasta raiz, rodar comando `npx -y create-next-app@latest frontend --typescript --tailwind --eslint --app --src-dir --import-alias "@/*"` (Modo silencioso/Automático).
- [ ] 2.2 Configurar o pilar do TDD instalando pacotes de testes usando npm: `jest`, `jest-environment-jsdom`, `@testing-library/react`.

## 3. Organização Clean Architecture Genérica
- [ ] 3.1 Construir estrutura pura em `frontend/src`: pastas `infrastructure/api/` e `use_cases/`.
- [ ] 3.2 Montar o script basilar de cliente do Axios `api_client.ts` dentro da infraestrutura focado em bater no nosso backend.

## 4. TDD e Primeira Página (Página Inicial é Login)
- [ ] 4.1 Escrever o teste de fracasso inicial (TDD) em `__tests__/login.test.tsx` assegurando que a Rota Inicial tenha obrigatoriamente inputs para "E-mail" e "Senha".
- [ ] 4.2 Enxugar e transformar `src/app/page.tsx` para seguir o TDD imposto e criar a tela crua e super minimalista do Gateway.

## 5. Testes Unitários de Componentes
- [ ] 5.1 Escrever `__tests__/unit/useAuth.test.ts` validando o hook de autenticação: se `role=lojista` retorna rota `/dashboard`, se `role=motorista` retorna `/drive`.
- [ ] 5.2 Escrever `__tests__/unit/apiClient.test.ts` verificando que o cliente Axios injeta o header `Authorization: Bearer <token>` automaticamente quando o token existe.

## 6. Testes de Integração de Fluxo (MSW)
- [ ] 6.1 Instalar e configurar `msw` (Mock Service Worker) para interceptar chamadas HTTP nas suítes de testes sem precisar do servidor backend ligado.
- [ ] 6.2 Escrever `__tests__/integration/login_flow.test.tsx` cobrindo o fluxo completo: Lojista preenche form → API mock retorna token → middleware redireciona para `/dashboard`.
- [ ] 6.3 Escrever `__tests__/integration/motorista_redirect.test.tsx` cobrindo: Motorista preenche form → API mock retorna token de motorista → sistema redireciona para `/drive`.
- [ ] 6.4 Escrever `__tests__/integration/auth_guard.test.tsx` validando que acessar `/dashboard` sem um token válido resulta em redirecionamento automático para `/`.
