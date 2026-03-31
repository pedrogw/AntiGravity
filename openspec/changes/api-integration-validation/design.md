## User Experience

O novo script de seed `admin_seed.py` garantirá um ambiente previsível para testes locais via Swagger `/docs`. Os testes de integração (E2E) em `tests/api/` rodarão via `httpx` no docker.

## Architecture & Implementation Strategy

### Componentes Chave
1. **API Integration Tests**
   - Utilizaremos `httpx.AsyncClient` acoplado ao `pytest-asyncio`.
   - Um arquivo de fixture re-inicializará um banco de testes isolado ou mockará as conexões `get_db`.
   - Bater em `/auth/register`, `/auth/login`, capturar o Bearer token, usá-lo pra criar Factories em `/places/factories`.

2. **Admin Seed Script**
   - Um script isolado `backend/admin_seed.py` rodará as sessões do sqlalchemy async para criar o e-mail master (admin@antigravity.com) forçando a Role de superuser ou inserções necessárias.

## Dependencies & API Changes

### Internal API/Schema
- Mantém coerência total com O que já temos no FastAPI.

### New/Updated Dependencies
- Usará o próprio ambiente do Docker (`api` container) para usar `httpx` já instalado no `requirements.txt`.

## Data Model

- Não aplicável mudanças na modelagem.

## Security & Privacy

- O Seed Script nunca deverá ser executado em prod.

## Testing Strategy

- `sudo docker compose exec api pytest tests/api -v` confirmando 100% Passed.

## Open Questions

- Separamos o banco de dados de testes num container diferente? (Por ora, rodamos diretamente no mesmo Postgres via rollbacks ou test db).
