## ADDED Requirements

### Requirement: Repositórios concretos isolados
As implementações da API que utilizam Axios MUST residir exclusivamente na camada de infraestrutura (`src/infrastructure/repositories/`) e MUST obrigatoriamente assinar os contratos dos protocolos do Domínio (`implements ...RepositoryProtocol`).

#### Scenario: Requisição segura
- **WHEN** um Repositório faz uma requisição POST para realizar login
- **THEN** a requisição passa pelo `api_client` e o resultado é devolvido convertido em Entidade de Domínio.

### Requirement: Storage encapsulado
As lógicas de salvar dados locais (como tokens de autenticação) MUST não chamar `localStorage` diretamente nas regras de negócio.

#### Scenario: Persistência do token de acesso
- **WHEN** um login é bem sucedido
- **THEN** a chamada para persistir o token usa uma classe `TokenStorageAdapter` encarregada de envelopar as APIs de storage nativas do ambiente.
