    ## FASE 1: Infraestrutura Base (Docker e PostgreSQL)
- [ ] 1.1 Criar estrutura de pastas root: `backend/` e `frontend/`.
- [ ] 1.2 Criar arquivo `docker-compose.yml` na raiz mapeando apenas o serviço `db` (postgres:15-alpine) com porta 5432 e variáveis de ambiente (User, Password, DB).
- [ ] 1.3 **Validação:** Rodar `docker-compose up -d db` e garantir via logs (`docker logs db`) que o banco PostgreSQL subiu e está aceitando conexões na porta 5432.

## FASE 2: Core do Backend (FastAPI + Pydantic + SQLAlchemy)
- [ ] 2.1 No `backend/`: Inicializar projeto Python com dependências (fastapi, uvicorn, sqlalchemy, asyncpg, pydantic, alembic, passlib, python-jose).
- [ ] 2.2 Criar `Dockerfile` do backend, definir volumes de dev e adicioná-lo ao `docker-compose.yml`. Configurar CORS no FastAPI.
- [ ] 2.3 Configurar Database Engine (SQLAlchemy Async), Base Declarative e Alembic.
- [ ] 2.4 Criar Modelos e Schemas base: Users, Factories, Stores, Deliveries, EtaHistory, ChaosEvents, Alerts.
- [ ] 2.5 Gerar e rodar migração Alembic para construir as tabelas no banco de dados da Fase 1.
- [ ] 2.6 Criar Router de Autenticação (Registro e JWT Login) e plugar no `main.py`.
- [ ] 2.7 Construir Lógica e Endpoints de CRUD Logístico: Locais, Janelas de Recebimento e Gerenciamento de Entregas.
- [ ] 2.8 **(TDD Loop RED)**: Instalar `pytest` e criar a pasta `tests/domain/`. Escrever **obrigatoriamente >30 testes automatizados de CÓDIGO (unitários/integração)** FALHOS baseados nas referências BDD (`specs/`) para o Motor Analítico (Cálculo Haversine, ETA, Simulador de Caos e Lazy Evaluation do SafeCheck) antes da aplicação no backend.
- [ ] 2.9 **(TDD Loop GREEN)**: Implementar a lógica pura do Motor Analítico em `app/domain/` até todos os 30+ assertions escritos no passo 2.8 passarem.
- [ ] 2.10 Criar Exception Handler Global no FastAPI para interceptar erros de banco de dados (503) e validação (422) e criar seed script.
- [ ] 2.11 **Validação TDD/API:** Rodar o comando `pytest tests/domain/` no backend e atestar `100% Passed`. Em seguida, subir o backend (`docker-compose up -d api`), abrir o Swagger UI (`http://localhost:8000/docs`) e rodar fluxo de teste manual E2E independentemente do Front-end.

## FASE 3: Frontend Foundation (Next.js + shadcn/ui)
- [ ] 3.1 No `frontend/`: Inicializar Next.js App Router com TypeScript e TailwindCSS. Remover boilerplate default.
- [ ] 3.2 Criar `Dockerfile` do frontend expondo porta 3000 e adicionar o serviço `web` no `docker-compose.yml`.
- [ ] 3.3 Inicializar shadcn/ui (`npx shadcn-ui@latest init` - CSS variables, estilo raw non-interactive).
- [ ] 3.4 Importar lista estrita de componentes shadcn permitidos: `npx shadcn-ui@latest add button card table dialog badge alert toast`.
- [ ] 3.5 Criar o layout genérico e a `page.tsx` estática inicial usando componentes Tailwind puro para as cascas estruturais.
- [ ] 3.6 **Validação:** Rodar `docker-compose up -d web` e acessar `http://localhost:3000` para confirmar que o contêiner Next.js está de pé, com Tailwind configurado, fontes carregadas e nenhum Erro de Hydration no console do navegador.

## FASE 4: Integração Full-Stack, UI e Demo
- [ ] 4.1 Criar biblioteca interna abstrata no Next.js (`lib/api.ts`) para encapsular lógicas de `fetch` à API (FastAPI) repassando header Bearer Token.
- [ ] 4.2 Construir a *Visão do Motorista* (PWA-like): Tela responsiva mobile-first com botões mockados de "Informar Reroute" e "Parada (0km/h)" disparando eventos na porta remota.
- [ ] 4.3 Construir o *Painel do Lojista*: Componente abstrato `DataTable` consumindo e renderizando a rota GET `/deliveries/` exclusivas àquele Lojista.
- [ ] 4.4 Construir Sub-componente Interativo: Aba de Desenvolvedor oculta (`Dialog` do shadcn) de **Injeção de Caos** para simular o stress.
- [ ] 4.5 Construir Sub-componente de Eventos: Listagem condicional de **Alertas Críticos (SLA Risk)** calculados dinamicamente no Client.
- [ ] 4.6 **Validação Final:** Acessar o ambiente de ponta a ponta (Browser -> Next.js container -> FastAPI container -> PostgresDb container). Logar como Lojista, listar entregas, usar a Action DevMode (Caos), selecionar "Alagamento", submeter, e atestar visualmente na tabela que o valor do "ETA Forecast" atualizou instantaneamente com o recálculo matemático.
