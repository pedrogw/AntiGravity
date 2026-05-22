## Context

Após estabelecermos o núcleo do Domínio (Entidades, Protocolos) e a Infraestrutura (Implementações do Axios e LocalStorage), agora precisamos unir os dois lados de maneira limpa. Os componentes React não devem acionar a Infraestrutura diretamente. Para isso, utilizamos Casos de Uso (Application Layer) e um Container de Injeção de Dependências.

## Goals / Non-Goals

**Goals:**
- Implementar as classes de Casos de Uso (ex: `LoginUseCase`) baseadas em Classes (Orientação a Objetos) injetando as abstrações dos repositórios via Construtor.
- Criar a factory (ou um sistema leve de DI) para resolver as instâncias reais dos Casos de Uso que a UI vai consumir.
- Garantir 100% de cobertura de código (Unit Tests com Vitest) apenas nesta camada.

**Non-Goals:**
- Não iremos ligar isso no React *ainda* (Isso será na Fase 4, onde alteraremos os Hooks). O foco desta fase é deixar a aplicação completamente operável via testes/código puro.

## Decisions

1. **Classes para UseCases (RORO pattern com classes):**
   - *Decisão:* Cada UseCase será uma classe com um único método público (`execute()`). O construtor recebe as dependências (`repo`). O método `execute` receberá um único objeto de input e retornará a Entidade.
   - *Alternativas:* Funções puras que retornam Closures (`const makeLoginUseCase = (repo) => async (input) => { ... }`). Optamos pelas classes pela melhor compatibilidade e facilidade de autocompletes no TypeScript.

2. **Factory Functions vs Decorators de DI:**
   - *Decisão:* Como não usamos frameworks pesados (como NestJS no front), evitaremos `tsyringe` ou similar. Usaremos arquivos "Factories" simples exportando funções como `makeLoginUseCase()` que amarram e instanciam o `ApiAuthRepository` e retornam a classe `LoginUseCase` pronta.

## Risks / Trade-offs

- **[Trade-off] Boilerplate Adicional:** Injeção manual exige que cada novo UseCase tenha uma factory configurada manualmente.
  - *Mitigação:* As factories de DI serão centralizadas em `src/infrastructure/di/` e serão fáceis de duplicar. O ganho de não ter "mágica de metadados" com decorators vale o esforço para uma codebase frontend que preza por bundles leves.
