## Why

A arquitetura atual do backend segue um padrão de camadas com vazamento de lógica de negócio e de orquestração para os routers (FastAPI), o que configura uma quebra da "Dependency Rule" da Clean Architecture. Além disso, as "entidades" de domínio são atualmente modelos do SQLAlchemy, o que resulta em um Domínio Anêmico dependente de infraestrutura. Para blindar o projeto para avaliação acadêmica rigorosa e garantir os princípios DDD (Domain-Driven Design), é necessário refatorar a estrutura adotando estritamente Casos de Uso, Repositórios e Entidades Puras.

## What Changes

- Criação da camada de Entidades puras (sem dependência de bibliotecas externas).
- Extração de toda a lógica de orquestração dos roteadores da API para uma nova camada de Casos de Uso (Application Layer).
- Criação da camada de Repositórios para servir de interface entre as Entidades e o banco de dados (SQLAlchemy).
- Movimentação dos modelos ORM atuais (`app/models`) para uma camada explícita de infraestrutura (`app/infrastructure/orm`).
- Refatoração dos roteadores (`auth`, `places`, `deliveries`) para dependerem apenas dos Casos de Uso, injetando Repositórios e removendo chamadas diretas de banco de dados (`db.execute`).

## Capabilities

### New Capabilities
- `clean-architecture-core`: Estruturação da separação em 4 camadas rígidas (Domain, Application, Interface, Infrastructure).

### Modified Capabilities
- Vazio (Os requisitos do produto não sofrem alteração, apenas a arquitetura do código muda).

## Impact

- **Código Afetado:** Pastas do backend serão reorganizadas (`app/domain`, `app/use_cases`, `app/infrastructure`, `app/api`).
- **APIs:** Os endpoints continuarão idênticos externamente (entradas e saídas preservadas).
- **Banco de Dados:** Risco mitigado (nomeação das classes ORM será preservada para não gerar conflito com migrações do Alembic).
- **Testes:** A injeção de dependência atual (`TestSessionLocal` provida via `Depends(get_db)`) cobrirá a instanciação dos Repositórios, mantendo os testes de integração funcionais.
