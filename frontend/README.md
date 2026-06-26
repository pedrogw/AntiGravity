# AntiGravity — Frontend

Interface web do motor analítico de logística, construída com Next.js App Router + TypeScript + TailwindCSS + shadcn/ui.

## Scripts

```bash
npm run dev      # Desenvolvimento (localhost:3000)
npm test         # Testes (Vitest)
npm run lint     # ESLint
npm run build    # Build de produção
```

## Estrutura

```
src/
├── domain/           → Entidades, protocolos, erros, value objects
├── application/      → Use cases
├── infrastructure/   → API client, repositórios HTTP, armazenamento, DI
├── hooks/            → useAuth, useDeliveries, usePlaces, useAlerts, useUsers
├── components/       → LoginForm, AuthGuard, dashboard/, driver/, ui/
├── mocks/            → MSW handlers para testes
└── app/              → Páginas (login, dashboard, drive)
```

## Variáveis de Ambiente

| Variável | Descrição |
|----------|-----------|
| `NEXT_PUBLIC_API_URL` | URL do backend (ex: `http://localhost:8000`) |

## Testes

```bash
npm test          # 143 testes, 0 falhas
npm run lint      # 0 erros, 0 warnings
npx next build    # Compila sem erros
```
