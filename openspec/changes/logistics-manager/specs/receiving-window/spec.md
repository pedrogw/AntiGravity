## ADDED Requirements

### Requirement: Configuração de janela de recebimento
O sistema SHALL permitir que o lojista configure os horários em que sua loja aceita recebimento de entregas. A janela MUST ter horário de início e horário de fim para cada dia da semana. Todos os horários MUST ser armazenados em UTC.

#### Scenario: Lojista configura janela de recebimento
- **GIVEN** que um lojista autenticado deseja restringir os horários de descarga de sua loja
- **WHEN** o lojista faz POST em `/stores/{id}/receiving-window` enviando payload com start_time="15:00" e end_time="19:00" (UTC) aplicável aos dias úteis
- **THEN** o sistema valida o formato, salva a janela em UTC no banco garantindo a relação com a loja, e retorna HTTP 201

#### Scenario: Entrega estimada fora da janela
- **GIVEN** que uma loja possui uma janela de recebimento configurada para encerrar estritamente às 19:00 UTC
- **WHEN** uma entrega é roteirizada e seu ETA inicial calculado prever chegada apenas às 21:00 UTC
- **THEN** o sistema detecta o conflito na origem, marca o objeto da entrega com a flag "fora_da_janela", e inclui o próximo horário/dia útil disponível na resposta HTTP

### Requirement: Validação de janela no cálculo de ETA
O sistema SHALL considerar a janela de recebimento ao calcular a viabilidade da entrega. Se o ETA cai fora da janela, o sistema MUST sinalizar o operador.

#### Scenario: ETA dentro da janela
- **GIVEN** uma janela de recebimento ativa entre 15:00 e 19:00 UTC
- **WHEN** o ETA dinâmico reprocessado via Haversine indica chegada para as 16:30 UTC
- **THEN** o sistema isenta qualquer conflito de operação, garantindo que a entrega mantenha a flag de status "dentro_da_janela"

#### Scenario: ETA fora da janela após evento de caos
- **GIVEN** uma entrega em andamento cujo ETA original de 18:30 UTC atendia a janela de fechamento das 19:00 UTC da loja
- **WHEN** um evento de caos atinge a rota (ex: acidente), empurrando o ETA restante recalculado para as 20:00 UTC
- **THEN** o sistema atualiza retroativamente a flag da entrega para "fora_da_janela" e emite notificação assíncrona para que o operador logístico e o lojista tenham visibilidade através das respostas nativas da API
