## 1. Casos de Uso Base (Autenticação)

- [x] 1.1 Criar a interface abstrata de UseCase se necessário (ex: `UseCase<Input, Output>`).
- [x] 1.2 Implementar `LoginUseCase` injetando `AuthRepositoryProtocol` e `TokenStorageAdapter` e escrevendo TDD (Testes Unitários no Vitest antes do código real).
- [x] 1.3 Implementar `LogoutUseCase`.
- [x] 1.4 Criar a Factory correspondente (`makeLoginUseCase`) em `src/infrastructure/di/factories.ts`.

## 2. Casos de Uso Secundários (Locais e Entregas)

- [x] 2.1 Implementar `CreateDeliveryUseCase` injetando `DeliveryRepositoryProtocol`.
- [x] 2.2 Implementar `ListDeliveriesUseCase`.
- [x] 2.3 Implementar `CreateFactoryUseCase` e `CreateStoreUseCase` baseados em `PlaceRepositoryProtocol`.
- [x] 2.4 Criar as Factories para esses Casos de Uso.
- [x] 2.5 Garantir cobertura de Vitest para todos esses Casos de Uso.
