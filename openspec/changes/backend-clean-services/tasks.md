## 1. Fundação de Eventos (Event Bus Assíncrono)

- [ ] 1.1 Criar `app/core/events/base.py` com a classe `DomainEvent` genérica e a interface `EventHandler`
- [ ] 1.2 Implementar o `EventBus` (singleton ou injetável) em `app/core/events/bus.py` suportando rotinas `async` via `asyncio.gather` ou `BackgroundTasks`
- [ ] 1.3 Escrever testes unitários básicos para garantir o despacho de eventos e isolamento de falhas em listeners

## 2. Eventos Específicos de Negócio

- [ ] 2.1 Definir `DeliveryCreatedEvent` (contendo dados relevantes da entrega recém-criada)
- [ ] 2.2 Definir `DeliveryStatusChangedEvent` (contendo status antigo e novo)
- [ ] 2.3 Criar um listener de auditoria assíncrono mockado para capturar e logar as criações e mudanças

## 3. Isolamento do Serviço de ETA (Pureza)

- [ ] 3.1 Criar `app/domain/services/eta_service.py`
- [ ] 3.2 Implementar a função pura `calculate_eta(origin_lat, origin_lng, dest_lat, dest_lng, speed_factor)` (ex: via fórmula de Haversine)
- [ ] 3.3 Testar matematicamente a função garantindo independência de bibliotecas web e banco de dados

## 4. Refatoração dos Casos de Uso (Orquestração Correta)

- [ ] 4.1 Injetar as dependências `DeliveryRepository` e `PlaceRepository` no `CreateDeliveryUseCase`
- [ ] 4.2 Alterar a lógica do Use Case para primeiro buscar a `Factory` e `Store` e extrair suas coordenadas (`lat`/`lng`)
- [ ] 4.3 Chamar o `eta_service` passando as coordenadas extraídas e definir o tempo no modelo `Delivery`
- [ ] 4.4 Realizar a persistência: `await repo.create(delivery)`
- [ ] 4.5 Disparar `DeliveryCreatedEvent` através do `EventBus` **apenas após o sucesso da linha anterior**

## 5. Validação Final

- [ ] 5.1 Atualizar os testes de integração (`test_deliveries.py` ou similar) provendo instâncias de `Factory` e `Store` válidas para permitir o cálculo de ETA
- [ ] 5.2 Rodar `pytest -v` e confirmar logs do EventBus disparando adequadamente após a persistência bem-sucedida
