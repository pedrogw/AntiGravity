## ADDED Requirements

### Requirement: Simulação completa de fluxo
O sistema SHALL oferecer um endpoint de demonstração que executa o fluxo completo: criar entrega → calcular ETA → injetar evento de caos → recalcular ETA → verificar janela de recebimento. Tudo em uma única chamada.

#### Scenario: Demo de fluxo completo
- **GIVEN** que o endpoint de demonstração foi acessado para apresentação à banca e o banco possui locais cadastrados
- **WHEN** qualquer usuário faz POST em `/demo/simulate` com factory_id, store_id e chaos_type (opcional)
- **THEN** o sistema executa o fluxo logicamente e retorna um JSON consolidado com: ETA original, evento de caos injetado, ETA recalculado, status da janela de recebimento e alertas gerados

#### Scenario: Demo sem evento de caos
- **GIVEN** a intenção de validar a rota em condições climáticas e de tráfego perfeitas (ideal)
- **WHEN** um POST é disparado para `/demo/simulate` sem explicitar o parâmetro `chaos_type`
- **THEN** o sistema retorna estritamente o cálculo do ETA original puro e o status da janela de recebimento, ignorando o fator caos

#### Scenario: Demo com múltiplos tipos de caos
- **GIVEN** um ambiente de teste rigoroso para provar a tese de acúmulo de variáveis de trânsito
- **WHEN** um POST é disparado para `/demo/simulate` com `chaos_types=["chuva", "engarrafamento"]`
- **THEN** o sistema aplica sequencialmente ambos os eventos, expõe o ETA parcial após cada iteração matemática, e devolve o ETA final consolidado
