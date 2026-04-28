## ADDED Requirements

### Requirement: Isolação do Domínio
O sistema SHALL implementar entidades de domínio puras (sem dependência de frameworks externos como SQLAlchemy ou FastAPI) para representar os conceitos core do negócio.

#### Scenario: Modelagem Pura
- **WHEN** uma entidade de domínio (como Delivery ou User) for instanciada
- **THEN** ela deve ser um objeto Python puro (ex: usando dataclasses) sem heranças de ORM

### Requirement: Orquestração via Casos de Uso
O sistema SHALL utilizar uma camada de Casos de Uso (Application Layer) para orquestrar as regras de negócio de cada funcionalidade.

#### Scenario: Desacoplamento da Interface Web
- **WHEN** um endpoint da API for acessado (ex: criar entrega)
- **THEN** o roteador FastAPI deverá instanciar um Caso de Uso e invocar seu método de execução em vez de processar a lógica diretamente ou manipular transações de banco de dados

### Requirement: Persistência via Repositórios
O sistema SHALL implementar o padrão Repository para encapsular as operações de banco de dados, atuando como ponte entre o SQLAlchemy e os Casos de Uso.

#### Scenario: Tradução de Objetos
- **WHEN** um Caso de Uso solicitar dados ao Repositório
- **THEN** o Repositório deverá realizar a query usando o ORM, mas deverá retornar uma Entidade Pura de Domínio ao Caso de Uso
