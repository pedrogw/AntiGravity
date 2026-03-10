## ADDED Requirements

### Requirement: Simulação completa de fluxo
O sistema SHALL oferecer um endpoint de demonstração que executa o fluxo completo: criar entrega → calcular ETA → injetar evento de caos → recalcular ETA → verificar janela de recebimento. Tudo em uma única chamada.

#### Scenario: Demo de fluxo completo
- **WHEN** qualquer usuário faz POST em `/demo/simulate` com factory_id, store_id e chaos_type (opcional)
- **THEN** o sistema retorna JSON com: ETA original, evento de caos injetado (se solicitado), ETA recalculado, status da janela de recebimento e alertas gerados

#### Scenario: Demo sem evento de caos
- **WHEN** POST em `/demo/simulate` sem chaos_type
- **THEN** o sistema retorna apenas cálculo de ETA e status da janela, sem caos

#### Scenario: Demo com múltiplos tipos de caos
- **WHEN** POST em `/demo/simulate` com chaos_types=["chuva", "engarrafamento"]
- **THEN** o sistema aplica ambos os eventos, mostra ETA parcial após cada um, e ETA final acumulado
