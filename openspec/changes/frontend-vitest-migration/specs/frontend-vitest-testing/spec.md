## ADDED Requirements

### Requirement: Testes com Vitest
O sistema MUST utilizar o Vitest como principal framework de testes unitários e de integração no frontend, e o Jest MUST ser inteiramente removido do `package.json`.

#### Scenario: Execução da suite de testes
- **WHEN** o desenvolvedor ou o pipeline de CI executa `npm run test`
- **THEN** a suíte de testes do Vitest é iniciada e reporta os resultados sem depender de pacotes do ecossistema Jest.

### Requirement: Rapidez no isolamento do Domínio
Os testes unitários das pastas `domain` e `application` MUST não carregar pacotes da DOM (jsdom) para sua execução.

#### Scenario: Testando o Domínio Puxo
- **WHEN** um teste verifica um `UseCase`
- **THEN** o Vitest o executa instantaneamente com environment nativo de Node.js sem parse de componentes visuais.
