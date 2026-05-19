## 1. Domain Value Objects

- [x] 1.1 Criar `app/domain/value_objects/coordinates.py`
- [x] 1.2 Implementar a classe `Coordinates` usando o decorator `@dataclass(frozen=True)` com atributos numéricos (`lat`, `lng`)
- [x] 1.3 Refatorar as entidades (ex: `Place` e `Delivery`) ou o serviço do Bloco 3 (`ETAService`) para consumir este novo Value Object no lugar de primitivas soltas

## 2. Inversão de Dependência (Protocols)

- [x] 2.1 Criar a pasta `app/domain/repositories/` e os arquivos base para os protocolos: `user_repo.py`, `place_repo.py`, `delivery_repo.py`
- [x] 2.2 Definir `UserRepositoryProtocol(Protocol)`, `PlaceRepositoryProtocol(Protocol)`, etc. contendo apenas as assinaturas (ex: `async def create(...) -> Entity: ...`)
- [x] 2.3 Alterar os `Use Cases` existentes em `app/use_cases/` para importarem os Protocols e não mais as classes concretas de `app/infrastructure/`

## 3. Validação de Regressão

- [x] 3.1 Executar os testes estáticos com `mypy app/use_cases/` para garantir que o duck typing dos Protocols está correto em relação às chamadas do framework
- [x] 3.2 Rodar `pytest -v` para assegurar que a tipagem flexível não alterou o comportamento em tempo de execução
