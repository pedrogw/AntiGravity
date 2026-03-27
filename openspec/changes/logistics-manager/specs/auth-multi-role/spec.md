## ADDED Requirements

### Requirement: Registro de usuário com type mapping
O sistema SHALL permitir o registro de novos usuários na arquitetura B2B, marcando rigidamente como role="lojista" ou "motorista". Cada usuário MUST ter email único, senha com hash seguro.

#### Scenario: Registro bem-sucedido de Lojista Proprietário
- **GIVEN** que os dados de email, senha e permissões desejadas providos são válidos e o email é inédito
- **WHEN** um POST é feito em `/auth/register` requisitando a role="lojista"
- **THEN** o sistema cria o usuário na base B2B, retorna HTTP 201 exibindo ID blindando hash interno

#### Scenario: Registro com email duplicado
- **GIVEN** que o banco de dados já possui um usuário ativo com o email `contato@teste.com`
- **WHEN** um novo POST é feito em `/auth/register` tentando utilizar o mesmo email `contato@teste.com`
- **THEN** o sistema bloqueia a transação e retorna HTTP 409 com a mensagem "Email já cadastrado"

### Requirement: Login com JWT
O sistema SHALL autenticar usuários via email/senha e retornar um token JWT contendo id, email e role.

#### Scenario: Login bem-sucedido
- **GIVEN** um usuário previamente registrado no sistema
- **WHEN** um POST é feito em `/auth/login` enviando as credenciais corretas (email e senha)
- **THEN** o sistema verifica o hash, autentica o acesso e retorna HTTP 200 contendo um `access_token` JWT válido com a claim da `role`

#### Scenario: Login com credenciais inválidas
- **GIVEN** um email existente na base de dados
- **WHEN** um POST é feito em `/auth/login` submetendo intencionalmente uma senha incorreta
- **THEN** o sistema nega acesso por segurança, retornando HTTP 401 com a mensagem "Credenciais inválidas" sem revelar se o email existe

### Requirement: Controle de segurança B2B Server-Client
O sistema SHALL proteger a soberania de dados do lojista (Dependency Injection check). O Motorista escreve pings; O Lojista lê pings de rotas próprias. Entidades não cruzam escopos.

#### Scenario: Lojista Consumidor analisa Dashboard
- **GIVEN** um token JWT válido pertencente a um usuário com a role="lojista"
- **WHEN** ele faz um GET em `/deliveries/`
- **THEN** a injeção retorna HTTP 200 populada EXCLUSIVAMENTE pelas entregas linkadas a ele

#### Scenario: Motorista tenta quebrar tenant de Lojista
- **GIVEN** um token JWT válido do app Mobile (role="motorista")
- **WHEN** este ator bate acidentalmente na raiz comercial `/deliveries/reports`
- **THEN** o guard middleware barra a requisição retornando HTTP 403 "Privilégio insuficiente"

#### Scenario: Requisição sem token
- **GIVEN** qualquer endpoint da API marcado como protegido pelas dependências de segurança
- **WHEN** uma requisição é disparada sem o header `Authorization: Bearer <token>`
- **THEN** o sistema rejeita instantaneamente o pacote retornando HTTP 401 "Não autenticado"
