## 1. Hardening de Validação (Pydantic)

- [x] 1.1 Atualizar `backend/app/schemas/place.py` para incluir limites geográficos reais (Lat -90 a 90, Lng -180 a 180) usando `Field`.
- [x] 1.2 Atualizar schemas de `User` e `Delivery` para garantir que campos obrigatórios não aceitem strings vazias.
- [/] 1.3 Criar arquivo `backend/tests/api/test_validation.py` com testes parametrizados enviando payloads propositalmente incorretos e esperando 422.

## 2. Segurança e Controle de Acesso (RBAC)

- [x] 2.1 Refatorar dependência `get_current_user` ou criar um decorador simples para validar a `Role` do usuário logado.
- [x] 2.2 Aplicar restrição na rota `POST /places/factories` e `POST /places/stores` para permitir apenas `Role.lojista`.
- [x] 2.3 Criar arquivo `backend/tests/api/test_security.py` para validar tentativas de acesso com Role errada (403) e Token expirado (401).

## 3. Testes Extremos de Domínio (Math Stress)

- [x] 3.1 Criar `backend/tests/domain/test_extreme.py` para testar as funções puras (`haversine`, `chaos`) com valores de borda: distância zero, velocidades negativas ou extremamente altas, e timestamps de épocas diferentes.
- [x] 3.2 Garantir que o `SafeCheck` não crash o backend caso o `last_ping` seja nulo ou inválido.
