## 1. Implementação do Domínio (Core)

- [x] 1.1 Criar a estrutura base de diretórios em `src/domain/` (`entities`, `errors`, `repositories`, `value_objects`).
- [x] 1.2 Implementar Classes de Erros customizados em `src/domain/errors/` (`AppError.ts`, `UnauthorizedError.ts`, `NetworkError.ts`, `ValidationError.ts`).
- [x] 1.3 Implementar a entidade abstrata base `Entity.ts` e as entidades concretas como `User.ts`.
- [x] 1.4 Criar a interface `AuthRepositoryProtocol.ts` contendo as assinaturas puras de login, logout e registro.

## 2. Implementação da Infraestrutura (Adapters)

- [x] 2.1 Mover as utilidades do Axios para `src/infrastructure/api/api_client.ts` se ainda não estiver configurado corretamente.
- [x] 2.2 Criar `src/infrastructure/storage/TokenStorageAdapter.ts` abstraindo o acesso ao `localStorage` para leitura, escrita e remoção.
- [x] 2.3 Implementar o `ApiAuthRepository.ts` implementando o `AuthRepositoryProtocol` utilizando o `api_client` e retornando Entidades e lançando Erros padronizados.
- [x] 2.4 Criar configuração inicial do injeção de dependência via factory ou singleton para inicializar os módulos.
