## ADDED Requirements

### Requirement: Inversão de Dependência (DIP) Estrrita
O sistema SHALL forçar as regras de negócio a dependerem exclusivamente de abstrações do próprio Domínio, não de módulos concretos de infraestrutura.

#### Scenario: Mocking isolado de banco
- **WHEN** um teste unitário valida a lógica de um Caso de Uso
- **THEN** o desenvolvedor MUST poder injetar uma classe Mock sem herdar de NADA, desde que os métodos implementados satisfaçam o Protocolo estático (`typing.Protocol`), garantindo tempo de execução em submilisegundos por não carregar motores de SQL.
