## Why

Com a finalização do Motor Analítico (Fase 2) e testes granulares de domínio (Unitários/Haversine), precisamos agora garantir que essas funções respondam corretamente no contexto HTTP da FastAPI. Para isso, são essenciais testes de integração (E2E) que percorram as rotas `/auth`, `/places`, `/deliveries` de ponta a ponta. Além disso, ter um usuário administrador (Seed Administrativo) facilita a simulação de todo o fluxo no Swagger UI sem criar novos logins manualmente e é crítico para as apresentações.

## What Changes

1. **Testes de Integração de API (`tests/api/`)**: Criação de `pytest` com `httpx` (async) para iterar nos fluxos de registro, auth via JWT, criação de fábricas, lojas e cálculo logístico, todos operando de dentro do container (`docker-compose exec api pytest`).
2. **Seed Administrativo Aprimorado**: Expansão do `seed.py` para injetar consistentemente um usuário tipo Admin, provendo permissões diretas de testes.
3. **Execução conteinerizada**: Todos os comandos serão encapsulados via `docker-compose exec api` garantindo reprodução instantânea no ambiente homologado de arquitetura.

## Capabilities

### New Capabilities
- `api-integration`: Testes de E2E batendo no banco de dados e verificando payloads e exceptions de todo o CRUD e tokens JWT via Httpx.
- `admin-seed`: O script inicial de modelagem de dados que injeta a base da conta Administrativa para exploração no Swagger.

### Modified Capabilities

## Impact

Afeta test suite principal de todo backend e melhora confiabilidade das entregas da Fase 3 (Frontend), para que o Dashboard interaja com APIs sólidas.
