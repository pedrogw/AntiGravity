## ADDED Requirements

### Requirement: pgadmin-ui
A ferramenta deve estar empacotada no docker-compose e escutar requisições de administração do BD

#### Scenario: Subir ecossistema Backend
- **WHEN** O operador roda `docker compose up -d`
- **THEN** O Container PgAdmin deve iniciar e ficar no ar (`Up`)

#### Scenario: Acesso Web
- **WHEN** O operador acessa a porta `5050`
- **THEN** Uma página de login deve ser mostrada aceitando credenciais admin
