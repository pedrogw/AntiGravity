## Why

Com a finalização do Motor Analítico e dos testes de integração básicos, o foco atual é elevar a confiabilidade do produto ("Robustness"). É de interesse do cliente garantir que o backend seja resiliente a entradas malformadas, cenários de borda extremos e tentativas de acesso não autorizado antes que o desenvolvimento do Frontend (Fase 3) comece a consumir estas APIs de forma intensiva.

## What Changes

Propomos a inclusão de uma Suíte de Robustez que cubra:
1. **Validação de Inputs Rigorosa**: Testar limites geográficos (Lat/Lng inválidos), nomes vazios e payloads corrompidos.
2. **Resiliência a Caos Extremo**: Validar como o sistema se comporta com fatores de atraso absurdamente altos ou negativos.
3. **Segurança e RBAC (Role Based Access Control)**: Garantir que um `motorista` não consiga criar `factories` e que tokens expirados sejam devidamente rejeitados.

## Capabilities

### New Capabilities
- `validation-hardening`: Testes focados em quebrar as validações Pydantic com dados de borda.
- `security-edge-testing`: Verificação rigorosa de escopo de JWT e permissões de roles.
- `extreme-chaos-validation`: Testes de estresse da lógica matemática sob parâmetros de simulação extremos.

### Modified Capabilities

## Impact

Aumenta significativamente a cobertura de testes sem alterar a lógica de produção atual, servindo como uma rede de segurança para as futuras integrações do dashboard.
