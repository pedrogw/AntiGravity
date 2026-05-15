## ADDED Requirements

### Requirement: Processamento de Tarefas Não-Bloqueante
O sistema SHALL possuir uma fila de workers assíncronos (Broker) responsável por executar lógicas secundárias ou integrações pesadas fora do *Event Loop* principal da API.

#### Scenario: Enfileiramento Rápido
- **WHEN** o `EventBus` ou a API despacha um job pesado (ex: disparar notificação, gerar relatório)
- **THEN** o sistema MUST colocar a tarefa na fila do Redis de forma imediata e retornar a resposta HTTP sem aguardar a conclusão do processo.

#### Scenario: Processamento Assíncrono Paralelo
- **WHEN** existem tarefas pendentes na fila
- **THEN** o processo Worker (separado da API principal) MUST coletar as tarefas e executá-las usando `asyncio`, suportando tentativas de reexecução (retries) automáticas em caso de falhas temporárias de rede ou I/O.
