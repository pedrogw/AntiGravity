## Por quê

Com a fundação da Clean Architecture estabelecida e a observabilidade garantida, precisamos focar no coração do sistema: a lógica de negócio. Atualmente, lógicas complexas como o cálculo de ETA (Estimated Time of Arrival) podem estar misturadas nos Casos de Uso ou controladores, dificultando reuso e testes isolados. Além disso, ações que ocorrem como consequência de eventos de domínio (ex: notificar quando uma entrega muda de status) criam acoplamento rígido se chamadas diretamente. O Bloco 3 resolve isso isolando regras complexas em Domain Services puros e introduzindo Eventos Internos para comunicação assíncrona/desacoplada em memória.

## O que Muda

- **Isolamento de Lógica Complexa (ETA)**: Extração da lógica de cálculo de tempo estimado e rotas para serviços de domínio específicos (`app/domain/services/eta_service.py`), garantindo que os Casos de Uso apenas orquestrem a infraestrutura e chamem o domínio.
- **Eventos Internos (In-Memory)**: Implementação de um barramento de eventos simples (Observer pattern ou lib leve) para que partes do sistema possam reagir a mudanças de estado (ex: `DeliveryCreatedEvent`, `StatusChangedEvent`) sem acoplamento direto de código.
- **Refatoração de Casos de Uso**: Casos de uso existentes de entregas (`deliveries`) serão atualizados para disparar esses eventos e delegar o cálculo de ETA para o novo serviço de domínio.

## Capacidades

### Novas Capacidades
- `eta-calculation-engine`: Motor dedicado ao cálculo e estimativa de tempo de entregas, isolado de frameworks e banco de dados.
- `internal-event-bus`: Mecanismo de publicação e assinatura (Pub/Sub) in-memory para desacoplamento de lógicas reativas (ex: auditoria, notificações).

### Capacidades Modificadas
*(Nenhuma capacidade existente tem seus requisitos funcionais alterados para o usuário final, apenas a engenharia interna de como elas operam).*

## Impacto

| Área | Detalhe |
|---|---|
| `app/domain/services/` | (Novo) Criação de serviços puros de domínio (ex: ETA) |
| `app/core/events/` | (Novo) Implementação do barramento e tipagem dos eventos |
| `app/use_cases/` | Refatoração para injetar o serviço de ETA e disparar eventos após ações de sucesso |
| `app/infrastructure/` | Possíveis "listeners" que reagem a eventos para gravar logs ou disparar webhooks |
