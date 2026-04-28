## Context

O backend atual foi desenvolvido usando um padrão em camadas (Layered Architecture) onde as rotas do FastAPI executam diretamente operações no banco de dados utilizando os modelos do SQLAlchemy. Embora eficiente em projetos menores e amplamente aceito no mercado para APIs rápidas, essa abordagem resulta em um Domínio Anêmico e em um forte acoplamento entre a camada HTTP, a lógica de negócio e a persistência de dados (violação da Dependency Rule). Para fins de avaliação acadêmica rigorosa e de evolução sustentável do sistema, migraremos a estrutura para uma implementação estrita de Clean Architecture e Domain-Driven Design (DDD).

## Goals / Non-Goals

**Goals:**
- Desacoplar a lógica de negócio (orquestração) dos roteadores HTTP.
- Isolar a infraestrutura de banco de dados em Repositórios (Interface Adapters).
- Criar Entidades de Domínio agnósticas (puras) e independentes.
- Garantir que a refatoração preserve a base de dados atual e faça os testes E2E continuarem passando.

**Non-Goals:**
- Não haverá adição de novas regras de negócio.
- Não iremos alterar os contratos da API externa (Schemas Pydantic de Request/Response permanecem os mesmos).
- Não trocaremos o ORM (SQLAlchemy) ou o Banco de Dados (PostgreSQL).

## Decisions

- **Dataclasses para Entidades Puras**: As entidades na nova camada `app/domain/entities` serão construídas usando a biblioteca padrão `dataclasses`.
  - *Rationale*: Garante que o domínio principal seja 100% puro (sem imports de libs externas). O Pydantic ficará restrito à camada de Interface HTTP (`app/schemas`).
- **Injeção de Dependências Dinâmica**: Os Repositórios serão instanciados no nível da Rota com a sessão atual e então passados para os Casos de Uso.
  - *Rationale*: Esta estratégia aproveita o sistema `Depends(get_db)` existente. Dessa forma, as sobreposições de banco de dados em `conftest.py` continuam valendo, garantindo o funcionamento perfeito dos testes atuais.
- **Preservação Nominal dos Modelos ORM**: Ao mover os arquivos de `app/models/` para `app/infrastructure/orm/`, a estrutura das classes `Base` será mantida exatamente igual, sendo importadas com alias nos Repositórios (`import ... as UserModel`).
  - *Rationale*: Previne uma falha crítica no Alembic. Como o nome da tabela é inferido pelo nome da classe em `base_class.py`, alterar o nome das classes faria o Alembic deletar a base de dados em produção.

## Risks / Trade-offs

- **Risco de Verbosidade Excessiva** → Arquitetura limpa exige criar 3 a 4 arquivos novos para um endpoint simples de CRUD. 
  - *Mitigação*: Manteremos templates básicos nos repositórios para evitar código boilerplate. O benefício do desacoplamento justifica o aumento estrutural para a tese acadêmica.
- **Tradução Lenta de Objetos** → O Pydantic precisa converter os objetos de Domínio (Dataclasses) nos schemas de saída.
  - *Mitigação*: Utilizaremos a configuração nativa `model_config = {"from_attributes": True}` nas respostas, que já se provou robusta na conversão de SQLAlchemy, operando igualmente bem com dataclasses puras.
