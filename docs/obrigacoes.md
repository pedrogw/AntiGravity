# Obrigações do Projeto — AntiGravity

## Arquitetura

### Clean Architecture / DDD
- **Domínio no centro:** Nenhuma dependência de infraestrutura, frameworks ou bibliotecas externas no domínio.
- **Entidades ricas:** Comportamento encapsulado na entidade — nada de getters/setters anêmicos. Métodos como `change_status()`, `update_position()`, `recalculate_eta()`, `apply_chaos()`, `aggregate()`.
- **Value Objects imutáveis:** `Coordinates`, `UserRole` etc. com validação própria (`__post_init__`).
- **Protocolos de repositório:** Interfaces no domínio (`domain/repositories/`), implementações na infraestrutura (`infrastructure/repositories/`).
- **Use Cases finos:** Orquestram I/O e delegam lógica para as entidades. Cada use case = 1 ação.
- **Injeção de dependência explícita:** Use cases recebem repositórios e serviços via construtor.
- **Event Bus:** Domínio publica eventos (`DeliveryCreatedEvent`, `DeliveryStatusChangedEvent`); efeitos colaterais (auditoria, cache, worker) são handlers desacoplados.

### Domínio Rico (evitar domínio anêmico)
- Toda regra de negócio vive na entidade, não no use case.
- Toda validação de dados vive no Value Object, não no schema Pydantic.
- Métodos puros (sem I/O) sempre que possível.
- Factory methods (`@classmethod`) para encapsular lógica de criação complexa.
- Nada de setters públicos — mutação via métodos com nome semântico.

## TDD (Test-Driven Development)

- **Primeiro o teste, depois a funcionalidade,** salvo raríssimas exceções justificadas.
- Testes devem ser **determinísticos** — sem dependência de `datetime.utcnow()`, sem flaky tests.
- Mock de bordas de sistema (DB, Redis, APIs externas); lógica de domínio testada sem mocks.
- **Cobertura mínima global de 80%** em todas as camadas, com metas específicas: **100% no domínio**, **100% nos use cases**, **≥80% na infraestrutura**.
- Nenhum code review ou merge é aprovado com cobertura abaixo de 80%.
- Testes de integração validam contratos (API); testes unitários validam lógica.

### Padrão de Testes
- **Domínio:** Funções puras, sem async, sem DB — cenários de sucesso, erro e boundaries.
- **Use Cases:** `AsyncMock` nos repositórios, `pytest.mark.anyio`, cobertura de branches de erro.
- **API:** `TestClient` + fixtures de autenticação, validação de status code + body.
- **Frontend (hooks):** Mock das factories de DI, `renderHook` + `act`, assert de estado e chamadas.

## Código

- **Português (BR):** Mensagens para o usuário, nomes de entidades, schemas, testes.
- **Código-fonte (inglês):** Nomes de classes, métodos, variáveis, arquivos — em inglês. Comentários apenas quando absolutamente necessário (preferir código autoexplicativo).
- **Sem comentários desnecessários:** Código deve ser autoexplicativo. Comentários só para documentar decisões não óbvias.
- **Type hints obrigatórios:** Python (tipos em todos os métodos) e TypeScript (strict mode).
- **Async sempre:** FastAPI assíncrono, SQLAlchemy async, conexões async.
- **Consistência transacional:** `commit()` + `refresh()` em todas as operações de escrita; `flush()` isolado não é seguro.

## Decisões Estruturais

| Diretriz | Por quê |
|---|---|
| SQLite in-memory para testes | Velocidade, isolamento, sem dependência externa |
| `unittest.mock.patch` para built-ins C-level | `monkeypatch` não funciona em `datetime.utcnow` |
| Datas em 2050 nos testes de caos | Determinismo de `remaining_time` |
| `asyncio.gather` para queries paralelas | Performance no dashboard |
| Cache-Aside com invalidação por evento | Consistência eventual controlada |
| middleware de observabilidade + DataMasking | Rastreabilidade sem vazar PII |
| slowapi com limites conservadores | Rate limiting por IP |
| `Idempotency-Key` header (não UNIQUE constraint) | Padrão REST; desacoplado do schema de domínio |

