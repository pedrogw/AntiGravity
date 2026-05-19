## Context

Atualmente, o domínio da aplicação não define como deseja interagir com a persistência de dados. Os repositórios concretos (`DeliveryRepository`, etc.) existem apenas na camada de infraestrutura. Isso significa que os Use Cases dependem da Infraestrutura, quebrando o princípio principal da Clean Architecture (DIP). Queremos formalizar a Inversão de Dependência de forma "Pythonic" (simples, sem boilerplate desnecessário).

## Goals / Non-Goals

**Goals:**
- Desacoplar Use Cases de Infraestrutura.
- Utilizar `typing.Protocol` (duck typing estático do Python) para definir contratos de repositórios, evitando o peso de herança com `abc.ABC`.
- Centralizar o uso de primitivas (ex: `latitude` e `longitude`) em Value Objects imutáveis.

**Non-Goals:**
- Mudar a lógica do banco de dados (SQLAlchemy permanecerá igual).
- Criar abstrações vazias ou desnecessárias ("over-engineering").

## Decisions

### Decisão 1: O uso de Protocols vs ABCs
**Escolha**: Criaremos `DeliveryRepositoryProtocol` (e afins) usando `typing.Protocol`. O repositório concreto em `infrastructure` não precisará herdar do Protocolo; contanto que ele implemente a mesma assinatura (duck typing estático), o `mypy` e as IDEs aceitarão.
**Por quê**: É a forma mais moderna e limpa de implementar Inversão de Dependência em Python. Mantém as classes não atreladas estruturalmente.

### Decisão 2: Implementação de Value Objects
**Escolha**: Usar a decorator padrão do Python `@dataclass(frozen=True)` para Value Objects.
**Por quê**: Garantia gratuita de imutabilidade. Quando uma instância é modificada, uma nova precisa ser criada. Evita efeitos colaterais silenciosos no código de negócio.

## Risks / Trade-offs

| Risco | Mitigação |
|---|---|
| Falso Positivo em Tipagem | Como o `Protocol` avalia assinaturas implicitamente, uma pequena diferença (ex: `limit: int` vs `limit: Optional[int]`) pode gerar erro de tipagem. Mitigação: usar ferramentas de análise estática (`pyright` ou `mypy`) no CI. |

## Migration Plan
1. Criar `app/domain/value_objects/coordinates.py`.
2. Criar `app/domain/repositories/` contendo os `Protocols`.
3. Atualizar as anotações de tipo dos argumentos `repo` no construtor de todos os Casos de Uso.
4. Validar se os testes continuam passando.
