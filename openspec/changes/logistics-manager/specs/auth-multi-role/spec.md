## ADDED Requirements

### Requirement: Registro de usuário com role
O sistema SHALL permitir o registro de novos usuários com atribuição de role (operador, lojista ou motorista). Cada usuário MUST ter email único, senha com hash seguro e role definida no momento do registro.

#### Scenario: Registro bem-sucedido de operador
- **WHEN** um POST é feito em `/auth/register` com email, senha e role="operador"
- **THEN** o sistema cria o usuário, retorna HTTP 201 com id e email (sem senha)

#### Scenario: Registro com email duplicado
- **WHEN** um POST é feito em `/auth/register` com email já existente
- **THEN** o sistema retorna HTTP 409 com mensagem "Email já cadastrado"

### Requirement: Login com JWT
O sistema SHALL autenticar usuários via email/senha e retornar um token JWT contendo id, email e role.

#### Scenario: Login bem-sucedido
- **WHEN** um POST é feito em `/auth/login` com credenciais válidas
- **THEN** o sistema retorna HTTP 200 com access_token JWT válido contendo claims de role

#### Scenario: Login com credenciais inválidas
- **WHEN** um POST é feito em `/auth/login` com senha incorreta
- **THEN** o sistema retorna HTTP 401 com mensagem "Credenciais inválidas"

### Requirement: Controle de acesso por role
O sistema SHALL restringir endpoints por role usando dependency injection. Operador acessa tudo, lojista acessa seus dados e entregas destinadas a ele, motorista acessa suas rotas e atualizações de posição.

#### Scenario: Operador acessa endpoint administrativo
- **WHEN** um operador autenticado faz GET em `/deliveries/` (listar todas)
- **THEN** o sistema retorna HTTP 200 com todas as entregas

#### Scenario: Lojista tenta acessar endpoint de operador
- **WHEN** um lojista autenticado tenta POST em `/chaos/events` (criar evento de caos)
- **THEN** o sistema retorna HTTP 403 "Acesso negado"

#### Scenario: Requisição sem token
- **WHEN** uma requisição é feita sem header Authorization em endpoint protegido
- **THEN** o sistema retorna HTTP 401 "Não autenticado"