## Camadas e Responsabilidades

```
domain/
  entities/       → Lógica de negócio, VOs, regras
  events.py       → Domain events
  haversine.py    → Cálculos puros
  chaos.py        → Lógica de caos pura
  safe_check.py   → Regras de segurança
  repositories/   → Protocolos (interfaces)
  services/       → Serviços de domínio

use_cases/        → Orquestradores (1 arquivo por caso de uso ou agregado coeso)

schemas/          → Pydantic (entrada/saída da API, sem lógica de negócio)

api/              → Rotas FastAPI (thin: validação + delegação ao use case)

infrastructure/
  repositories/   → Implementações SQLAlchemy dos protocolos
  orm/            → Modelos SQLAlchemy (tabelas)
  cache/          → Redis client + cache service
  events/         → Listeners (auditoria, cache invalidation)

core/             → Config, security, exceptions, logging, event bus, rate limiter

main.py           → App factory, lifespan, routers, exception handlers, wiring
```

## Frontend (Next.js)

- **Mesma clean architecture:** `domain/` → `application/` → `infrastructure/` → `components/`
- **Hooks finos:** Consomem use cases via factories de DI. Testáveis com mock das factories.
- **MSW para mock de API** em testes de integração.
- **shadcn/ui** para componentes de UI.
- **Vitest** como runner de testes.

## Convenções de Commit

- Commits no estilo conventional commits: `feat:`, `refactor:`, `fix:`, `docs:`, `test:`.
- Mensagens em inglês, concisas.
- Commits atômicos: uma mudança lógica por commit.

## Garantia de Qualidade em Alterações

Toda alteração de código deve seguir este fluxo obrigatório antes de ser commitada:

### 1. Análise de Impacto
- Identificar todos os arquivos e camadas afetados pela mudança (domínio, use cases, API, infraestrutura, schemas, testes).
- Verificar se a mudança pode quebrar contratos existentes (response models, assinaturas de método, protocolos de repositório).
- Verificar se a mudança afeta o comportamento em produção (Docker Compose, deploy Render/Vercel).
- **Nenhuma alteração deve ser feita assumindo que "funciona por coincidência"** — toda dependência implícita deve ser explicitada ou eliminada.

### 2. Testes Intensivos
- **Nova funcionalidade:** Testes escritos antes do código (TDD), cobrindo sucesso, erro e boundaries.
- **Correção de bug:** Teste que reproduz o bug deve ser adicionado antes da correção, e passar após.
- **Refatoração:** Nenhum teste existente pode ser alterado (a menos que o contrato tenha mudado intencionalmente). Rodar suite completa antes e depois — resultado deve ser idêntico.
- **Cobertura:** A alteração não pode reduzir a cobertura global. Idealmente, caminhos novos devem estar em 100%.

### 3. Verificação Cruzada
- Reler o diff completo antes de commitar — procurar por:
  - Lógica duplicada ou contraditória
  - Type hints faltando ou errados
  - Recursos não fechados (conexões, files, sessions)
  - Secrets ou IPs hardcoded
  - Código comentado ou dead code
- Verificar lint (backend: `ruff`, frontend: `npm run lint`).
- Verificar que o código funciona no ambiente real: `docker compose up -d` + teste manual do fluxo alterado.

### 4. Bloqueios
- Nenhum commit é aprovado sem análise de impacto documentada (pelo menos no corpo da mensagem do commit).
- Nenhum merge é aprovado com lint warnings ou testes falhando.
- Qualquer alteração que toque em segurança (tokens, senhas, CORS, rate limiting) requer validação manual adicional do fluxo no Docker Compose.
