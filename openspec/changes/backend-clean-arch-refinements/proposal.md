## Why

Embora a arquitetura base do backend seja sólida, alguns detalhes cruciais de Clean Architecture ainda não foram aplicados na sua plenitude. Os repositórios atuais estão acoplados às suas implementações (`UserRepo` concreto, etc.) sem uma abstração de domínio, violando o Dependency Inversion Principle (DIP). Além disso, não temos objetos de valor estruturados, levando ao uso de primitivos para regras de negócio (como coordenadas geográficas). Este bloco formaliza essas melhorias para garantir testes isolados mais rápidos e pureza no domínio.

## What Changes

- Implementação de `typing.Protocol` para os Repositórios dentro da camada de Domínio, invertendo a dependência.
- Refatoração dos Casos de Uso para dependerem exclusivamente dos *Protocols*, e não de implementações concretas (permitindo injeção de dependências via *Mocks* puros em testes).
- Criação de `Value Objects` minimalistas usando `@dataclass(frozen=True)` (ex: `Coordinates` para encapsular `lat/lng`).
- **BREAKING**: Assinaturas de Casos de Uso e testes que usavam implementações concretas do repositório precisarão ser atualizados para tipagem baseada nos *Protocols*.

## Capabilities

### New Capabilities
- `domain-value-objects`: Estruturas imutáveis puras para agrupar conceitos relacionados, como `Coordinates`.
- `repository-protocols`: Contratos formais (Interfaces via *typing.Protocol*) que definem como a aplicação interage com a persistência sem conhecer a infraestrutura.

### Modified Capabilities
- Nenhuma (apenas refatoração estrutural interna, sem mudança de requisitos funcionais).

## Impact

- `app/domain/value_objects/`: Ganhará novos arquivos (ex: `coordinates.py`).
- `app/domain/repositories/`: Será criada para abrigar as definições de *Protocol*.
- `app/use_cases/`: Terão a tipagem de dependências alterada.
- `tests/`: Os testes de Casos de Uso ficarão extremamente rápidos, pois não precisarão rodar integração com banco; poderão usar instâncias de classes Dummy/Mock que cumprem os *Protocols*.
