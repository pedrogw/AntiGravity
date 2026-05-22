## Context

A Fase 1 estabeleceu o Vitest como motor de testes, mas ainda não temos código isolado o suficiente para testar. A camada de domínio no Frontend é essencial para garantir validações como "Um delivery não pode ser aceito se já foi entregue" no lado do cliente, agilizando feedback antes mesmo de requisitar a API. Esta fase foca exclusivamente nas pastas `domain/` e `infrastructure/`.

## Goals / Non-Goals

**Goals:**
- Implementar as entidades básicas modeladas a partir das respostas do backend.
- Implementar as interfaces dos repositórios que serão depois orquestrados pelos UseCases.
- Implementar os repositórios reais (Axios) sob a pasta `infrastructure/api/repositories`.

**Non-Goals:**
- Não iremos refatorar os Hooks React (Fase 4/5) nesta etapa.
- Não iremos implementar os Casos de Uso (Fase 3) ainda. Focaremos no contrato e na fundação.

## Decisions

1. **Uso de Classes vs Interfaces Puras para Entidades:**
   - *Decisão:* Usaremos classes puras (ES6 Classes) para Entidades e Value Objects onde houver lógica atrelada (ex: um método genérico de formatação), e interfaces simples apenas quando os dados forem puramente DTOs estáticos.
   - *Alternativas:* Usar Zod ou Type-only. Preferimos Classes para poder atrelar comportamentos sem depender de funções helper dispersas.

2. **Inversão de Dependências na Infraestrutura:**
   - Os repositórios da infraestrutura implementarão a interface do domínio (`class ApiAuthRepository implements AuthRepositoryProtocol`), protegendo a aplicação contra quebras futuras se mudarmos bibliotecas HTTP.

## Risks / Trade-offs

- **[Risco] Dessincronização Frontend/Backend:** As Entidades criadas no frontend podem ficar defasadas se o Backend mudar contratos.
  - *Mitigação:* As Entidades do frontend serão as mais enxutas possíveis, baseadas nas chaves comuns vitais da interface de usuário. Toleraremos dados extras enviados pelo backend.
