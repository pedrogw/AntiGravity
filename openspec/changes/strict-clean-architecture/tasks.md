## 1. Domain Entities

- [x] 1.1 Criar dataclasses puras para User e UserRole em `app/domain/entities/user.py`
- [x] 1.2 Criar dataclasses puras para Factory e Store em `app/domain/entities/place.py`
- [x] 1.3 Criar dataclasses puras para Delivery e EtaHistory em `app/domain/entities/delivery.py`
- [x] 1.4 Criar dataclass pura para Alert em `app/domain/entities/alert.py`
- [x] 1.5 Criar dataclass pura para ChaosEventLog em `app/domain/entities/chaos.py`

## 2. Infrastructure & ORM

- [x] 2.1 Mover e renomear o diretório `app/models/` para `app/infrastructure/orm/`
- [x] 2.2 Atualizar `app/db/base.py` para refletir os novos imports de `app/infrastructure/orm/` (protegendo o Alembic)
- [x] 2.3 Atualizar os Pydantic schemas (`app/schemas/`) para importar enums e constantes das Entidades puras em vez do ORM

## 3. Repositories

- [x] 3.1 Criar `UserRepository` em `app/infrastructure/repositories/user_repo.py` (com métodos `create` e `get_by_email` mapeando ORM <-> Entidade)
- [x] 3.2 Criar `PlaceRepository` em `app/infrastructure/repositories/place_repo.py` (mapeando operações de Factory e Store)
- [x] 3.3 Criar `DeliveryRepository` em `app/infrastructure/repositories/delivery_repo.py` (mapeando operações de Delivery)

## 4. Use Cases (Application Layer)

- [x] 4.1 Implementar `RegisterUserUseCase` e `LoginUserUseCase` em `app/use_cases/auth_use_cases.py`
- [x] 4.2 Implementar Casos de Uso para criação e listagem em `app/use_cases/places_use_cases.py`
- [x] 4.3 Implementar Casos de Uso para criação e listagem em `app/use_cases/deliveries_use_cases.py`

## 5. API Routers Refactoring

- [x] 5.1 Refatorar `app/api/auth.py` para depender estritamente dos Casos de Uso e injetar o Repositório via FastAPI Depends
- [x] 5.2 Refatorar `app/api/places.py` para depender estritamente dos Casos de Uso
- [x] 5.3 Refatorar `app/api/deliveries.py` para depender estritamente dos Casos de Uso

## 6. Validation

- [ ] 6.1 Rodar suite completa de testes E2E (`pytest -v`) e garantir que a refatoração não quebrou os contratos da API nem o comportamento esperado
