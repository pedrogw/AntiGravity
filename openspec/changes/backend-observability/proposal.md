## Por quê

Atualmente, o backend FastAPI não possui um sistema padronizado de logs e tratamento de erros globais. Erros geram stacktraces crus no console, rotas precisam lidar com blocos `try-except` repetitivos, e pior: a camada de domínio (Use Cases) está importando exceções específicas de transporte (`HTTPException` do FastAPI), o que viola a Clean Architecture. Para que a aplicação seja profissional, precisamos de observabilidade segura (logs JSON sem dados sensíveis), rastreabilidade (Request IDs) e um domínio puramente agnóstico.

## O que Muda

- **Middleware de Logging com Data Masking**: Implementação de um interceptor global que injeta `X-Request-ID` e loga estruturadamente. Dados sensíveis (senhas, tokens) serão obrigatoriamente mascarados.
- **Limpeza Arquitetural (Decoupling)**: Remoção de todos os imports do FastAPI (`HTTPException`) de dentro da pasta `app/use_cases/`. Eles serão substituídos por `DomainExceptions`.
- **Exception Handler Global**: Centralização do tratamento de erros. A lógica existente de `OperationalError` será movida para cá, junto com o novo mapeamento de `DomainException` -> `HTTPException`.
- **Healthcheck Padrão**: Oficialização do endpoint `/health`.

## Capacidades

### Novas Capacidades
- `observability-middleware`: Sistema de logs estruturados, mascaramento de dados (PII/Senhas) e rastreabilidade via Request ID.
- `global-exception-handling`: Padronização de erros e isolamento absoluto entre Camada de Domínio e Transporte HTTP.

### Capacidades Modificadas
- Nenhuma capacidade de negócio modificada.

## Impacto

| Área | Detalhe |
|---|---|
| `app/use_cases/*` | **BREAKING INTERNAL**: Todos os disparos de `HTTPException` serão trocados por `DomainException`. |
| `app/main.py` | Movimentação do handler atual e injeção do novo ecossistema. |
| `app/core/logging.py` | Configuração com suporte a Data Masking. |
| Rotas em `app/api/` | Códigos mais limpos e focados apenas em orquestração. |
