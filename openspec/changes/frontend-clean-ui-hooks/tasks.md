## 1. Criação dos Custom Hooks

- [x] 1.1 Criar diretório `src/hooks/`
- [x] 1.2 Criar o hook `useAuth.ts` contendo a lógica de extração do token, controle de `isLoading`, `error` e a função `login(email, pass)` extraída da página principal

## 2. Refatoração de Componentes UI

- [x] 2.1 Mover marcação de formulário pesada do `src/app/page.tsx` para o novo componente `src/components/LoginForm.tsx`
- [x] 2.2 Configurar o `LoginForm` para aceitar `props` puras (estado e callbacks, como `onSubmit`) e garantir tipagem estrita com TypeScript

## 3. Orquestração e Validação

- [x] 3.1 Atualizar `src/app/page.tsx` para instanciar o hook `useAuth` e passar seus dados e callbacks para a renderização do `<LoginForm>`
- [x] 3.2 Rodar os testes existentes (ex: `npm run test` para `login_flow.test.tsx`) e assegurar que a refatoração passou no ciclo (GREEN) sem quebrar o comportamento do usuário final
