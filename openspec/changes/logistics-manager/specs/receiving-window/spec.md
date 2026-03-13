## ADDED Requirements

### Requirement: Configuração de janela de recebimento
O sistema SHALL permitir que o lojista configure os horários em que sua loja aceita recebimento de entregas. A janela MUST ter horário de início e horário de fim para cada dia da semana. Todos os horários MUST ser armazenados em UTC.

#### Scenario: Lojista configura janela de recebimento
- **WHEN** lojista faz POST em `/stores/{id}/receiving-window` com start_time="15:00" e end_time="19:00" (UTC) para dias úteis
- **THEN** o sistema salva a janela em UTC e retorna HTTP 201

#### Scenario: Entrega estimada fora da janela
- **WHEN** uma entrega tem ETA de chegada às 21:00 UTC mas a loja fecha recebimento às 19:00 UTC
- **THEN** o sistema marca a entrega com flag "fora_da_janela" e inclui o próximo horário disponível na resposta

### Requirement: Validação de janela no cálculo de ETA
O sistema SHALL considerar a janela de recebimento ao calcular a viabilidade da entrega. Se o ETA cai fora da janela, o sistema MUST sinalizar o operador.

#### Scenario: ETA dentro da janela
- **WHEN** ETA calculado é 16:30 UTC e janela é 15:00–19:00 UTC
- **THEN** o sistema marca entrega como "dentro_da_janela"

#### Scenario: ETA fora da janela após evento de caos
- **WHEN** evento de caos empurra ETA de 18:30 UTC para 20:00 UTC e janela fecha às 19:00 UTC
- **THEN** o sistema atualiza flag para "fora_da_janela" e notifica operador e lojista via resposta da API
