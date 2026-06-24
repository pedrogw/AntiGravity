<!-- BEGIN:nextjs-agent-rules -->
# This is NOT the Next.js you know

This version has breaking changes — APIs, conventions, and file structure may all differ from your training data. Read the relevant guide in `node_modules/next/dist/docs/` before writing any code. Heed deprecation notices.
<!-- END:nextjs-agent-rules -->

<!-- BEGIN:frontend-suggestions -->
# Bloco de Sugestões (próximo ciclo)

- **Polling/auto-refresh** — `fetchDeliveries()` roda só no mount. Um `setInterval` com refetch traria dados frescos para dashboard e drive
- **Dialog "Criar Entrega"** — Botão no dashboard para abrir formulário com select de fábrica, loja, motorista (pré-requisitos implementados: `usePlaces.listFactories`, `usePlaces.listStores`, `useUsers.fetchDrivers`)
- **Filtros na DataTable** — Search por ID, filtro por status, paginação client-side ou server-side
- **Loading skeleton** — Substituir "Carregando..." por shimmer/skeleton enquanto dados carregam
- **Testes de integração** — Coverage para DashboardPage, DrivePage, DeliveryCard, ChaosDevTools, DeliveryDataTable
- **Cache local de deliveries** — Evitar refetch desnecessário ao navegar entre abas
<!-- END:frontend-suggestions -->
