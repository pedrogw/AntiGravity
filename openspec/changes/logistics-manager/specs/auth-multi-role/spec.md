## ADDED Requirements

### Requirement: Registro de usuário com role
O sistema SHALL permitir o registro de novos usuários com atribuição de role (operador, lojista ou motorista). Cada usuário MUST ter email único, senha com hash seguro e role definida no momento do registro.

#### Scenario: Registro bem-sucedido de operador
- **GIVEN** que os dados de email, senha e permissões desejadas providos pelo cliente são válidos e o email é inédito
- **WHEN** um POST é feito em `/auth/register` requisitando a role="operador"
- **THEN** o sistema cria o usuário na base, retorna HTTP 201 e exibe o ID e o email protegendo o hash da senha

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

### Requirement: Controle de acesso por role
O sistema SHALL restringir endpoints por role usando dependency injection. Operador acessa tudo, lojista acessa seus dados e entregas destinadas a ele, motorista acessa suas rotas e atualizações de posição.

#### Scenario: Operador acessa endpoint administrativo
- **GIVEN** um token JWT válido pertencente a um usuário com a role="operador"
- **WHEN** este usuário faz um GET em `/deliveries/` (endpoint de visibilidade total da frota)
- **THEN** o sistema autoriza a requisição via Dependency Injection e retorna HTTP 200 com todas as entregas

#### Scenario: Lojista tenta acessar endpoint de operador
- **GIVEN** um token JWT válido, porém pertencente a um usuário com a role="lojista"
- **WHEN** este lojista tenta executar um POST em `/chaos/events` (rota restrita aos controladores de tráfego)
- **THEN** o middleware de autorização do sistema intervém, bloqueia a chamada e retorna HTTP 403 "Acesso negado"

#### Scenario: Requisição sem token
- **GIVEN** qualquer endpoint da API marcado como protegido pelas dependências de segurança
- **WHEN** uma requisição é disparada sem o header `Authorization: Bearer <token>`
- **THEN** o sistema rejeita instantaneamente o pacote retornando HTTP 401 "Não autenticado"
