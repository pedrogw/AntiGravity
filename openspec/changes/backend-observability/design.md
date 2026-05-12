## Context

A análise de integridade revelou duas falhas arquiteturais graves na versão atual:
1. **Acoplamento de Framework no Domínio**: Os Use Cases (`app/use_cases/auth_use_cases.py`) estão importando e lançando `fastapi.HTTPException`. Isso destrói o princípio da Clean Architecture, amarrando a regra de negócio a um framework web.
2. **Logs Inseguros**: Adicionar logs crus em requisições de autenticação e criação corre o risco de expor senhas (`password`) e PII (`email`) em texto claro no servidor.

Além disso, a injeção do middleware e do handler global deve levar em consideração lógicas já existentes no `main.py` (como o tratamento de `OperationalError`).

## Goals / Non-Goals

**Goals:**
- Desacoplar completamente a pasta `app/use_cases` do FastAPI.
- Implementar Data Masking automático para chaves sensíveis nos logs (ex: `password: "***"`).
- Integrar handlers existentes (banco de dados) no novo ecossistema centralizado.
- Garantir rastreabilidade de requisições com `X-Request-ID`.

**Non-Goals:**
- Integração com sistemas de observabilidade externos (APMs) na fase inicial.

## Decisions

### Decisão 1: Data Masking em Logs
**Escolha**: Criar um filtro customizado (`logging.Filter` ou formatador específico) que utilize regex ou parsing de chaves para substituir valores sensíveis em dicionários ou strings de request body.
**Por quê**: É uma exigência de segurança (Compliance) não vazar PII em logs do servidor.

### Decisão 2: Substituição Obrigatória por DomainException
**Escolha**: O handler global interceptará classes que herdam de uma `DomainException` pura (definida em `app.core.exceptions`).
**Por quê**: O Use Case levanta um erro que faz sentido pro negócio (ex: `EmailAlreadyExistsException`), e a camada de transporte (Router/Handler) sabe que para esse erro específico, ela deve devolver um `HTTP 409 Conflict`.

### Decisão 3: Refatoração do `main.py`
**Escolha**: Mover a lógica de `OperationalError` atual para o novo arquivo de exception handling e registrá-lo limpamente no `main.py` junto com o novo `DomainException` handler.
**Por quê**: Evita espalhar lógicas de erro pelo código-fonte de orquestração principal.

## Risks / Trade-offs

| Risco | Mitigação |
|---|---|
| Perda de contexto técnico em produção | O global handler *sempre* deve logar a causa original completa (traceback real) internamente associado ao Request ID, devolvendo apenas a mensagem mascarada/segura ao cliente HTTP. |
| O filtro de Masking não pegar todos os dados | Usar abordagens híbridas (mascaramento de chaves conhecidas JSON e varredura simples em queries URL). |

## Migration Plan
1. Criar o mecanismo de Logging com Masking e o Middleware.
2. Criar a estrutura de Exceções de Domínio.
3. Varredura completa nos `app/use_cases/` substituindo os imports.
4. Mover e centralizar os handlers antigos do `main.py` junto com os novos.
