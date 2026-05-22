## Why

Com os Casos de Uso (Application Layer) construídos na Fase 3, a fundação está completa. No entanto, a camada de Apresentação (UI) ainda utiliza código acoplado, acessando APIs diretamente ou espalhando lógica de tratamento de erros genéricos pelos componentes. Esta fase encerra a migração conectando os React Hooks aos Casos de Uso criados. Isso transformará o React em uma "dumb view" pura, que reage aos dados e delega todas as ações pesadas para a injeção de dependências.

## What Changes

- Refatoração dos Custom Hooks (`useAuth`, etc.) para instanciar os Casos de Uso via as Factories da Injeção de Dependências.
- Remoção total de referências a pacotes de infraestrutura (como `axios` ou chamadas diretas a `localStorage`) de dentro da pasta `src/hooks` e `src/components`.
- Atualização do mapeamento de erros nos componentes para interagir com as classes de Erros de Domínio (ex: exibir toast customizado se receber `UnauthorizedError`).
- Refatoração dos testes de integração do React Testing Library (RTL) para validar o comportamento da UI alimentada pelos Casos de Uso.

## Capabilities

### New Capabilities
- `frontend-presentation-hooks`: Refatoração do padrão de Hooks para atuar apenas como ponte (bridge) entre o React Lifecycle e os Casos de Uso do Domínio.
- `frontend-domain-error-handling`: Interface unificada de tratamento e exibição de Erros de Domínio nos componentes React.

### Modified Capabilities
- Os componentes visuais e suas regras de produto não mudam; o que muda é como a interface invoca comandos no sistema.

## Impact

- **Segurança de Rendering:** Alterações na infraestrutura da API não afetarão o React, desde que a Entidade retornada pelo Domínio se mantenha a mesma.
- **Previsibilidade:** Os componentes não precisarão fazer checks complexos de `if (response.status === 401)`, usando em vez disso checks do tipo `if (error instanceof UnauthorizedError)`.
- **Testes de Integração:** Os testes de componentes no RTL ficarão incrivelmente limpos e rápidos.
