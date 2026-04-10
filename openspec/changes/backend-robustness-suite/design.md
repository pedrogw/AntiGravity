## User Experience

O cliente final não interage diretamente com esses testes, mas notará a alta estabilidade das APIs durante o consumo do Frontend. Erros bizarros ou injeções de dados absurdos serão barrados na porta de entrada com retornos claros de 422 ou 403.

## Architecture & Implementation Strategy

### Estratégia de Teste

1. **Parâmetros Parametrizados (Pydantic)**:
   - Utilizaremos `@pytest.mark.parametrize` para bombardear o backend com dados inválidos em massa (strings onde deveriam ser floats, latitudes > 90, etc).
   - O objetivo é testar a robustez dos Schemas Pydantic.

2. **Testes de Quebra de Permissões (Scopes)**:
   - Gerar tokens JWT alternados com role `motorista` para tentar acessar endpoints exclusivos de `lojista` (fábricas, lojas).
   - Garantir que o `Depends(get_current_user)` e as checagens de role estejam 100% integradas.

3. **Chaos stress math**:
   - Validar a função `haversine` e `chaos` com distâncias zero ou velocidades astronômicas para garantir que o código não levante exceções não tratadas (ZeroDivisionError, etc).

## Data Model

Nenhuma alteração nos modelos do banco.

## Security & Privacy

Este é o foco principal deste design: **Hardening da autenticação**.

- Validação de expiração de tokens.
- Validação de roles cruzadas.

## Testing Strategy

- `sudo docker compose exec api pytest tests/api/test_validation.py`
- `sudo docker compose exec api pytest tests/api/test_security.py`
- `sudo docker compose exec api pytest tests/domain/test_extreme.py`

## Open Questions

- Devemos configurar um middleware de logs para capturar estes "Invalid Payload Attempts" para auditoria no TCC?
