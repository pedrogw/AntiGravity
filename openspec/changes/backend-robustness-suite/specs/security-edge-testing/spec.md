## ADDED Requirements

### Requirement: security-edge-testing
Garantir que a autorização por papéis (Roles) seja inviolável.

#### Scenario: Motorista tenta criar Fábrica
- **GIVEN** Um token JWT com role: motorista
- **WHEN** O usuário tenta POST /places/factories
- **THEN** A API retorna 403 Forbidden

#### Scenario: Token Expirado
- **GIVEN** Um token JWT gerado há 24h atrás
- **WHEN** O usuário tenta acessar rota protegida
- **THEN** A API retorna 401 Unauthorized
